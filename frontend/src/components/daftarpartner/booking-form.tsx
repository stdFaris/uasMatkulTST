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
import { BookingConflictAlert } from './popupConfict'
import { useToast } from '@/hooks/use-toast'

interface BookingFormProps {
  partner: Partner
  onSubmit: (booking: BookingCreate) => Promise<void>
  loading: boolean
}

export function BookingForm({ partner, onSubmit, loading }: BookingFormProps) {
  const { toast } = useToast()
  const [selectedDate, setSelectedDate] = useState<Date>()
  const [selectedTime, setSelectedTime] = useState<string>('08:00')
  const [bookingType, setBookingType] = useState<BookingType>(
    BookingType.HOURLY
  )
  const [duration, setDuration] = useState<number>(1)
  const [notes, setNotes] = useState<string>('')
  const [showConflictAlert, setShowConflictAlert] = useState(false)

  // Function to generate available time options based on selected duration
  const getTimeOptions = () => {
    if (bookingType !== BookingType.HOURLY) return []

    // Calculate the latest possible start time based on duration
    const maxStartHour = 20 - duration

    return Array.from({ length: maxStartHour - 7 }, (_, i) => {
      const hour = i + 8
      return `${hour.toString().padStart(2, '0')}:00`
    })
  }

  const getDurationOptions = () => {
    switch (bookingType) {
      case BookingType.HOURLY:
        // Get start hour from selected time
        const startHour = selectedTime
          ? parseInt(selectedTime.split(':')[0])
          : 8
        // Calculate remaining hours until 20:00
        const remainingHours = 20 - startHour
        // Limit to 6 hours or remaining hours
        const maxDuration = Math.min(6, remainingHours)
        return Array.from({ length: maxDuration }, (_, i) => i + 1)

      case BookingType.DAILY:
        return Array.from({ length: 7 }, (_, i) => i + 1)

      case BookingType.MONTHLY:
        return Array.from({ length: 12 }, (_, i) => i + 1)

      default:
        return []
    }
  }

  // Function to get booking type display name
  const getBookingTypeLabel = (type: BookingType): string => {
    switch (type) {
      case BookingType.HOURLY:
        return 'Jam'
      case BookingType.DAILY:
        return 'Hari'
      case BookingType.MONTHLY:
        return 'Bulan'
      default:
        return type
    }
  }

  const renderTimeSelect = () => {
    if (bookingType === BookingType.HOURLY) {
      const timeOptions = getTimeOptions()

      return (
        <div className="space-y-4">
          <Label className="text-gray-700 dark:text-gray-300">
            Pilih Waktu
          </Label>
          <Select
            value={selectedTime}
            onValueChange={(value) => {
              setSelectedTime(value)
              // Reset duration if current duration would exceed 20:00
              const startHour = parseInt(value.split(':')[0])
              const maxDuration = 20 - startHour
              if (duration > maxDuration) {
                setDuration(maxDuration)
              }
            }}
          >
            <SelectTrigger className="bg-gray-50 dark:bg-gray-700">
              <SelectValue placeholder="Pilih waktu" />
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
        if (endDateTime.getHours() > 20) {
          throw new Error('Booking tidak bisa melebihi jam 20:00')
        }
        break

      case BookingType.DAILY:
        if (duration === 1) {
          endDateTime.setHours(20, 0, 0, 0)
        } else {
          endDateTime.setDate(endDateTime.getDate() + (duration - 1))
          endDateTime.setHours(20, 0, 0, 0)
        }
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

    try {
      await onSubmit(bookingData)
      toast({
        title: 'Booking Berhasil',
        description: 'Booking anda telah berhasil dibuat',
      })
    } catch (error: any) {
      console.error('Error in handleSubmit:', error)
      setShowConflictAlert(true)
    }
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
              Jenis Booking
            </Label>
            <Select
              value={bookingType}
              onValueChange={(value) => {
                setBookingType(value as BookingType)
                setDuration(1)
              }}
            >
              <SelectTrigger className="bg-gray-50 dark:bg-gray-700">
                <SelectValue placeholder="Pilih jenis booking" />
              </SelectTrigger>
              <SelectContent>
                {Object.values(BookingType).map((type) => (
                  <SelectItem key={type} value={type}>
                    {getBookingTypeLabel(type)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-4">
            <Label className="text-gray-700 dark:text-gray-300">Durasi</Label>
            <Select
              value={duration.toString()}
              onValueChange={(value) => setDuration(parseInt(value))}
            >
              <SelectTrigger className="bg-gray-50 dark:bg-gray-700">
                <SelectValue placeholder="Pilih durasi" />
              </SelectTrigger>
              <SelectContent>
                {getDurationOptions().map((value) => (
                  <SelectItem key={value} value={value.toString()}>
                    {value} {getBookingTypeLabel(bookingType)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="space-y-4">
          <Label className="text-gray-700 dark:text-gray-300">
            Pilih Tanggal
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
          <Label className="text-gray-700 dark:text-gray-300">Catatan</Label>
          <Textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Tambahkan permintaan khusus atau catatan di sini"
            className="min-h-[100px] bg-gray-50 dark:bg-gray-700"
          />
        </div>

        <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="text-lg font-semibold text-gray-900 dark:text-white">
              Total Harga: Rp{' '}
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
              Konfirmasi Booking
            </Button>
          </div>
        </div>
      </CardContent>
      <BookingConflictAlert
        isOpen={showConflictAlert}
        onClose={() => setShowConflictAlert(false)}
        conflictDetails={{
          startTime: selectedDate ? selectedDate.toISOString() : '',
          endTime: selectedDate
            ? calculateEndDateTime(selectedDate).toISOString()
            : '',
        }}
      />
    </Card>
  )
}
