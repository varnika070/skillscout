#!/bin/bash

echo "🚀 SkillScout Lambda Deployment Script"
echo "========================================"
echo ""

# Configuration
FUNCTION_NAME="skillscout-api"
REGION="us-east-1"
RUNTIME="python3.11"
HANDLER="lambda_handler.handler"
TIMEOUT=30
MEMORY=512

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "📦 Step 1: Creating deployment package..."
echo ""

# Clean previous builds
rm -rf lambda_package
rm -f skillscout-lambda.zip

# Create package directory
mkdir lambda_package

# Copy application files
echo "   Copying application files..."
cp main.py lambda_package/
cp graph_engine.py lambda_package/
cp ai_service.py lambda_package/
cp lambda_handler.py lambda_package/

# Copy .env (WARNING: Don't do this in real production!)
# In production, use Lambda environment variables instead
echo "   Copying environment configuration..."
cp .env lambda_package/

# Install dependencies
echo "   Installing Python dependencies..."
pip install -r requirements.txt -t lambda_package/ --quiet

# Create ZIP file
echo "   Creating ZIP archive..."
cd lambda_package
zip -r ../skillscout-lambda.zip . -q
cd ..

# Get file size
SIZE=$(du -h skillscout-lambda.zip | cut -f1)

echo ""
echo -e "${GREEN}✅ Deployment package created!${NC}"
echo "   File: skillscout-lambda.zip"
echo "   Size: $SIZE"
echo ""

# Check if AWS CLI is configured
if ! command -v aws &> /dev/null; then
    echo -e "${YELLOW}⚠️  AWS CLI not found${NC}"
    echo ""
    echo "Manual deployment steps:"
    echo "1. Go to AWS Lambda Console"
    echo "2. Create function: $FUNCTION_NAME"
    echo "3. Runtime: $RUNTIME"
    echo "4. Upload: skillscout-lambda.zip"
    echo "5. Handler: $HANDLER"
    echo "6. Timeout: $TIMEOUT seconds"
    echo "7. Memory: ${MEMORY}MB"
    echo "8. Add environment variable: OPENAI_API_KEY"
    exit 0
fi

# Check if function exists
echo "📡 Step 2: Checking if Lambda function exists..."
if aws lambda get-function --function-name $FUNCTION_NAME --region $REGION &> /dev/null; then
    echo "   Function exists, updating..."
    
    # Update function code
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://skillscout-lambda.zip \
        --region $REGION \
        --no-cli-pager
    
    echo -e "${GREEN}✅ Function code updated!${NC}"
else
    echo "   Function doesn't exist, creating..."
    
    # Create IAM role first (if needed)
    echo "   Creating IAM role..."
    
    # Create function
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime $RUNTIME \
        --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
        --handler $HANDLER \
        --zip-file fileb://skillscout-lambda.zip \
        --timeout $TIMEOUT \
        --memory-size $MEMORY \
        --region $REGION \
        --no-cli-pager
    
    echo -e "${GREEN}✅ Function created!${NC}"
fi

echo ""
echo "🔑 Step 3: Setting environment variables..."

# Set environment variables
aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --environment "Variables={OPENAI_API_KEY=$OPENAI_API_KEY,ENV=production}" \
    --region $REGION \
    --no-cli-pager > /dev/null

echo -e "${GREEN}✅ Environment variables configured!${NC}"

echo ""
echo "🌐 Step 4: Getting function URL..."

# Get function URL (if configured)
FUNCTION_URL=$(aws lambda get-function-url-config \
    --function-name $FUNCTION_NAME \
    --region $REGION \
    --query 'FunctionUrl' \
    --output text 2>/dev/null)

if [ -z "$FUNCTION_URL" ] || [ "$FUNCTION_URL" == "None" ]; then
    echo -e "${YELLOW}⚠️  Function URL not configured${NC}"
    echo "   Configure via AWS Console or:"
    echo "   aws lambda create-function-url-config --function-name $FUNCTION_NAME"
else
    echo -e "${GREEN}✅ Function URL:${NC} $FUNCTION_URL"
fi

echo ""
echo "========================================"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Test Lambda: aws lambda invoke --function-name $FUNCTION_NAME response.json"
echo "2. Check logs: aws logs tail /aws/lambda/$FUNCTION_NAME --follow"
echo "3. Update API Gateway to point to new Lambda"
echo ""

# Cleanup
echo "🧹 Cleaning up..."
rm -rf lambda_package
echo -e "${GREEN}✅ Done!${NC}"