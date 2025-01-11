import { useState } from 'react'
import { BookingCreate, Booking } from '@/types/booking'
import axiosClient from '@/lib/axios-client'

export function useBooking() {
  const [loading, setLoading] = useState(false)

  const createBooking = async (
    bookingData: BookingCreate
  ): Promise<Booking | null> => {
    setLoading(true)
    try {
      const response = await axiosClient.post('/bookings/', bookingData)
      return response.data
    } catch (err) {
      console.error('Booking error:', err)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return { createBooking, loading }
}
