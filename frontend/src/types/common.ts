// src/types/common.ts
export interface APIResponse<T> {
  status: string
  message: string
  data?: T
  errors?: string[]
}

export interface PageResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
}
