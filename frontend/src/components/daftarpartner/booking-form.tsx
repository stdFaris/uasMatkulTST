import { useState } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Calendar } from '@/components/ui/calendar'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Loader2 } from 'lucide-react'
import { BookingType } from '@/types/partner'
import { Partner } from '@/types/partner'
import { BookingCreate } from '@/types/booking'

interface BookingFormProps {
  partner: Partner
  onSubmit: (booking: BookingCreate) => Promise<void>
  loading: boolean
}

export function BookingForm({ partner, onSubmit, loading }: BookingFormProps) {
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

  const renderTimeSelect = () => {
    if (bookingType === BookingType.HOURLY) {
      return (
        <div className="space-y-4">
          <Label className="text-gray-700 dark:text-gray-300">
            Select Time
          </Label>
          <Select value={selectedTime} onValueChange={setSelectedTime}>
            <SelectTrigger className="bg-gray-50 dark:bg-gray-700">
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
      )
    }
    return null
  }

  const calculateEndDateTime = (startDateTime: Date): Date => {
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

    return endDateTime
  }

  const handleSubmit = async () => {
    if (!selectedDate || !notes) return

    const startDateTime = new Date(selectedDate)

    if (bookingType === BookingType.HOURLY) {
      const [hours] = selectedTime.split(':').map(Number)
      startDateTime.setHours(hours, 0, 0, 0)
    } else {
      startDateTime.setHours(8, 0, 0, 0)
    }

    const endDateTime = calculateEndDateTime(startDateTime)

    const bookingData: BookingCreate = {
      partner_id: partner.id,
      type: bookingType,
      start_datetime: startDateTime.toISOString(),
      end_datetime: endDateTime.toISOString(),
      notes,
    }

    await onSubmit(bookingData)
  }

  return (
    <Card className="bg-white dark:bg-gray-800 shadow-lg">
      <CardHeader>
        <CardTitle className="text-2xl font-display text-gray-900 dark:text-white">
          Book {partner.full_name}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-8">
        <div className="grid gap-6 md:grid-cols-2">
          <div className="space-y-4">
            <Label className="text-gray-700 dark:text-gray-300">
              Booking Type
            </Label>
            <Select
              value={bookingType}
              onValueChange={(value) => {
                setBookingType(value as BookingType)
                setDuration(1)
              }}
            >
              <SelectTrigger className="bg-gray-50 dark:bg-gray-700">
                <SelectValue placeholder="Select booking type" />
              </SelectTrigger>
              <SelectContent>
                {Object.values(BookingType).map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-4">
            <Label className="text-gray-700 dark:text-gray-300">Duration</Label>
            <Select
              value={duration.toString()}
              onValueChange={(value) => setDuration(parseInt(value))}
            >
              <SelectTrigger className="bg-gray-50 dark:bg-gray-700">
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
        </div>

        <div className="space-y-4">
          <Label className="text-gray-700 dark:text-gray-300">
            Select Date
          </Label>
          <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <Calendar
              mode="single"
              selected={selectedDate}
              onSelect={setSelectedDate}
              disabled={(date) => date < new Date()}
              className="rounded-md border-0"
            />
          </div>
        </div>

        {renderTimeSelect()}

        <div className="space-y-4">
          <Label className="text-gray-700 dark:text-gray-300">Notes</Label>
          <Textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add any special requests or notes here"
            className="min-h-[100px] bg-gray-50 dark:bg-gray-700"
          />
        </div>

        <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="text-lg font-semibold text-gray-900 dark:text-white">
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
              onClick={handleSubmit}
              disabled={loading || !selectedDate || !notes}
              className="w-full sm:w-auto bg-primary-600 hover:bg-primary-700 text-white"
              size="lg"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : null}
              Confirm Booking
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
