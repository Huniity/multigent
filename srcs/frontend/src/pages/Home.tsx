import { useState, useEffect, type FormEvent, type ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { authFetch } from '../utils/authFetch';

// Constants
const LOADING_MESSAGES = [
  'Parsing your code structure…',
  'Our security agent is reviewing your code…',
  'Our performance agent is analysing efficiency…',
  'Our quality agent is checking maintainability…',
  'Agents are cross-referencing findings…',
  'Compiling the revised output…',
];

// Loading screen
function LoadingScreen({ step, visible }: { step: number; visible: boolean }) {
  const progress = ((step + 1) / LOADING_MESSAGES.length) * 100;

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-[#08080a]">
      <Logo />

      <div className="mt-12 mb-8 w-2 h-2 rounded-full bg-[#aaef5a] animate-pulse" />

      <p
        className="text-sm text-[#e2dfda] text-center min-h-6 px-6 transition-opacity duration-300"
        style={{ opacity: visible ? 1 : 0 }}
      >
        {LOADING_MESSAGES[step]}
      </p>

      <div className="w-72 h-px bg-[#18181e] mt-8 relative overflow-hidden">
        <div
          className="absolute inset-y-0 left-0 bg-[#aaef5a] transition-[width] duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

      <p className="mt-4 text-[10px] text-[#30303e] tracking-widest">
        {step + 1} / {LOADING_MESSAGES.length}
      </p>
    </div>
  );
}

// Main component
export default function Home() {
  const navigate = useNavigate();

  const [code, setCode] = useState('');
  const [codeError, setCodeError] = useState<string | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [msgVisible, setMsgVisible] = useState(true);

  // Cycles loading messages: show for 1800ms, fade out for 350ms, advance
  useEffect(() => {
    if (!loading) return;

    setMsgVisible(true);

    const showTimer = setTimeout(() => {
      setMsgVisible(false);

      const advanceTimer = setTimeout(() => {
        setStep((s) => Math.min(s + 1, LOADING_MESSAGES.length - 1));
        setMsgVisible(true);
      }, 450);

      return () => clearTimeout(advanceTimer);
    }, 3000);

    return () => clearTimeout(showTimer);
  }, [loading, step]);

  function handleChange(e: ChangeEvent<HTMLTextAreaElement>) {
    setCode(e.target.value);
    setCodeError(null);
    setApiError(null);
  }

  async function pollUntilComplete(id: string): Promise<void> {
    while (true) {
      await new Promise((resolve) => setTimeout(resolve, 5000));
      const res = await authFetch(`/api/reviews/${id}/`);
      if (!res.ok) return;
      const data = await res.json() as { result: object | null };
      if (data.result !== null) return;
    }
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();

    if (!code.trim()) {
      setCodeError('Please paste your code before submitting.');
      return;
    }

    setLoading(true);
    setStep(0);
    setMsgVisible(true);
    setApiError(null);

    try {
      const res = await authFetch('/api/reviews/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code.trim() }),
      });

      if (!res.ok) {
        const err = await res.json() as { detail?: string };
        setApiError(err.detail ?? 'Something went wrong. Please try again.');
        return;
      }

      const data = await res.json() as { id: string };
      await pollUntilComplete(data.id);
      navigate(`/review/${data.id}`);
    } catch {
      setApiError('Unable to connect to the server. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <LoadingScreen step={step} visible={msgVisible} />;
  }



  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-[#08080a] p-8 text-left">
      <div className="w-full max-w-xl">

        <div className="mb-10">
          <Logo />
        </div>

        <h1
          className="text-4xl font-bold text-[#f0ede5] leading-tight mb-4"
          style={{ fontFamily: "'Syne', sans-serif" }}
        >
          Submit code<br />for review.
        </h1>
        <p className="text-sm text-[#787891] leading-relaxed mb-10">
          Paste a code snippet. Multiple agents will audit it simultaneously
          and produce a unified revised output.
        </p>

        <form onSubmit={handleSubmit} noValidate className="space-y-5">

          {/* API-level error */}
          {apiError && (
            <div className="text-xs text-[#f87171] bg-[#2a1010] border border-[#f87171]/30 px-4 py-3">
              {apiError}
            </div>
          )}

          {/* Code textarea */}
          <div className="space-y-2">
            <label
              htmlFor="code"
              className="block text-[9px] tracking-widest uppercase text-[#787891]"
            >
              Code snippet
            </label>
            <textarea
              id="code"
              name="code"
              placeholder={"# Paste your code here…\n\ndef example():\n    pass"}
              value={code}
              onChange={handleChange}
              spellCheck={false}
              rows={16}
              className={[
                'w-full bg-[#101014] text-[#e2dfda] text-sm px-3.5 py-2.5 outline-none',
                'placeholder:text-[#35333e] font-mono transition-colors border resize-y',
                'focus:border-[#aaef5a]',
                codeError ? 'border-[#f87171]' : 'border-[#20202a]',
              ].join(' ')}
            />
            {codeError && (
              <span className="block text-[11px] text-[#f87171]">{codeError}</span>
            )}
          </div>

          <div className="h-px bg-[#18181e]" />

          <div className="flex items-center gap-5">
            <button
              type="submit"
              className="bg-[#aaef5a] text-[#081400] text-xs font-medium tracking-widest uppercase py-3 px-7 cursor-pointer hover:opacity-85 active:opacity-70 transition-opacity"
            >
              →&nbsp;&nbsp;Submit for review
            </button>
            <span className="text-[11px] text-[#f0ede5]">5 agents</span>
            <span className="text-[11px] text-[#aaef5a]">Bug Report Agent</span>
            <span className="text-[11px] text-[#aaef5a]">Security Agent</span>
            <span className="text-[11px] text-[#aaef5a]">Performance Agent</span>
            <span className="text-[11px] text-[#aaef5a]">Quality Agent</span>
            <span className="text-[11px] text-[#aaef5a]">Style Agent</span>

          </div>

        </form>
      </div>
    </div>
  );
}

// Shared
function Logo() {
  return (
    <div className="flex items-center gap-2">
      <div className="w-2 h-2 rounded-full bg-[#aaef5a]" />
      <span
        className="text-sm font-bold tracking-widest uppercase text-[#f0ede5]"
        style={{ fontFamily: "'Syne', sans-serif" }}
      >
        Multigent
      </span>
    </div>
  );
}