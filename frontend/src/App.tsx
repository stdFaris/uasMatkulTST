import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { ProtectedRoute } from '@/components/auth/protected-route'
import { MainLayout } from './components/layout/main-layout'
import LoginPage from './pages/login'
import RegisterPage from './pages/register'
import DashboardPage from './pages/dashboard'
import { PartnersPage } from './pages/partners'
import { useAuthStore } from '@/hooks/useAuth'
import { getAccessToken } from '@/lib/utils'
import PartnerDetailsPage from './pages/partnerDetailsPage'

export default function App() {
  const { setIsAuthenticated, isAuthenticated, fetchUser } = useAuthStore()

  // Effect untuk cek token
  useEffect(() => {
    const token = getAccessToken()
    setIsAuthenticated(!!token)
  }, [setIsAuthenticated])

  useEffect(() => {
    const loadUser = async () => {
      if (isAuthenticated) {
        try {
          await fetchUser()
        } catch (error) {
          console.error('Failed to fetch user:', error)
        }
      }
    }

    loadUser()
  }, [isAuthenticated, fetchUser])

  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected Routes */}
        <Route element={<MainLayout />}>
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/partners" element={<PartnersPage />} />
            <Route path="/partners/:id" element={<PartnerDetailsPage />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Route>
        </Route>

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
