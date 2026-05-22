import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import Review from './pages/Review'

// Guards
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

function GuestRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  return isAuthenticated ? <Navigate to="/" replace /> : <>{children}</>
}

// App (to re-add: <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
// and <Route path="/review/:id" element={<ProtectedRoute><Review /></ProtectedRoute>} /> )
export default function App() {
  return (
    <Routes>
      <Route path="/login"    element={<GuestRoute><Login /></GuestRoute>} />
      <Route path="/register" element={<GuestRoute><Register /></GuestRoute>} />

      <Route path="/"           element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/review/:id" element={<ProtectedRoute><Review /></ProtectedRoute>} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}