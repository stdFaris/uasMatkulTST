// src/types/booking.ts
import { Partner } from './partner'

export enum BookingType {
  HOURLY = 'hourly',
  DAILY = 'daily',
  MONTHLY = 'monthly',
}

export enum BookingStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  CANCELLED = 'cancelled',
  COMPLETED = 'completed',
}

export interface Booking {
  id: number
  partner_id: number
  type: BookingType
  start_datetime: string
  end_datetime: string
  status: BookingStatus
  total_price: number
  notes?: string
  partner: Partner
}

export interface BookingCreate {
  partner_id: number
  type: BookingType
  start_datetime: string
  end_datetime: string
  notes?: string
}

export interface BookingCancel {
  reason: string
  cancellation_time: string
}
