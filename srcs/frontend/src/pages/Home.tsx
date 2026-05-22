import { useState, useEffect, type FormEvent, type ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

// Constants
const LOADING_MESSAGES = [
  'Fetching repository contents…',
  'Our security agent is reviewing your code…',
  'Our performance agent is analysing efficiency…',
  'Our quality agent is checking maintainability…',
  'Agents are cross-referencing findings…',
  'Compiling the revised output…',
];

// Validation
function isValidGithubUrl(raw: string): boolean {
  try {
    const { hostname, pathname } = new URL(raw.trim());
    const isGithub = hostname === 'github.com' || hostname === 'www.github.com';
    // Require at least owner/repo in the path
    const segments = pathname.split('/').filter(Boolean);
    return isGithub && segments.length >= 2;
  } catch {
    return false;
  }
}

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
  const accessToken = useAuthStore((s) => s.accessToken);

  const [url, setUrl]             = useState('');
  const [urlError, setUrlError]   = useState<string | null>(null);
  const [apiError, setApiError]   = useState<string | null>(null);
  const [loading, setLoading]     = useState(false);
  const [step, setStep]           = useState(0);
  const [msgVisible, setMsgVisible] = useState(true);

  // Cycles loading messages: show for 1800 ms, fade out for 350 ms, advance
  useEffect(() => {
    if (!loading) return;

    setMsgVisible(true);

    const showTimer = setTimeout(() => {
      setMsgVisible(false);

      const advanceTimer = setTimeout(() => {
        setStep((s) => Math.min(s + 1, LOADING_MESSAGES.length - 1));
        setMsgVisible(true);
      }, 350);

      return () => clearTimeout(advanceTimer);
    }, 1800);

    return () => clearTimeout(showTimer);
  }, [loading, step]);

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    setUrl(e.target.value);
    setUrlError(null);
    setApiError(null);
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();

    // Client-side validation
    if (!url.trim()) {
      setUrlError('Repository URL is required.');
      return;
    }
    if (!isValidGithubUrl(url)) {
      setUrlError(
        'Enter a valid GitHub repository URL (e.g. https://github.com/owner/repo).'
      );
      return;
    }

    setLoading(true);
    setStep(0);
    setMsgVisible(true);
    setApiError(null);

    try {
      const res = await fetch('/api/v1/reviews/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken ?? ''}`,
        },
        body: JSON.stringify({ url: url.trim() }),
      });

      // 202 Accepted — review is queued, response contains the review ID
      if (res.status === 202 || res.ok) {
        const data = await res.json() as { id: string };
        navigate(`/review/${data.id}`);
        return;
      }

      const err = await res.json() as { detail?: string };
      setApiError(err.detail ?? 'Something went wrong. Please try again.');
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
          Submit a repository<br />for review.
        </h1>
        <p className="text-sm text-[#787891] leading-relaxed mb-10">
          Paste a GitHub repository URL. Multiple agents will audit the code
          simultaneously and produce a unified revised output.
        </p>

        <form onSubmit={handleSubmit} noValidate className="space-y-5">

          {/*API-level error*/}
          {apiError && (
            <div className="text-xs text-[#f87171] bg-[#2a1010] border border-[#f87171]/30 px-4 py-3">
              {apiError}
            </div>
          )}

          {/*URL field*/}
          <div className="space-y-2">
            <label
              htmlFor="url"
              className="block text-[9px] tracking-widest uppercase text-[#787891]"
            >
              GitHub repository URL
            </label>
            <input
              id="url"
              type="url"
              name="url"
              placeholder="https://github.com/owner/repository"
              value={url}
              onChange={handleChange}
              autoComplete="off"
              spellCheck={false}
              className={[
                'w-full bg-[#101014] text-[#e2dfda] text-sm px-3.5 py-2.5 outline-none',
                'placeholder:text-[#35333e] font-mono transition-colors border',
                'focus:border-[#aaef5a]',
                urlError ? 'border-[#f87171]' : 'border-[#20202a]',
              ].join(' ')}
            />
            {urlError && (
              <span className="block text-[11px] text-[#f87171]">{urlError}</span>
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
            <span className="text-[11px] text-[#30303e]">2 agents · async</span>
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