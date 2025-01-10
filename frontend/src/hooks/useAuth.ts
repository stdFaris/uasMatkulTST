// src/hooks/useAuth.ts
import { create } from 'zustand'
import { useNavigate } from 'react-router-dom'
import axiosClient from '@/lib/axios-client'
import { UserAuth, Token, CustomerCreate, User } from '@/types/auth'
import { setTokens, clearTokens } from '@/lib/utils'

interface AuthState {
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  user: User | null
  login: (credentials: UserAuth) => Promise<void>
  register: (data: CustomerCreate) => Promise<void>
  logout: () => void
  setIsAuthenticated: (value: boolean) => void
  fetchUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  isLoading: false,
  error: null,
  user: null,
  setIsAuthenticated: (value: boolean) => set({ isAuthenticated: value }),
  fetchUser: async () => {
    try {
      set({ isLoading: true, error: null })
      const response = await axiosClient.get<User>('/auth/me')
      set({ user: response.data, isLoading: false })
    } catch (error: any) {
      set({
        error: error.response?.data?.message || 'Failed to fetch user data',
        isLoading: false,
      })
      throw error
    }
  },
  login: async (credentials: UserAuth) => {
    try {
      set({ isLoading: true, error: null })
      const response = await axiosClient.post<Token>('/auth/login', credentials)
      const { access_token, refresh_token } = response.data
      setTokens(access_token, refresh_token)

      // Fetch user data after successful login
      const userResponse = await axiosClient.get<User>('/auth/me')
      set({
        isAuthenticated: true,
        isLoading: false,
        user: userResponse.data,
      })
    } catch (error: any) {
      set({
        error:
          error.response?.data?.message || 'An error occurred during login',
        isLoading: false,
      })
      throw error
    }
  },
  register: async (data: CustomerCreate) => {
    try {
      set({ isLoading: true, error: null })
      await axiosClient.post('/customers/register', data)
      const response = await axiosClient.post<Token>('/auth/login', {
        email: data.email,
        password: data.password,
      })
      const { access_token, refresh_token } = response.data
      setTokens(access_token, refresh_token)

      // Fetch user data after successful registration
      const userResponse = await axiosClient.get<User>('/auth/me')
      set({
        isAuthenticated: true,
        isLoading: false,
        user: userResponse.data,
      })
    } catch (error: any) {
      set({
        error:
          error.response?.data?.message ||
          'An error occurred during registration',
        isLoading: false,
      })
      throw error
    }
  },
  logout: () => {
    clearTokens()
    set({ isAuthenticated: false, user: null })
  },
}))

export const useAuth = () => {
  const navigate = useNavigate()
  const auth = useAuthStore()

  const login = async (credentials: UserAuth) => {
    try {
      await auth.login(credentials)
      navigate('/dashboard')
    } catch (error) {
      // Error handling is done in the store
    }
  }

  const register = async (data: CustomerCreate) => {
    try {
      await auth.register(data)
      navigate('/dashboard')
    } catch (error) {
      // Error handling is done in the store
    }
  }

  const logout = () => {
    auth.logout()
    navigate('/login')
  }

  return {
    isAuthenticated: auth.isAuthenticated,
    isLoading: auth.isLoading,
    error: auth.error,
    user: auth.user,
    login,
    register,
    logout,
    fetchUser: auth.fetchUser,
  }
}
