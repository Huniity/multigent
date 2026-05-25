import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { authFetch } from '../utils/authFetch';

// Types
interface ReviewResult {
  bug_report:         string | null
  security_report:    string | null
  style_report:       string | null
  performance_report: string | null
  final_report:       string | null
  overall_score:      number | null
}

interface Review {
  id:           string
  source:       string
  label:        string
  score:        number | null
  created_at:   string
  completed_at: string | null
  result:       ReviewResult | null
}

// Sub-components
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

/**Shown while the initial fetch is in flight*/
function FetchingState() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-[#08080a] gap-4">
      <div className="w-2 h-2 rounded-full bg-[#aaef5a] animate-pulse" />
      <p className="text-sm text-[#787891]">Loading review…</p>
    </div>
  );
}

/**Shown when status === 'pending' — auto-polls every 10s*/
function PendingState({ onRefresh }: { onRefresh: () => void }) {
  const [countdown, setCountdown] = useState(10);

  useEffect(() => {
    const interval = setInterval(() => {
      setCountdown((c) => {
        if (c <= 1) { onRefresh(); return 10; }
        return c - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [onRefresh]);

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-[#08080a] text-center px-6">
      <div className="w-2 h-2 rounded-full bg-[#f8c354] animate-pulse mb-8" />
      <h2
        className="text-2xl font-bold text-[#f0ede5] mb-3"
        style={{ fontFamily: "'Syne', sans-serif" }}
      >
        Agents are still working.
      </h2>
      <p className="text-sm text-[#787891] mb-8 max-w-sm leading-relaxed">
        Your review is being processed. This page will check again automatically
        in {countdown}s, or you can check now.
      </p>
      <div className="flex items-center gap-4">
        <button
          onClick={onRefresh}
          className="bg-[#aaef5a] text-[#081400] text-xs font-medium tracking-widest uppercase py-3 px-7 cursor-pointer hover:opacity-85 transition-opacity"
        >
          Check now
        </button>
        <Link
          to="/"
          className="text-xs text-[#787891] hover:text-[#aaef5a] transition-colors"
        >
          ← Back to home
        </Link>
      </div>
    </div>
  );
}

/**Shown when result exists*/
function CompleteState({ review }: { review: Review }) {
  const result = review.result!
  const reports = [
    { label: 'Final Report',       content: result.final_report        },
    { label: 'Security',           content: result.security_report     },
    { label: 'Bugs',               content: result.bug_report          },
    { label: 'Performance',        content: result.performance_report  },
    { label: 'Style',              content: result.style_report        },
  ]
  const [tab, setTab] = useState(0)

  return (
    <div className="flex flex-col flex-1 bg-[#08080a] text-left">
      {/* Header */}
      <div className="border-b border-[#18181e] px-10 py-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Logo />
          <span className="text-[#28282e]">/</span>
          <span className="text-xs text-[#787891] tracking-widest uppercase">Review {review.id}</span>
        </div>
        <div className="flex items-center gap-6">
          {result.overall_score !== null && (
            <span className="text-xs text-[#787891]">
              Score:{' '}
              <span style={{ color: result.overall_score >= 80 ? '#aaef5a' : result.overall_score >= 60 ? '#f8c354' : '#f87171' }}
                className="font-bold">
                {result.overall_score}/100
              </span>
            </span>
          )}
          <Link to="/" className="text-xs text-[#787891] hover:text-[#aaef5a] transition-colors">← Dashboard</Link>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-[#18181e] px-10 gap-1">
        {reports.map((r, i) => (
          <button key={i} onClick={() => setTab(i)}
            className={[
              'py-3 px-5 text-xs tracking-widest border-b-2 transition-colors cursor-pointer bg-transparent',
              tab === i ? 'text-[#aaef5a] border-[#aaef5a]' : 'text-[#787891] border-transparent hover:text-[#a0a0b0]',
            ].join(' ')}>
            {r.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-10 py-8">
        <pre className="bg-[#060608] border border-[#18181e] p-5 text-xs text-[#e2dfda] font-mono leading-relaxed overflow-x-auto whitespace-pre-wrap text-left">
          {reports[tab].content || 'No output for this report.'}
        </pre>
      </div>
    </div>
  )
}


// Main component
export default function Review() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [review, setReview]   = useState<Review | null>(null);
  const [fetching, setFetching] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  async function fetchReview() {
    if (!id) { navigate('/'); return; }

    setFetching(true);
    setFetchError(null);

    try {
      const res = await authFetch(`/api/reviews/${id}/`);

      if (!res.ok) {
        const err = await res.json() as { detail?: string };
        setFetchError(err.detail ?? 'Failed to load review.');
        return;
      }

      const data = await res.json() as Review;
      setReview(data);
    } catch {
      setFetchError('Unable to connect to the server. Please try again.');
    } finally {
      setFetching(false);
    }
  }

  useEffect(() => { fetchReview(); }, [id]);

  // Render
  if (fetching && !review) return <FetchingState />;

  if (fetchError) {
    return (
      <div className="flex flex-col flex-1 items-center justify-center bg-[#08080a] text-center px-6">
        <p className="text-sm text-[#f87171] mb-6">{fetchError}</p>
        <Link to="/" className="text-xs text-[#aaef5a] underline">← Back to home</Link>
      </div>
    );
  }

  if (!review) return null;

  if (review.result === null) return <PendingState onRefresh={fetchReview} />;
  return <CompleteState review={review} />;
}