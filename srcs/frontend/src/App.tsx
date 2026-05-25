import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Login     from './pages/Login'
import Register  from './pages/Register'
import Dashboard from './pages/Dashboard'
import Home      from './pages/Home'
import Review    from './pages/Review'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

function GuestRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  return isAuthenticated ? <Navigate to="/" replace /> : <>{children}</>
}

export default function App() {
  return (
    <Routes>
      <Route path="/login"    element={<GuestRoute><Login /></GuestRoute>} />
      <Route path="/register" element={<GuestRoute><Register /></GuestRoute>} />

      <Route path="/"           element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/new"        element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/review/:id" element={<ProtectedRoute><Review /></ProtectedRoute>} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
