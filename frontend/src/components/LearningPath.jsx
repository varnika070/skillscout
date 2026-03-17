import React from 'react';
import { CheckCircle2, Circle, Clock, TrendingUp, Users, ArrowLeft } from 'lucide-react';
import { DIFFICULTY_COLORS, DIFFICULTY_LABELS } from '../utils/constants';

const LearningPath = ({ pathData, language, onBack }) => {
  if (!pathData) return null;

  const content = {
    en: {
      title: 'Your Complete Learning Path',
      subtitle: 'Follow this sequence for optimal learning',
      timeline: 'Timeline',
      weeks: 'weeks',
      days: 'days',
      totalTime: 'Total Time',
      skillsToLearn: 'Skills to Master',
      difficulty: 'Difficulty',
      timeRequired: 'Time Required',
      whyNow: 'Why Learn This Now',
      communityTip: 'Community Tip',
      startLearning: 'Start Learning'
    },
    hi: {
      title: 'आपका Complete Learning Path',
      subtitle: 'सबसे अच्छे result के लिए यह sequence follow करें',
      timeline: 'Timeline',
      weeks: 'हफ्ते',
      days: 'दिन',
      totalTime: 'Total Time',
      skillsToLearn: 'सीखने के लिए Skills',
      difficulty: 'Difficulty',
      timeRequired: 'समय',
      whyNow: 'अभी क्यों सीखें',
      communityTip: 'Community Tip',
      startLearning: 'शुरू करें'
    }
  };

  const text = content[language];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-primary text-white p-6 shadow-lg">
        <button
          onClick={onBack}
          className="mb-4 flex items-center text-white/90 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          {language === 'en' ? 'Back' : 'वापस'}
        </button>
        <h1 className="text-3xl font-bold mb-2">{text.title}</h1>
        <p className="text-white/90">{text.subtitle}</p>
      </div>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Timeline Summary */}
        <div className="bg-gradient-primary text-white rounded-2xl p-6 mb-8 shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm mb-1">{text.totalTime}</p>
              <p className="text-4xl font-bold">
                {pathData.total_weeks} {text.weeks}
              </p>
              <p className="text-white/80 text-sm mt-1">
                ({pathData.total_days} {text.days})
              </p>
            </div>
            <div className="text-right">
              <p className="text-white/80 text-sm mb-1">{text.skillsToLearn}</p>
              <p className="text-4xl font-bold">{pathData.learning_path.length}</p>
              <p className="text-white/80 text-sm mt-1">
                <TrendingUp className="w-4 h-4 inline mr-1" />
                {text.timeline}
              </p>
            </div>
          </div>
        </div>

        {/* Learning Path */}
        <div className="space-y-4">
          {pathData.learning_path.map((skill, index) => (
            <div
              key={skill.id}
              className="card p-6 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Skill Header */}
              <div className="flex items-start gap-4 mb-4">
                <div className="flex-shrink-0">
                  {skill.is_critical_gap ? (
                    <div className="w-10 h-10 bg-warning rounded-full flex items-center justify-center">
                      <span className="text-white font-bold">{index + 1}</span>
                    </div>
                  ) : (
                    <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
                      <span className="text-white font-bold">{index + 1}</span>
                    </div>
                  )}
                </div>
                
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-bold text-gray-800">
                      {skill.name}
                      {skill.is_critical_gap && (
                        <span className="ml-2 text-warning text-sm">⚠️ Critical Gap</span>
                      )}
                    </h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${DIFFICULTY_COLORS[skill.difficulty]}`}>
                      {DIFFICULTY_LABELS[skill.difficulty]}
                    </span>
                  </div>
                  
                  <p className="text-gray-600 text-sm mb-3">
                    {skill.description}
                  </p>

                  <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {skill.estimated_days} {text.days}
                    </span>
                    {skill.community && (
                      <span className="flex items-center gap-1">
                        <Users className="w-4 h-4" />
                        {skill.community.struggle_rate}% struggled
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Why Now Explanation */}
              {skill.why_now && (
                <div className="bg-blue-50 rounded-lg p-4 mb-3">
                  <p className="text-sm font-semibold text-gray-700 mb-2">
                    💡 {text.whyNow}:
                  </p>
                  <p className="text-gray-700 leading-relaxed text-sm">
                    {skill.why_now}
                  </p>
                </div>
              )}

              {/* Community Tip */}
              {skill.community?.helpful_tip && (
                <div className="bg-green-50 rounded-lg p-4">
                  <p className="text-sm font-semibold text-gray-700 mb-2">
                    ✨ {text.communityTip}:
                  </p>
                  <p className="text-gray-700 text-sm italic">
                    "{skill.community.helpful_tip}"
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Action Button */}
        <div className="mt-8">
          <button className="btn-primary w-full text-lg py-4">
            {text.startLearning} 🚀
          </button>
        </div>
      </div>
    </div>
  );
};

export default LearningPath;