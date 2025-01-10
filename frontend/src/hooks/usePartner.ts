// src/hooks/usePartner.ts
import { useState, useEffect } from 'react'
import { Partner } from '@/types/partner'
import axiosClient from '@/lib/axios-client'
import { getErrorMessage } from '@/lib/utils'

export function usePartner(partnerId: number) {
  const [partner, setPartner] = useState<Partner | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPartner = async () => {
      try {
        setLoading(true)
        const response = await axiosClient.get(`/partners/${partnerId}`)
        setPartner(response.data)
      } catch (err) {
        console.error('Fetch error:', err)
        setError(getErrorMessage(err))
      } finally {
        setLoading(false)
      }
    }

    if (partnerId) {
      fetchPartner()
    }
  }, [partnerId])

  return { partner, loading, error }
}
