import { useEffect, useState } from 'react'
import { Partner } from '@/types/partner'
import { PartnerFilter } from '@/types/partner'
import axiosClient from '@/lib/axios-client'
import { getErrorMessage } from '@/lib/utils'

export function usePartners(kecamatan: string, filters: PartnerFilter) {
  const [partners, setPartners] = useState<Partner[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPartners = async () => {
      try {
        setLoading(true)
        const queryParams = new URLSearchParams({
          kecamatan,
          ...Object.fromEntries(
            Object.entries(filters).filter(([_, v]) => v !== undefined)
          ),
        })

        const response = await axiosClient.get(
          `/partners/search?${queryParams}`
        )
        setPartners(response.data)
      } catch (err) {
        console.error('Fetch error:', err)
        setError(getErrorMessage(err))
      } finally {
        setLoading(false)
      }
    }

    fetchPartners()
  }, [kecamatan, filters])

  return { partners, loading, error }
}
