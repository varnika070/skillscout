import React, { useState } from 'react';
import GoalSelection from './components/GoalSelection';
import GapDetection from './components/GapDetection';
import LearningPath from './components/LearningPath';
import LoadingSpinner from './components/LoadingSpinner';
import { generateLearningPath } from './services/api';
import { DEMO_CURRENT_SKILLS } from './utils/constants';

function App() {
  const [step, setStep] = useState('goal'); // 'goal' | 'gap' | 'path'
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  const [pathData, setPathData] = useState(null);
  const [error, setError] = useState(null);

  const handleSelectGoal = async (goalId) => {
    setLoading(true);
    setError(null);

    try {
      const data = await generateLearningPath(goalId, DEMO_CURRENT_SKILLS);
      setPathData(data);
      
      // If there's a critical gap, show gap detection screen
      if (data.next_critical_gap) {
        setStep('gap');
      } else {
        setStep('path');
      }
    } catch (err) {
      console.error('Error generating path:', err);
      setError(err.message || 'Failed to generate learning path');
      alert('Error: Make sure backend is running on http://localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  const handleContinueFromGap = () => {
    setStep('path');
  };

  const handleBack = () => {
    setStep('goal');
    setPathData(null);
    setError(null);
  };

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'hi' : 'en');
  };

  if (loading) {
    return <LoadingSpinner message="Analyzing your learning path..." />;
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl p-8 max-w-md shadow-xl">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-gray-700 mb-4">{error}</p>
          <button onClick={handleBack} className="btn-primary w-full">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  switch (step) {
    case 'gap':
      return (
        <GapDetection
          gapData={pathData}
          language={language}
          onContinue={handleContinueFromGap}
          onBack={handleBack}
        />
      );
    
    case 'path':
      return (
        <LearningPath
          pathData={pathData}
          language={language}
          onBack={handleBack}
        />
      );
    
    case 'goal':
    default:
      return (
        <GoalSelection
          onSelectGoal={handleSelectGoal}
          language={language}
          onToggleLanguage={toggleLanguage}
        />
      );
  }
}

export default App;