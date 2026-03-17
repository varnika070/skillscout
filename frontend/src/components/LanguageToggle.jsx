import React from 'react';
import { Globe } from 'lucide-react';

const LanguageToggle = ({ language, onToggle }) => {
  return (
    <button
      onClick={onToggle}
      className="flex items-center gap-2 bg-white/20 hover:bg-white/30 text-white 
                 px-4 py-2 rounded-full text-sm font-medium transition-all"
    >
      <Globe className="w-4 h-4" />
      <span>{language === 'en' ? 'English' : 'हिंदी'}</span>
      <span className="text-xs opacity-75">|</span>
      <span className="text-xs opacity-75">{language === 'en' ? 'Switch to हिंदी' : 'Switch to EN'}</span>
    </button>
  );
};

export default LanguageToggle;