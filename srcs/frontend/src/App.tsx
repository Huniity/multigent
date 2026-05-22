import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'

// Guards
/**Redirects unauthenticated users to /login*/
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

/**Redirects already-authenticated users away from auth pages*/
function GuestRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  return isAuthenticated ? <Navigate to="/" replace /> : <>{children}</>
}

// Review placeholder (Replace with pages/Review.tsx once that task is implemented.)
function ReviewPlaceholder() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-[#08080a] text-[#787891] text-sm">
      Review page — coming soon.
    </div>
  )
}

// App
export default function App() {
  return (
    <Routes>
      <Route path="/login"    element={<GuestRoute><Login /></GuestRoute>} />
      <Route path="/register" element={<GuestRoute><Register /></GuestRoute>} />

      <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />

      <Route
        path="/review/:id"
        element={<ProtectedRoute><ReviewPlaceholder /></ProtectedRoute>}
      />

      {/* Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}