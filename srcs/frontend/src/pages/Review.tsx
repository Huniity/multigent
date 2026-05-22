import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

// Types
type ReviewStatus = 'pending' | 'complete' | 'failed';

interface AgentReport {
  name: string;
  blurb: string;
}

interface Review {
  id: string;
  status: ReviewStatus;
  created_at: string;
  revised_code?: string;
  agents?: AgentReport[];
  readme?: string;
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

/**Shown when status === 'failed'*/
function FailedState() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-[#08080a] text-center px-6">
      <div className="w-2 h-2 rounded-full bg-[#f87171] mb-8" />
      <h2
        className="text-2xl font-bold text-[#f0ede5] mb-3"
        style={{ fontFamily: "'Syne', sans-serif" }}
      >
        Review failed.
      </h2>
      <p className="text-sm text-[#787891] mb-8 max-w-sm leading-relaxed">
        One or more agents were unreachable or encountered an error while
        processing your submission. Please try submitting again.
      </p>
      <Link
        to="/"
        className="bg-[#aaef5a] text-[#081400] text-xs font-medium tracking-widest uppercase py-3 px-7 hover:opacity-85 transition-opacity"
      >
        ← Submit again
      </Link>
    </div>
  );
}

/**Shown when status === 'complete'*/
function CompleteState({ review }: { review: Review }) {
  const [tab, setTab] = useState<'code' | 'readme'>('code');

  return (
    <div className="flex flex-col flex-1 bg-[#08080a] text-left">
      {/*Header*/}
      <div className="border-b border-[#18181e] px-10 py-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Logo />
          <span className="text-[#28282e]">/</span>
          <span className="text-xs text-[#787891] tracking-widest uppercase">
            Review {review.id}
          </span>
        </div>
        <Link
          to="/"
          className="text-xs text-[#787891] hover:text-[#aaef5a] transition-colors"
        >
          ← New review
        </Link>
      </div>

      {/*Tabs*/}
      <div className="flex border-b border-[#18181e] px-10 gap-1">
        {([
          { id: 'code',   label: 'Revised code'  },
          { id: 'readme', label: 'Agent README'   },
        ] as const).map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={[
              'py-3 px-5 text-xs tracking-widest border-b-2 transition-colors cursor-pointer bg-transparent',
              tab === t.id
                ? 'text-[#aaef5a] border-[#aaef5a]'
                : 'text-[#787891] border-transparent hover:text-[#a0a0b0]',
            ].join(' ')}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/*Content*/}
      <div className="flex-1 overflow-y-auto px-10 py-8">

        {/*Revised code tab*/}
        {tab === 'code' && (
          <div>
            <p className="text-[9px] tracking-widest uppercase text-[#787891] mb-4">
              Final output — revised by {review.agents?.length ?? 0} agents
            </p>
            <pre
              className="bg-[#060608] border border-[#18181e] p-5 text-xs text-[#90d860] font-mono leading-relaxed overflow-x-auto whitespace-pre text-left"
            >
              {review.revised_code}
            </pre>
          </div>
        )}

        {/*Agent README tab*/}
        {tab === 'readme' && (
          <div className="max-w-2xl">
            {/* Per-agent blurbs */}
            {review.agents && review.agents.length > 0 && (
              <div className="mb-10">
                <p className="text-[9px] tracking-widest uppercase text-[#787891] mb-6">
                  Agent reports
                </p>
                {review.agents.map((agent, i) => (
                  <div
                    key={i}
                    className="border border-[#18181e] bg-[#0d0d11] px-6 py-5 mb-4"
                  >
                    <p
                      className="text-sm font-bold text-[#c0bcb5] mb-3"
                      style={{ fontFamily: "'Syne', sans-serif" }}
                    >
                      {agent.name}
                    </p>
                    <p className="text-xs text-[#787891] leading-relaxed text-left">
                      {agent.blurb}
                    </p>
                  </div>
                ))}
              </div>
            )}

            {/*Collective README*/}
            {review.readme && (
              <div>
                <p className="text-[9px] tracking-widest uppercase text-[#787891] mb-4">
                  Collective README
                </p>
                <pre
                  className="bg-[#060608] border border-[#18181e] p-5 text-xs text-[#e2dfda] font-mono leading-relaxed overflow-x-auto whitespace-pre-wrap text-left"
                >
                  {review.readme}
                </pre>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}

// Main component
export default function Review() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const accessToken = useAuthStore((s) => s.accessToken);

  const [review, setReview]   = useState<Review | null>(null);
  const [fetching, setFetching] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  async function fetchReview() {
    if (!id) { navigate('/'); return; }

    setFetching(true);
    setFetchError(null);

    try {
      const res = await fetch(`/api/v1/reviews/${id}/`, {
        headers: { Authorization: `Bearer ${accessToken ?? ''}` },
      });

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

  if (review.status === 'pending') return <PendingState onRefresh={fetchReview} />;
  if (review.status === 'failed')  return <FailedState />;
  return <CompleteState review={review} />;
}