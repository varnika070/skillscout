import React from 'react';
import { AlertTriangle, Users, ArrowRight, CheckCircle2, X } from 'lucide-react';

const GapDetection = ({ gapData, language, onContinue, onBack }) => {
  if (!gapData || !gapData.next_critical_gap) {
    return null;
  }

  const gapSkill = gapData.learning_path.find(
    (skill) => skill.id === gapData.next_critical_gap
  );

  if (!gapSkill) return null;

  const content = {
    en: {
      title: 'Prerequisite Gap Detected',
      missing: "You're missing:",
      whyMatters: 'Why this matters:',
      community: 'Community Insight',
      struggled: 'of learners struggled here',
      btnPrimary: 'Learn This First',
      btnSecondary: 'I Already Know This',
      estimate: 'Estimated time:',
      days: 'days'
    },
    hi: {
      title: 'Prerequisite Gap का पता चला',
      missing: 'आपके पास यह नहीं है:',
      whyMatters: 'यह क्यों ज़रूरी है:',
      community: 'Community Insight',
      struggled: 'learners को यहाँ struggle हुआ',
      btnPrimary: 'पहले यह सीखें',
      btnSecondary: 'मुझे पता है',
      estimate: 'समय:',
      days: 'दिन'
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
          <X className="w-5 h-5 mr-2" />
          Back
        </button>
        <h1 className="text-2xl font-bold">
          {language === 'en' ? 'Your Learning Path' : 'आपका Learning Path'}
        </h1>
        <p className="text-white/90 mt-1">
          {language === 'en' 
            ? `Goal: ${gapData.target_skill_name}` 
            : `लक्ष्य: ${gapData.target_skill_name}`}
        </p>
      </div>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Gap Alert - THE MONEY SHOT */}
        <div className="bg-warning-light border-l-4 border-warning rounded-xl p-6 mb-6 shadow-xl animate-slide-up">
          <div className="flex items-start gap-4 mb-4">
            <div className="bg-warning rounded-full p-3">
              <AlertTriangle className="w-8 h-8 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                ⚠️ {text.title}
              </h2>
              <p className="text-gray-700 mb-3">
                <span className="font-semibold">{text.missing}</span>
              </p>
              <p className="text-2xl font-bold text-warning mb-4">
                {gapSkill.name}
              </p>
            </div>
          </div>

          {/* Explanation */}
          <div className="bg-white rounded-lg p-4 mb-4">
            <p className="text-sm font-semibold text-gray-700 mb-2">
              {text.whyMatters}
            </p>
            <p className="text-gray-700 leading-relaxed">
              {gapSkill.why_now}
            </p>
          </div>

          {/* Community Badge */}
          {gapSkill.community && (
            <div className="bg-blue-100 text-blue-800 px-4 py-3 rounded-lg inline-flex items-center gap-2 mb-4">
              <Users className="w-5 h-5" />
              <span className="font-semibold">
                📊 {gapSkill.community.struggle_rate}% {text.struggled}
              </span>
            </div>
          )}

          {/* Time Estimate */}
          <div className="text-sm text-gray-600 mb-6">
            {text.estimate} <strong>{gapSkill.estimated_days} {text.days}</strong>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3">
            <button
              onClick={onContinue}
              className="w-full bg-gradient-warning text-white font-bold py-4 px-6 rounded-xl
                       shadow-lg hover:shadow-xl transform hover:scale-105 transition-all
                       flex items-center justify-center gap-2"
            >
              <CheckCircle2 className="w-5 h-5" />
              {text.btnPrimary}
            </button>
            <button
              onClick={onContinue}
              className="w-full bg-white border-2 border-gray-300 text-gray-700 font-bold 
                       py-4 px-6 rounded-xl hover:border-primary hover:text-primary 
                       transition-all flex items-center justify-center gap-2"
            >
              {text.btnSecondary}
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Community Tip (if available) */}
        {gapSkill.community?.helpful_tip && (
          <div className="bg-white rounded-xl p-6 shadow-md border-l-4 border-primary">
            <h3 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
              <Users className="w-5 h-5 text-primary" />
              {language === 'en' ? 'Pro Tip from Community' : 'Community से Pro Tip'}
            </h3>
            <p className="text-gray-700 italic">
              "{gapSkill.community.helpful_tip}"
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default GapDetection;