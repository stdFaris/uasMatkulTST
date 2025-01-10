import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Loader2, Star } from 'lucide-react'
import { usePartner } from '@/hooks/usePartner'
import { Calendar } from '@/components/ui/calendar'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { BookingType } from '@/types/partner'
import { useBooking } from '@/hooks/useBooking'
import { BookingCreate } from '@/types/booking'

export default function PartnerDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { partner, loading: partnerLoading } = usePartner(Number(id))
  const { createBooking, loading: bookingLoading } = useBooking()

  const [selectedDate, setSelectedDate] = useState<Date>()
  const [selectedTime, setSelectedTime] = useState<string>('08:00')
  const [bookingType, setBookingType] = useState<BookingType>(
    BookingType.HOURLY
  )
  const [duration, setDuration] = useState<number>(1)
  const [notes, setNotes] = useState<string>('')

  // Generate time options from 8 AM to 8 PM
  const timeOptions = Array.from({ length: 13 }, (_, i) => {
    const hour = i + 8
    return `${hour.toString().padStart(2, '0')}:00`
  })

  // Generate duration options based on booking type
  const getDurationOptions = () => {
    switch (bookingType) {
      case BookingType.HOURLY:
        return Array.from({ length: 6 }, (_, i) => i + 1) // 1-6 hours
      case BookingType.DAILY:
        return Array.from({ length: 7 }, (_, i) => i + 1) // 1-7 days
      case BookingType.MONTHLY:
        return Array.from({ length: 12 }, (_, i) => i + 1) // 1-12 months
      default:
        return []
    }
  }

  const handleBookingSubmit = async () => {
    if (!partner || !selectedDate || !notes) {
      return
    }

    const startDateTime = new Date(selectedDate)

    if (bookingType === BookingType.HOURLY) {
      const [hours] = selectedTime.split(':').map(Number)
      startDateTime.setHours(hours, 0, 0, 0)
    } else {
      startDateTime.setHours(8, 0, 0, 0)
    }

    let endDateTime = new Date(startDateTime)

    switch (bookingType) {
      case BookingType.HOURLY:
        endDateTime.setHours(endDateTime.getHours() + duration)
        break
      case BookingType.DAILY:
        endDateTime.setDate(endDateTime.getDate() + duration)
        endDateTime.setHours(20, 0, 0, 0)
        break
      case BookingType.MONTHLY:
        endDateTime.setMonth(endDateTime.getMonth() + duration)
        endDateTime.setHours(20, 0, 0, 0)
        break
    }

    const bookingData: BookingCreate = {
      partner_id: partner.id,
      type: bookingType,
      start_datetime: startDateTime.toISOString(),
      end_datetime: endDateTime.toISOString(),
      notes,
    }

    const booking = await createBooking(bookingData)

    if (booking) {
      navigate('/bookings')
    }
  }

  if (partnerLoading || !partner) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Partner Info Card */}
        <div className="lg:col-span-4">
          <Card>
            <CardHeader>
              <CardTitle>{partner.full_name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-2">
                <Star className="h-5 w-5 text-yellow-500" />
                <span>
                  {partner.rating} ({partner.total_reviews} reviews)
                </span>
              </div>
              <div className="space-y-2">
                <h3 className="font-semibold">Pricing</h3>
                <div className="grid grid-cols-1 gap-2 text-sm">
                  <div>
                    Hourly: Rp {partner.pricing.hourly_rate.toLocaleString()}
                  </div>
                  <div>
                    Daily: Rp {partner.pricing.daily_rate.toLocaleString()}
                  </div>
                  <div>
                    Monthly: Rp {partner.pricing.monthly_rate.toLocaleString()}
                  </div>
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="font-semibold">Specializations</h3>
                <div className="flex flex-wrap gap-2">
                  {partner.specializations.map((spec) => (
                    <span
                      key={spec}
                      className="bg-primary/10 text-primary px-2 py-1 rounded-full text-sm"
                    >
                      {spec}
                    </span>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Booking Form Card */}
        <div className="lg:col-span-8">
          <Card>
            <CardHeader>
              <CardTitle>Book {partner.full_name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <Label>Booking Type</Label>
                <Select
                  value={bookingType}
                  onValueChange={(value) => {
                    setBookingType(value as BookingType)
                    setDuration(1)
                  }}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select booking type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={BookingType.HOURLY}>Hourly</SelectItem>
                    <SelectItem value={BookingType.DAILY}>Daily</SelectItem>
                    <SelectItem value={BookingType.MONTHLY}>Monthly</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-4">
                <Label>Select Date</Label>
                <Calendar
                  mode="single"
                  selected={selectedDate}
                  onSelect={setSelectedDate}
                  className="rounded-md border"
                  disabled={(date) => date < new Date()}
                />
              </div>

              {bookingType === BookingType.HOURLY && (
                <div className="space-y-4">
                  <Label>Select Time</Label>
                  <Select value={selectedTime} onValueChange={setSelectedTime}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select time" />
                    </SelectTrigger>
                    <SelectContent>
                      {timeOptions.map((time) => (
                        <SelectItem key={time} value={time}>
                          {time}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}

              <div className="space-y-4">
                <Label>Duration ({bookingType.toLowerCase()})</Label>
                <Select
                  value={duration.toString()}
                  onValueChange={(value) => setDuration(parseInt(value))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select duration" />
                  </SelectTrigger>
                  <SelectContent>
                    {getDurationOptions().map((value) => (
                      <SelectItem key={value} value={value.toString()}>
                        {value}{' '}
                        {value === 1
                          ? bookingType.slice(0, -2)
                          : bookingType.toLowerCase()}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-4">
                <Label>Notes</Label>
                <Textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Add any special requests or notes here"
                  className="min-h-[100px]"
                />
              </div>

              <div className="pt-4 border-t">
                <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
                  <div className="text-lg font-semibold">
                    Total Price: Rp{' '}
                    {(
                      duration *
                      (bookingType === BookingType.HOURLY
                        ? partner.pricing.hourly_rate
                        : bookingType === BookingType.DAILY
                        ? partner.pricing.daily_rate
                        : partner.pricing.monthly_rate)
                    ).toLocaleString()}
                  </div>
                  <Button
                    onClick={handleBookingSubmit}
                    disabled={bookingLoading || !selectedDate || !notes}
                    size="lg"
                  >
                    {bookingLoading ? (
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    ) : null}
                    Confirm Booking
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
