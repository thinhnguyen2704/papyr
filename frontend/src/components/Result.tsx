import React from 'react';
import { Copy, Check, FileText } from 'lucide-react';

interface ResultCardProps {
  result: string;
  copySuccess: boolean;
  copy: () => void;
  darkMode: boolean;
  labels: {
    resultHeader: string;
    copy: string;
    copied: string;
    error: string;
    uploadFailed: string;
    noText: string;
  };
}

export const ResultCard: React.FC<ResultCardProps> = ({ 
  result, 
  copySuccess, 
  copy, 
  darkMode,
  labels
}) => {
  return (
    <div className={`w-full rounded-4xl p-8 shadow-2xl border transition-all duration-500 ${
      darkMode 
        ? 'bg-white/95 border-white/20' 
        : 'bg-white border-zinc-200 shadow-zinc-300/50'
    }`}>
      
      <div className="flex items-center justify-between mb-6 border-b border-zinc-200/60 pb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-blue-50 rounded-lg">
            <FileText className="text-blue-600" size={20} />
          </div>
          <h2 className="text-zinc-900 font-bold tracking-tight text-lg">{labels.resultHeader}</h2>
        </div>
        
        <button
          onClick={copy}
          className={`flex items-center gap-2 px-4 py-2 rounded-full font-bold text-xs transition-all active:scale-95 ${
            copySuccess 
              ? 'bg-green-500 text-white' 
              : 'bg-zinc-900 text-white hover:bg-zinc-700'
          }`}
        >
          {copySuccess ? <Check size={14} /> : <Copy size={14} />}
          {copySuccess ? labels.copied : labels.copy}
        </button>
      </div>

      {/* Text Area */}
      <p className="text-zinc-800 text-base leading-relaxed whitespace-pre-line font-medium max-h-64 overflow-y-auto custom-scrollbar">
        {result ? result : labels.noText}
      </p>
    </div>
  );
};