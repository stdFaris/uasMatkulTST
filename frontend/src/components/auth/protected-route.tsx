import { useEffect } from 'react'
import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/hooks/useAuth'
import { getAccessToken } from '@/lib/utils'

export function ProtectedRoute() {
  const { isAuthenticated, setIsAuthenticated } = useAuthStore()
  const location = useLocation()

  useEffect(() => {
    const token = getAccessToken()
    setIsAuthenticated(!!token)
  }, [setIsAuthenticated])

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <Outlet />
}
