// src/types/customer.ts
export enum UserRole {
  CUSTOMER = 'customer',
  PARTNER = 'partner',
  ADMIN = 'admin',
}

export enum BookingStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
  TERMINATED = 'terminated',
}

export enum BookingType {
  HOURLY = 'hourly',
  DAILY = 'daily',
  MONTHLY = 'monthly',
}

export interface Customer {
  id: number
  email: string
  full_name: string
  phone: string
  is_active: boolean
  role: UserRole
  profile_image?: string
  created_at: string
  updated_at: string
}

export interface Review {
  id: number
  booking_id: number
  customer_id: number
  partner_id: number
  rating: number
  comment?: string
  created_at: string
}

export interface Booking {
  id: number
  partner_id: number
  booking_type: 'hourly' | 'daily' | 'monthly'
  status:
    | 'pending'
    | 'confirmed'
    | 'in_progress'
    | 'completed'
    | 'cancelled'
    | 'terminated'
  start_datetime: string
  end_datetime: string
  duration_hours?: number
  total_price: number
  notes?: string
  partner: {
    full_name: string
    profile_image?: string
  }
}
