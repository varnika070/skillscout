import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="min-h-screen bg-gradient-primary flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="w-16 h-16 text-white animate-spin mx-auto mb-4" />
        <p className="text-xl text-white font-semibold">{message}</p>
        <p className="text-sm text-white/80 mt-2">AI is analyzing your learning path...</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;