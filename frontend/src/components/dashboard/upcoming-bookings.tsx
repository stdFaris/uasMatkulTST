// src/components/dashboard/upcoming-bookings.tsx
import { Booking } from '@/types/booking'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { formatDateTime, formatPrice } from '@/lib/utils'
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
    <Card className="col-span-full xl:col-span-2">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Upcoming Bookings</CardTitle>
        <Button onClick={onRefresh} variant="ghost" size="sm">
          <RefreshCw className="w-4 h-4" />
        </Button>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {bookings.length === 0 ? (
            <p className="text-center text-muted-foreground py-4">
              No upcoming bookings
            </p>
          ) : (
            bookings.map((booking) => (
              <div
                key={booking.id}
                className="flex items-center justify-between p-4 rounded-lg bg-secondary-50"
              >
                <div>
                  <p className="font-medium">{booking.partner.full_name}</p>
                  <p className="text-sm text-muted-foreground">
                    {formatDateTime(booking.start_datetime)}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {booking.type}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-medium">
                    {formatPrice(booking.total_price)}
                  </p>
                  <p className="text-sm text-muted-foreground capitalize">
                    {booking.status.toLowerCase()}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}
