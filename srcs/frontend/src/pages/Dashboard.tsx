import { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

interface ReviewResult {
  overall_score: number | null
}

interface Review {
  id: number
  source: string
  label: string
  score: number | null
  created_at: string
  completed_at: string | null
  result: ReviewResult | null
}

interface User {
  id: number
  username: string
  email: string
}

function scoreColor(n: number) {
  if (n >= 80) return '#aaef5a'
  if (n >= 60) return '#f8c354'
  return '#f87171'
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function Logo() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 9 }}>
      <div style={{ width: 8, height: 8, background: '#aaef5a', borderRadius: '50%' }} />
      <span style={{ fontFamily: "'Syne', sans-serif", fontSize: 14, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase' as const, color: '#f0ede5' }}>
        Multigent
      </span>
    </div>
  )
}

export default function Dashboard() {
  const navigate = useNavigate()
  const location = useLocation()
  const accessToken = useAuthStore(s => s.accessToken)
  const clearTokens = useAuthStore(s => s.clearTokens)

  const [reviews, setReviews] = useState<Review[]>([])
  const [user, setUser]       = useState<User | null>(null)

  useEffect(() => {
    const headers = { Authorization: `Bearer ${accessToken ?? ''}` }
    Promise.all([
      fetch('/api/reviews/all/', { headers }).then(r => r.json()),
      fetch('/api/auth/me/',     { headers }).then(r => r.json()),
    ]).then(([reviewsData, userData]) => {
      setReviews(Array.isArray(reviewsData) ? reviewsData : [])
      setUser(userData)
    })
  }, [])

  function signOut() {
    clearTokens()
    navigate('/login')
  }

  const scores = reviews
    .map(r => r.result?.overall_score)
    .filter((s): s is number => s !== null)
  const avgScore = scores.length > 0
    ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
    : null

  const navItems = [
    { label: 'Reviews',    icon: '▦', to: '/'    },
    { label: 'New review', icon: '+', to: '/new' },
  ]

  const s = {
    wrap:    { display: 'flex', minHeight: '100vh', background: '#08080a', color: '#e2dfda', fontFamily: "'JetBrains Mono', monospace", fontSize: 13 } as const,
    sidebar: { width: 220, background: '#0b0b0e', borderRight: '1px solid #18181e', display: 'flex', flexDirection: 'column', position: 'sticky', top: 0, height: '100vh' } as const,
    main:    { flex: 1, padding: '2.5rem 3rem', overflowY: 'auto' } as const,
    navLink: (active: boolean) => ({
      display: 'flex', alignItems: 'center', gap: 10,
      padding: '10px 24px', textDecoration: 'none',
      color: active ? '#aaef5a' : '#787891',
      borderLeft: `2px solid ${active ? '#aaef5a' : 'transparent'}`,
      fontSize: 11, letterSpacing: '0.06em', textTransform: 'uppercase' as const,
      transition: 'color 0.15s',
    }),
    card: {
      background: '#0d0d11', border: '1px solid #18181e',
      padding: '18px 22px', cursor: 'pointer',
      display: 'grid', gridTemplateColumns: '1fr auto',
      alignItems: 'center', gap: 16, marginBottom: 10,
    } as const,
    stat: { background: '#0d0d11', border: '1px solid #18181e', padding: '16px 20px' } as const,
    tag:  { background: '#18181e', color: '#787891', fontSize: 9, letterSpacing: '0.08em', textTransform: 'uppercase' as const, padding: '3px 8px' } as const,
    monoLabel: { fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase' as const, color: '#787891', display: 'block', marginBottom: 8 } as const,
  }

  return (
    <div style={s.wrap}>

      {/* Sidebar */}
      <div style={s.sidebar}>
        <div style={{ padding: '2rem 1.5rem 2.75rem' }}>
          <Logo />
        </div>

        <nav style={{ flex: 1 }}>
          {navItems.map(item => (
            <Link key={item.to} to={item.to} style={s.navLink(location.pathname === item.to)}>
              <span style={{ fontSize: 13 }}>{item.icon}</span>
              {item.label}
            </Link>
          ))}
        </nav>

        <div style={{ borderTop: '1px solid #18181e', padding: '1rem 1.5rem 1.5rem' }}>
          <div style={{ fontSize: 9, color: '#787891', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 4 }}>Signed in as</div>
          <div style={{ color: '#787891', fontSize: 11, marginBottom: 14 }}>{user?.username ?? '—'}</div>
          <button onClick={signOut} style={{ background: 'none', border: 'none', color: '#787891', fontSize: 11, cursor: 'pointer', padding: 0, fontFamily: 'inherit' }}>
            ↖ Sign out
          </button>
        </div>
      </div>

      {/* Main */}
      <div style={s.main}>

        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 32 }}>
          <div>
            <h1 style={{ fontFamily: "'Syne', sans-serif", fontSize: 30, fontWeight: 800, color: '#f0ede5', marginBottom: 4 }}>
              Code Reviews
            </h1>
            <p style={{ color: '#787891', fontSize: 11 }}>
              {reviews.length} review{reviews.length !== 1 ? 's' : ''} · 5 agents per review
            </p>
          </div>
          <Link to="/new" style={{ border: '1px solid #20202a', color: '#787891', fontSize: 11, letterSpacing: '0.06em', padding: '10px 20px', textDecoration: 'none', textTransform: 'uppercase' }}>
            + New review
          </Link>
        </div>

        {/* Stats */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, marginBottom: 32 }}>
          {[
            { label: 'Avg. score', value: avgScore !== null ? String(avgScore) : '—', unit: '/100'        },
            { label: 'Reviews',    value: String(reviews.length),                      unit: 'total'       },
            { label: 'Agents',     value: '5',                                         unit: 'per review'  },
          ].map(stat => (
            <div key={stat.label} style={s.stat}>
              <span style={s.monoLabel}>{stat.label}</span>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 5 }}>
                <span style={{ fontFamily: "'Syne', sans-serif", fontSize: 30, fontWeight: 800, color: '#f0ede5' }}>{stat.value}</span>
                <span style={{ color: '#787891', fontSize: 11 }}>{stat.unit}</span>
              </div>
            </div>
          ))}
        </div>

        {/* List */}
        <span style={s.monoLabel}>Recent reviews</span>

        {reviews.length === 0 ? (
          <p style={{ color: '#787891', fontSize: 12, paddingTop: 12 }}>
            No reviews yet.{' '}
            <Link to="/new" style={{ color: '#aaef5a' }}>Submit your first one.</Link>
          </p>
        ) : (
          reviews.map(r => {
            const score = r.result?.overall_score ?? null
            return (
              <div key={r.id} style={s.card} onClick={() => navigate(`/review/${r.id}`)}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                    <span style={{ color: '#f0ede5', fontSize: 14, fontWeight: 500 }}>{r.label}</span>
                    <span style={s.tag}>{r.source === 'pasted_code' ? 'Pasted' : 'File'}</span>
                    {r.result === null && <span style={{ ...s.tag, color: '#f8c354' }}>Pending</span>}
                  </div>
                  <div style={{ color: '#787891', fontSize: 11 }}>{formatDate(r.created_at)} · 5 agents</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  {score !== null ? (
                    <>
                      <div style={{ fontFamily: "'Syne', sans-serif", fontSize: 22, fontWeight: 700, color: scoreColor(score) }}>{score}</div>
                      <div style={{ fontSize: 9, color: '#787891', textTransform: 'uppercase', letterSpacing: '0.08em' }}>score</div>
                    </>
                  ) : (
                    <div style={{ color: '#30303e', fontSize: 20 }}>—</div>
                  )}
                </div>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}
