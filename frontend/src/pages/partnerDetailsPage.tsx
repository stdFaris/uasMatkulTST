import { useParams, useNavigate } from 'react-router-dom'
import { Loader2 } from 'lucide-react'
import { usePartner } from '@/hooks/usePartner'
import { useBooking } from '@/hooks/useBooking'
import { PartnerInfoCard } from '@/components/daftarpartner/partner-card'
import { BookingForm } from '@/components/daftarpartner/booking-form'
import { BookingCreate } from '@/types/booking'

export default function PartnerDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const {
    partner,
    loading: partnerLoading,
    error: partnerError,
  } = usePartner(Number(id))
  const { createBooking, loading: bookingLoading } = useBooking()

  const handleBookingSubmit = async (bookingData: BookingCreate) => {
    try {
      const booking = await createBooking(bookingData)
      if (booking) {
        navigate('/bookings')
      }
    } catch (error) {
      throw error
    }
  }

  if (partnerError) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
          Error Loading Partner Details
        </h2>
        <p className="text-gray-600 dark:text-gray-300">
          Unable to load partner information. Please try again later.
        </p>
      </div>
    )
  }

  if (partnerLoading || !partner) {
    return (
      <div className="container mx-auto px-4 py-16 flex justify-center items-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <nav className="mb-8">
          <button
            onClick={() => navigate(-1)}
            className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white flex items-center gap-2"
          >
            ← Back to Partners
          </button>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-4">
            <div className="sticky top-8">
              <PartnerInfoCard partner={partner} />
            </div>
          </div>

          <div className="lg:col-span-8">
            <BookingForm
              partner={partner}
              onSubmit={handleBookingSubmit}
              loading={bookingLoading}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
