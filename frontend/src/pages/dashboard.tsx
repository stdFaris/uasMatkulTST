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
        <div className="text-lg font-medium text-primary-700">Loading...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-primary-50 to-white space-y-4">
        <div className="text-lg text-error-600 font-medium">{error}</div>
        <Button
          onClick={refresh}
          variant="outline"
          className="hover:bg-primary-50"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Try Again
        </Button>
      </div>
    )
  }

  if (!data) return null

  const { stats, upcoming_bookings, recommended_partners, customer } = data

  return (
    <div className="min-h-screen">
      <div className="container mx-auto px-4 py-8 space-y-8">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold text-primary-900">Dashboard</h1>
            <p className="text-primary-600">
              Welcome back, {customer.full_name}
            </p>
          </div>
          <Button
            onClick={refresh}
            variant="outline"
            size="sm"
            className="hover:bg-primary-50"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
          <StatsCard
            title="Total Bookings"
            value={stats.total_bookings}
            icon={<Calendar className="h-5 w-5 text-primary-600" />}
          />
          <StatsCard
            title="Active Bookings"
            value={stats.active_bookings}
            icon={<Clock className="h-5 w-5 text-primary-600" />}
          />
          <StatsCard
            title="Total Amount Spent"
            value={formatPrice(stats.total_spent)}
            icon={<DollarSign className="h-5 w-5 text-primary-600" />}
          />
          <StatsCard
            title="Completed Services"
            value={stats.completed_bookings}
            icon={<Users className="h-5 w-5 text-primary-600" />}
          />
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
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
    </div>
  )
}
