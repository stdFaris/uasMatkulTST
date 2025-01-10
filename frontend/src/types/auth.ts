// src/types/auth.ts
export interface UserAuth {
  email: string
  password: string
}

export interface Token {
  access_token: string
  refresh_token: string
}

export interface CustomerCreate {
  email: string
  password: string
  full_name: string
  phone: string
  kecamatan: string
}

export interface User {
  id: string
  email: string
  name: string
  kecamatan: string
}
