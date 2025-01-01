// src/types/auth.ts
export interface LoginFormData {
  email: string
  password: string
}

export interface RegisterFormData {
  email: string
  password: string
  full_name: string
  phone: string
  submit?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}
