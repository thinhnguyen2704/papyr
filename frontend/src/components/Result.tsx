import React from 'react';
import { Copy, Check, FileText } from 'lucide-react';

interface ResultCardProps {
  result: string;
  copySuccess: boolean;
  copy: () => void;
}

export const ResultCard: React.FC<ResultCardProps> = ({ result, copySuccess, copy }) => {
  return (
    <div className="w-full bg-white/95 backdrop-blur-md rounded-[2rem] p-8 shadow-[0_20px_50px_rgba(0,0,0,0.3)] border border-white/20 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      {/* Header Area */}
      <div className="flex items-center justify-between mb-6 border-b border-zinc-200 pb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-blue-100 rounded-lg">
            <FileText className="text-blue-600" size={20} />
          </div>
          <h2 className="text-zinc-900 font-bold tracking-tight text-lg">Extracted Text</h2>
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
          {copySuccess ? 'COPIED' : 'COPY TEXT'}
        </button>
      </div>

      {/* Text Output Area */}
      <div className="relative">
        <p className="text-zinc-800 text-base leading-relaxed whitespace-pre-line font-medium selection:bg-blue-100 max-h-64 overflow-y-auto pr-2 custom-scrollbar">
          {result}
        </p>
        
        {/* Subtle Gradient Fade at bottom for long text */}
        <div className="absolute bottom-0 left-0 w-full h-8 bg-linear-to-t from-white/50 to-transparent pointer-events-none" />
      </div>
    </div>
  );
};