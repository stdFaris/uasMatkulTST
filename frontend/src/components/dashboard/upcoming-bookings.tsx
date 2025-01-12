import { Booking } from '@/types/booking'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { formatDateTimeBooking, formatPrice } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { RefreshCw } from 'lucide-react'

interface UpcomingBookingsProps {
  bookings: Booking[]
  onRefresh: () => void
}

export function UpcomingBookings({
  bookings,
  onRefresh,
}: UpcomingBookingsProps) {
  return (
    <Card className="col-span-full xl:col-span-2 bg-white shadow-soft hover:shadow-lg transition-shadow duration-200">
      <CardHeader className="flex flex-row items-center justify-between border-b border-primary-100 pb-4">
        <CardTitle className="text-lg font-semibold text-primary-900">
          Upcoming Bookings
        </CardTitle>
        <Button
          onClick={onRefresh}
          variant="ghost"
          size="sm"
          className="hover:bg-primary-50"
        >
          <RefreshCw className="w-4 h-4" />
        </Button>
      </CardHeader>
      <CardContent className="pt-4">
        <div className="max-h-96 overflow-y-auto pr-2">
          <div className="space-y-4">
            {bookings.length === 0 ? (
              <p className="text-center text-primary-600 py-8">
                No upcoming bookings
              </p>
            ) : (
              bookings.slice(0, 5).map((booking) => (
                <div
                  key={booking.id}
                  className="flex items-center justify-between p-4 rounded-lg bg-primary-50/50 hover:bg-primary-50 transition-colors"
                >
                  <div className="space-y-1">
                    <p className="font-semibold text-primary-900">
                      {booking.partner.full_name}
                    </p>
                    <div className="text-sm text-primary-600 space-y-0.5">
                      <p>
                        Start: {formatDateTimeBooking(booking.start_datetime)}
                      </p>
                      <p>End: {formatDateTimeBooking(booking.end_datetime)}</p>
                    </div>
                    <p className="text-sm text-primary-600">{booking.type}</p>
                  </div>
                  <div className="text-right space-y-1">
                    <p className="font-semibold text-primary-900">
                      {formatPrice(booking.total_price)}
                    </p>
                    <p className="text-sm text-primary-600 capitalize">
                      {booking.status.toLowerCase()}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
