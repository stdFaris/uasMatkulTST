// src/types/notification.ts
import { Booking } from './booking'

export enum NotificationType {
  BOOKING_REMINDER = 'booking_reminder',
  SCHEDULE_CHANGE = 'schedule_change',
  BOOKING_CONFIRMATION = 'booking_confirmation',
  PARTNER_UNAVAILABLE = 'partner_unavailable',
}

export interface Notification {
  id: number
  type: NotificationType
  message: string
  booking: Booking
  created_at: string
  is_read: boolean
}
