// src/types/partner.ts
import { MatchSortCriteria } from './enums'
export enum PartnerRole {
  PEMBANTU = 'pembantu',
  TUKANG_KEBUN = 'tukang_kebun',
  TUKANG_PIJAT = 'tukang_pijat',
}

export enum BookingType {
  HOURLY = 'hourly',
  DAILY = 'daily',
  MONTHLY = 'monthly',
}

export interface PartnerPricing {
  hourly_rate: number
  daily_rate: number
  monthly_rate: number
}

export interface MatchRequest {
  start_datetime: string
  kecamatan: string
  role: PartnerRole
  booking_type: BookingType
  filters: {
    role: PartnerRole
    min_rating: number
    min_experience: number
    max_hourly_rate: number | null
    specialization: string | null
    kecamatan: string
  }
  sort_by: MatchSortCriteria
}

export interface PartnerFilter {
  role?: string
  min_rating?: number
  min_experience?: number
  max_hourly_rate?: number
  specialization?: string
}

// src/types/partner.ts
export interface Partner {
  id: number
  full_name: string
  role: 'pembantu' | 'tukang_kebun' | 'tukang_pijat'
  experience_years: number
  rating: number
  total_reviews: number
  specializations: string[]
  pricing: {
    hourly_rate: number
    daily_rate: number
    monthly_rate: number
  }
  kecamatan: string
  is_available: boolean
  profile_image?: string
  languages: string[]
  profile_description?: string
}
