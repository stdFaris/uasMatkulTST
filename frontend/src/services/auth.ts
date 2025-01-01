// src/services/auth.ts
import axios from 'axios'
import { LoginFormData, RegisterFormData, AuthResponse } from '@/types/auth'

const API_URL = import.meta.env.VITE_API_URL

export const login = async (data: LoginFormData): Promise<AuthResponse> => {
  const formData = new FormData()
  formData.append('username', data.email)
  formData.append('password', data.password)

  const response = await axios.post(`${API_URL}/api/auth/token`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  const token = response.data
  localStorage.setItem('token', token.access_token)
  return token
}

export const register = async (data: RegisterFormData): Promise<void> => {
  await axios.post(`${API_URL}/api/customers`, data)
}

export const logout = (): void => {
  localStorage.removeItem('token')
}
