import { NextResponse } from 'next/server'

// Mock API endpoint - replace with actual FastAPI backend call
export async function POST(request: Request) {
    try {
        const body = await request.json()
        const { goal, currentSkills, background, timeline, language } = body

        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500))

        // Mock response - replace with actual backend integration
        const mockPath = {
            goal: goal,
            totalDuration: timeline === '1-3-months' ? '2-3 months' : timeline === '3-6-months' ? '4-5 months' : '8-10 months',
            steps: [
                {
                    id: '1',
                    skill: language === 'hi' ? 'HTML और CSS की बुनियादी बातें' : 'HTML & CSS Fundamentals',
                    explanation: language === 'hi'
                        ? 'वेब पेज बनाने के लिए HTML और CSS आवश्यक हैं। HTML संरचना प्रदान करता है जबकि CSS स्टाइलिंग करता है।'
                        : 'HTML and CSS are essential for building web pages. HTML provides structure while CSS handles styling.',
                    prerequisites: [],
                    estimatedTime: '2-3 weeks',
                    resources: {
                        primary: 'MDN Web Docs - HTML & CSS',
                        videos: [
                            'HTML Crash Course (Hindi)',
                            'CSS Complete Tutorial',
                            'Responsive Design Basics'
                        ]
                    },
                    communityInsight: language === 'hi'
                        ? '85% शिक्षार्थियों ने flexbox को चुनौतीपूर्ण पाया - अभ्यास पर ध्यान दें'
                        : '85% of learners found flexbox challenging - focus on practice'
                },
                {
                    id: '2',
                    skill: language === 'hi' ? 'JavaScript प्रोग्रामिंग' : 'JavaScript Programming',
                    explanation: language === 'hi'
                        ? 'JavaScript वेब पेजों को इंटरैक्टिव बनाता है। यह आधुनिक वेब विकास के लिए महत्वपूर्ण है।'
                        : 'JavaScript makes web pages interactive. It is crucial for modern web development.',
                    prerequisites: ['HTML & CSS Fundamentals'],
                    estimatedTime: '4-6 weeks',
                    resources: {
                        primary: 'JavaScript.info',
                        videos: [
                            'JavaScript Basics (Hindi)',
                            'ES6 Features Explained',
                            'Async JavaScript Tutorial'
                        ]
                    },
                    communityInsight: language === 'hi'
                        ? '78% ने closures और async/await को कठिन पाया - अतिरिक्त समय दें'
                        : '78% found closures and async/await difficult - allocate extra time'
                },
                {
                    id: '3',
                    skill: language === 'hi' ? 'React Framework' : 'React Framework',
                    explanation: language === 'hi'
                        ? 'React एक लोकप्रिय JavaScript library है जो user interfaces बनाने के लिए उपयोग की जाती है।'
                        : 'React is a popular JavaScript library for building user interfaces.',
                    prerequisites: ['JavaScript Programming'],
                    estimatedTime: '3-4 weeks',
                    resources: {
                        primary: 'Official React Documentation',
                        videos: [
                            'React Complete Course (Hindi)',
                            'React Hooks Deep Dive',
                            'State Management Tutorial'
                        ]
                    },
                    communityInsight: language === 'hi'
                        ? '92% ने hooks सीखने के बाद तेजी से प्रगति की'
                        : '92% progressed faster after learning hooks'
                }
            ]
        }

        return NextResponse.json(mockPath)
    } catch (error) {
        console.error('Error:', error)
        return NextResponse.json(
            { error: 'Failed to generate learning path' },
            { status: 500 }
        )
    }
}
