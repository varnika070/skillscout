'use client'

import { useState } from 'react'
import OnboardingForm from '@/components/OnboardingForm'
import LearningPath from '@/components/LearningPath'
import LanguageToggle from '@/components/LanguageToggle'

export default function Home() {
    const [learningPath, setLearningPath] = useState(null)
    const [language, setLanguage] = useState<'en' | 'hi'>('en')

    return (
        <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
            <div className="container mx-auto px-4 py-8">
                <header className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-4xl font-bold text-primary">SkillScout</h1>
                        <p className="text-gray-600 mt-2">
                            {language === 'en'
                                ? 'Your AI-powered learning guide'
                                : 'आपका AI-संचालित सीखने का मार्गदर्शक'}
                        </p>
                    </div>
                    <LanguageToggle language={language} setLanguage={setLanguage} />
                </header>

                {!learningPath ? (
                    <OnboardingForm
                        setLearningPath={setLearningPath}
                        language={language}
                    />
                ) : (
                    <LearningPath
                        path={learningPath}
                        language={language}
                        onReset={() => setLearningPath(null)}
                    />
                )}
            </div>
        </main>
    )
}
