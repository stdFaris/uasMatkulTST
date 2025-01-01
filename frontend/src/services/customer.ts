// src/services/customer.ts
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const getCustomerBookings = async (status?: string) => {
  const response = await axios.get(`${API_URL}/api/customers/me/bookings`, {
    params: { status },
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
  return response.data
}
