// src/pages/dashboard.tsx
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Calendar, Clock, DollarSign, Users, RefreshCw } from 'lucide-react'
import { useDashboard } from '@/hooks/useDashboard'
import { StatsCard } from '@/components/dashboard/stats-card'
import { UpcomingBookings } from '@/components/dashboard/upcoming-bookings'
import { RecommendedPartners } from '@/components/dashboard/recommended-partners'
import { formatPrice } from '@/lib/utils'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/button'
import { Notifications } from '@/components/dashboard/notifications'

export default function DashboardPage() {
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const { data, isLoading, error, refresh } = useDashboard()

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
    }
  }, [isAuthenticated, navigate])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen space-y-4">
        <div className="text-lg text-error-500">{error}</div>
        <Button onClick={refresh} variant="outline">
          <RefreshCw className="w-4 h-4 mr-2" />
          Try Again
        </Button>
      </div>
    )
  }

  if (!data) return null

  const { stats, upcoming_bookings, recommended_partners, customer } = data

  return (
    <div className="container mx-auto p-4 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex flex-col space-y-2">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome back, {customer.full_name}
          </p>
        </div>
        <Button onClick={refresh} variant="outline" size="sm">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <StatsCard
          title="Total Bookings"
          value={stats.total_bookings}
          icon={<Calendar className="h-4 w-4 text-muted-foreground" />}
        />
        <StatsCard
          title="Active Bookings"
          value={stats.active_bookings}
          icon={<Clock className="h-4 w-4 text-muted-foreground" />}
        />
        <StatsCard
          title="Total Amount Spent"
          value={formatPrice(stats.total_spent)}
          icon={<DollarSign className="h-4 w-4 text-muted-foreground" />}
        />
        <StatsCard
          title="Completed Services"
          value={stats.completed_bookings}
          icon={<Users className="h-4 w-4 text-muted-foreground" />}
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <UpcomingBookings bookings={upcoming_bookings} onRefresh={refresh} />
        <RecommendedPartners
          partners={recommended_partners}
          onRefresh={refresh}
        />
        <Notifications
          notifications={data.recent_notifications}
          onRefresh={refresh}
        />
      </div>
    </div>
  )
}
