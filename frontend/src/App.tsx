import { useState } from 'react';
import axios from 'axios';
import { ShieldCheck, ShieldAlert, ShieldX, Loader2, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

type RiskLevel = "Secure" | "Suspicious" | "Dangerous";

interface AnalysisResponse {
  risk_score: number;
  risk_level: RiskLevel;
  explanation: string;
  recommendation: string;
}

function App() {
  const [input, setInput] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [result, setResult] = useState<AnalysisResponse | null>(null);

  const analyzeContent = async () => {
    if (!input.trim()) return;
    setStatus('loading');
    setResult(null);

    try {
      const { data } = await axios.post<AnalysisResponse>('http://127.0.0.1:8000/api/v1/analyze', { content: input });
      setStatus('success');
      setResult(data);
    } catch (err) {
      console.error(err);
      setStatus('error');
    }
  };

  const getRiskColor = (level: RiskLevel) => {
    switch (level) {
      case 'Secure': return 'text-emerald-800 bg-emerald-50 border-emerald-300';
      case 'Suspicious': return 'text-amber-800 bg-amber-50 border-amber-300';
      case 'Dangerous': return 'text-rose-800 bg-rose-50 border-rose-300';
      default: return 'text-slate-800 bg-slate-50 border-slate-300';
    }
  };

  const getRiskBg = (level: RiskLevel) => {
    switch (level) {
      case 'Secure': return 'bg-emerald-500';
      case 'Suspicious': return 'bg-amber-500';
      case 'Dangerous': return 'bg-rose-500';
      default: return 'bg-slate-500';
    }
  };

  const getRiskIcon = (level: RiskLevel) => {
    switch (level) {
      case 'Secure': return <ShieldCheck className="w-20 h-20 text-emerald-600 mx-auto mb-6 drop-shadow-md" />;
      case 'Suspicious': return <ShieldAlert className="w-20 h-20 text-amber-600 mx-auto mb-6 drop-shadow-md" />;
      case 'Dangerous': return <ShieldX className="w-20 h-20 text-rose-600 mx-auto mb-6 drop-shadow-md" />;
      default: return null;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center py-16 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-4xl w-full space-y-10">
        
        <div className="text-center">
          <div className="inline-flex items-center justify-center p-4 bg-indigo-100 rounded-full mb-6 relative">
             <div className="absolute inset-0 bg-indigo-400 rounded-full blur-md opacity-20 animate-pulse"></div>
             <ShieldCheck className="h-14 w-14 text-indigo-700 relative z-10" />
          </div>
          <h1 className="text-5xl font-extrabold text-slate-900 tracking-tight">Veridict AI</h1>
          <p className="mt-4 text-xl text-slate-600 font-light max-w-2xl mx-auto">
            Your privacy-first intelligent cybersecurity assistant. Validate suspicious messages and links in seconds.
          </p>
        </div>

        <div className="bg-white py-10 px-8 rounded-3xl shadow-xl border border-slate-100 relative overflow-hidden">
           <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 to-purple-500"></div>
          
          <label htmlFor="content" className="block text-lg font-medium text-slate-800 mb-3">
            Paste your content here
          </label>
          <div className="mt-2 relative">
            <textarea
              id="content"
              rows={4}
              className="appearance-none block w-full px-5 py-4 border border-slate-200 rounded-xl bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white focus:border-transparent transition-all sm:text-base resize-none shadow-inner"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
          </div>
          
          <div className="mt-8">
            <button
              onClick={analyzeContent}
              disabled={status === 'loading' || !input.trim()}
              className="w-full flex justify-center items-center py-4 px-6 rounded-xl shadow-lg text-lg font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:scale-[1.01] active:scale-[0.99]"
            >
              {status === 'loading' ? (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center">
                  <Loader2 className="w-6 h-6 mr-3 animate-spin" />
                  Analyzing Risk Profile...
                </motion.div>
              ) : 'Analyze Content'}
            </button>
          </div>
        </div>

        <AnimatePresence>
          {status === 'error' && (
            <motion.div
              key="error"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="p-6 rounded-2xl bg-red-100 border border-red-200 text-red-800 text-center shadow-md font-medium flex items-center justify-center mt-4"
            >
              <ShieldX className="w-6 h-6 mr-3" />
              An error occurred while validating your input. Ensure the backend server is running!
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <AnimatePresence>
        {status === 'success' && result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 min-h-screen border-none bg-slate-900/60 backdrop-blur-sm z-[9999] flex items-center justify-center p-4 sm:p-6"
            onClick={() => setStatus('idle')}
            style={{ width: "100vw", height: "100vh", position: "fixed", top: 0, left: 0 }}
          >
            <motion.div
              onClick={(e) => e.stopPropagation()}
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              transition={{ type: "spring", damping: 25, stiffness: 300 }}
              className={cn("w-full max-w-2xl p-8 sm:p-10 rounded-3xl border shadow-2xl relative overflow-y-auto max-h-[90vh]", getRiskColor(result.risk_level))}
            >
              <button 
                onClick={() => setStatus('idle')}
                className="absolute top-4 right-4 p-2 rounded-full hover:bg-black/10 transition-colors"
              >
                <span className="font-bold text-xl">✕</span>
              </button>

              <div className={cn("absolute top-0 left-0 w-full h-2", getRiskBg(result.risk_level))}></div>
              
              <div className="text-center">
                {getRiskIcon(result.risk_level)}
                <h3 className="text-4xl font-extrabold mb-3 tracking-tight">Risk Level: {result.risk_level}</h3>
                <div className="inline-block px-4 py-1 rounded-full bg-white/60 backdrop-blur-md text-sm font-bold uppercase tracking-widest mb-8 border border-white/50">
                  Risk Score: <span className="text-black/80">{(result.risk_score * 100).toFixed(0)}%</span>
                </div>
              </div>
              
              <div className="bg-white/80 backdrop-blur-sm p-6 sm:p-8 rounded-2xl shadow-sm border border-white text-left">
                <div className="flex items-center mb-5 pb-4 border-b border-black/10">
                  <div className="p-2 bg-indigo-100 rounded-lg mr-4 shadow-inner">
                    <Info className="w-6 h-6 text-indigo-700" />
                  </div>
                  <h4 className="text-xl font-bold text-slate-800">Security Analysis</h4>
                </div>
                
                <div className="space-y-4">
                  {result.explanation.split(' | ').filter(Boolean).map((text, i) => (
                    <motion.p 
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 + (i * 0.1) }}
                      className="text-lg leading-relaxed text-slate-700 font-medium relative pl-5 before:content-[''] before:absolute before:left-0 before:top-3 before:w-2 before:h-2 before:bg-indigo-500 before:rounded-full"
                    >
                      {text.replace('AI Explanation: ', '').replace('Rules triggered: ', '').replace('Reputation warnings: ', '')}
                    </motion.p>
                  ))}
                </div>
                
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="mt-8 pt-6 border-t border-black/10"
                >
                  <span className="text-xs font-extrabold uppercase tracking-widest text-slate-500 mb-2 block">Recommendation</span>
                  <p className="font-bold text-2xl text-slate-900">{result.recommendation}</p>
                </motion.div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
