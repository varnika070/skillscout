import React from 'react';
import { ArrowRight, Sparkles } from 'lucide-react';
import { CAREER_GOALS } from '../utils/constants';
import LanguageToggle from './LanguageToggle';

const GoalSelection = ({ onSelectGoal, language, onToggleLanguage }) => {
  const content = {
    en: {
      title: "What's your learning goal?",
      subtitle: "We'll create a personalized path with AI-powered guidance",
      footer: "Powered by AI • 50,000+ learners helped"
    },
    hi: {
      title: "आप क्या सीखना चाहते हैं?",
      subtitle: "हम AI की मदद से आपके लिए personalized path बनाएंगे",
      footer: "AI से powered • 50,000+ learners की मदद की"
    }
  };

  const text = content[language];

  return (
    <div className="min-h-screen bg-gradient-primary">
      {/* Header */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-yellow-300" />
            <h1 className="text-2xl font-bold text-white">SkillScout</h1>
          </div>
          <LanguageToggle language={language} onToggle={onToggleLanguage} />
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12 max-w-5xl">
        <div className="text-center mb-12 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            {text.title}
          </h2>
          <p className="text-xl text-white/90">
            {text.subtitle}
          </p>
        </div>

        {/* Career Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {CAREER_GOALS.map((goal, index) => (
            <div
              key={goal.id}
              className="card p-6 cursor-pointer transform hover:scale-105 transition-all duration-300 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
              onClick={() => onSelectGoal(goal.id)}
            >
              <div className="flex items-start gap-4">
                <div className={`text-5xl bg-gradient-to-br ${goal.color} p-4 rounded-2xl`}>
                  {goal.emoji}
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-gray-800 mb-1">
                    {goal.title}
                  </h3>
                  <p className="text-sm text-primary font-semibold mb-2">
                    {goal.subtitle}
                  </p>
                  <p className="text-gray-600 text-sm mb-3">
                    {goal.description}
                  </p>
                  <div className="flex items-center text-primary font-semibold text-sm">
                    <span>Start Learning</span>
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="text-center text-white/70 text-sm">
          {text.footer}
        </div>
      </div>
    </div>
  );
};

export default GoalSelection;