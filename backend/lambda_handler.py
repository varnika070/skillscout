"""
AWS Lambda Handler for SkillScout API
Wraps FastAPI application with Mangum for serverless deployment
"""

import os
import sys

# Add current directory to path for Lambda
sys.path.insert(0, os.path.dirname(__file__))

from mangum import Mangum
from main import app

# Create Lambda handler
# Mangum wraps FastAPI to work with AWS Lambda + API Gateway
handler = Mangum(app, lifespan="off")

# For local testing
if __name__ == "__main__":
    import uvicorn
    print("🚀 Running in local mode...")
    print("   Access API at: http://localhost:8000")
    print("   API docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)