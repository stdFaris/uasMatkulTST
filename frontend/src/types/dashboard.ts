import { Booking } from './booking'
import { Partner } from './partner'
import { Customer } from './customer'
import { Notification } from './notification'

interface DashboardStats {
  total_bookings: number
  active_bookings: number
  completed_bookings: number
  cancelled_bookings: number
  total_spent: number
}

export interface CustomerDashboard {
  customer: Customer
  upcoming_bookings: Booking[]
  recommended_partners: Partner[]
  stats: DashboardStats
  active_bookings: number
  recent_notifications: Notification[]
}
