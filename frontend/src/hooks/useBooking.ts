import { useState } from 'react'
import { BookingCreate, Booking } from '@/types/booking'
import { useToast } from './use-toast'
import axiosClient from '@/lib/axios-client'
import { getErrorMessage } from '@/lib/utils'

export function useBooking() {
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  const createBooking = async (
    bookingData: BookingCreate
  ): Promise<Booking | null> => {
    setLoading(true)
    try {
      const response = await axiosClient.post('/bookings/', bookingData)

      toast({
        title: 'Booking Success',
        description: 'Your booking has been successfully created',
      })
      return response.data
    } catch (err) {
      console.error('Booking error:', err)
      toast({
        title: 'Booking Failed',
        description: getErrorMessage(err),
        variant: 'destructive',
      })
      return null
    } finally {
      setLoading(false)
    }
  }

  return { createBooking, loading }
}
