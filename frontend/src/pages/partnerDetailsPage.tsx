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
  const { partner, loading: partnerLoading } = usePartner(Number(id))
  const { createBooking, loading: bookingLoading } = useBooking()

  const handleBookingSubmit = async (bookingData: BookingCreate) => {
    const booking = await createBooking(bookingData)
    if (booking) {
      navigate('/bookings')
    }
  }

  if (partnerLoading || !partner) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4">
          <PartnerInfoCard partner={partner} />
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
  )
}
