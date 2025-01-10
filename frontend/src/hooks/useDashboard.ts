// src/hooks/useDashboard.ts
import { create } from 'zustand'
import { useEffect } from 'react'
import axiosClient from '@/lib/axios-client'
import type { CustomerDashboard } from '@/types/dashboard'
import { PartnerRole } from '@/types/enums'

interface DashboardState {
  data: CustomerDashboard | null
  isLoading: boolean
  error: string | null
  fetchDashboard: () => Promise<void>
}

const useDashboardStore = create<DashboardState>((set) => ({
  data: null,
  isLoading: false,
  error: null,
  fetchDashboard: async (roleFilter?: PartnerRole[]) => {
    try {
      set({ isLoading: true, error: null })

      const queryParams = roleFilter?.length
        ? `?${roleFilter.map((role) => `role_filter=${role}`).join('&')}`
        : ''

      const dashboardResponse = await axiosClient.get<CustomerDashboard>(
        `/customers/dashboard${queryParams}`
      )

      set({
        data: dashboardResponse.data,
        isLoading: false,
        error: null,
      })
    } catch (error: any) {
      console.error('Dashboard Error:', error.response?.data || error)
      let errorMessage = 'Failed to fetch dashboard data'
      if (error.response?.data?.detail) {
        errorMessage =
          typeof error.response.data.detail === 'string'
            ? error.response.data.detail
            : 'Validation error occurred'
      }
      set({
        error: errorMessage,
        isLoading: false,
        data: null,
      })
    }
  },
}))

export const useDashboard = () => {
  const store = useDashboardStore()

  useEffect(() => {
    store.fetchDashboard()
    const refreshInterval = setInterval(() => {
      store.fetchDashboard()
    }, 5 * 60 * 1000)

    return () => clearInterval(refreshInterval)
  }, [])

  return {
    ...store,
    refresh: store.fetchDashboard,
  }
}
