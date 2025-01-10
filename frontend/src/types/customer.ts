// src/types/customer.ts
import { PartnerRole, BookingType } from './partner'
export interface CustomerPreferences {
  preferred_partner_roles: PartnerRole[]
  preferred_booking_type?: BookingType
  preferred_languages?: string[]
  max_price_per_hour?: number
  preferred_kecamatan?: string
}

export interface Customer {
  id: number
  email: string
  full_name: string
  phone: string
  kecamatan: string
  preferences?: CustomerPreferences
  created_at: string
}
