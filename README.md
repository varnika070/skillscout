# SkillScout Frontend

AI-powered learning guidance platform for Indian learners.

## Features

- 🎯 Personalized learning path generation
- 🌐 Bilingual support (English & Hindi)
- 📱 Mobile-responsive design
- 🎨 Clean, accessible UI with Tailwind CSS
- ✅ Progress tracking
- 📚 Resource recommendations with YouTube integration
- 💡 Community learning insights

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
├── app/
│   ├── api/
│   │   └── generate-path/
│   │       └── route.ts          # Mock API endpoint
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Home page
│   └── globals.css               # Global styles
├── components/
│   ├── OnboardingForm.tsx        # User onboarding form
│   ├── LearningPath.tsx          # Learning path display
│   └── LanguageToggle.tsx        # Language switcher
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## Backend Integration

The current implementation uses a mock API endpoint at `/app/api/generate-path/route.ts`. 

To integrate with the FastAPI backend:

1. Update the API endpoint URL in `components/OnboardingForm.tsx`
2. Replace the mock response with actual backend calls
3. Configure CORS settings if needed

Example:

```typescript
const response = await axios.post('http://localhost:8000/api/generate-path', {
  goal,
  currentSkills,
  background,
  timeline,
  language,
})
```

## Key Features Implementation

### Bilingual Support
- Language toggle between English and Hindi
- Translations for all UI elements
- Bhashini integration ready (backend)

### Learning Path Generation
- User onboarding with goal and skill input
- Personalized path with prerequisites
- Estimated timelines for each step

### Progress Tracking
- Mark steps as complete
- Visual progress bar
- Persistent state during session

### Resource Recommendations
- Primary resource links
- YouTube video tutorials (filtered)
- Community insights

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Other Platforms

The app can be deployed to any platform supporting Next.js:
- Netlify
- Railway
- AWS Amplify

## Environment Variables

Create a `.env.local` file for environment-specific configuration:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Contributing

This is a hackathon project. For production use:
1. Replace mock API with actual backend
2. Add error boundaries
3. Implement proper authentication
4. Add comprehensive testing
5. Optimize performance with caching

## License

MIT
