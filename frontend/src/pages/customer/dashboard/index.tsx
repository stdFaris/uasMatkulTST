// src/pages/customer/dashboard/index.tsx
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { getCustomerBookings } from '@/services/customer'
import { Booking } from '@/types/customer'
import { format } from 'date-fns'

const Dashboard = () => {
  const { data: bookings = [] } = useQuery<Booking[]>({
    queryKey: ['bookings'],
    queryFn: () => getCustomerBookings(),
  })

  const upcomingBookings = bookings.filter((booking) =>
    ['pending', 'confirmed'].includes(booking.status)
  )

  const recentBookings = bookings
    .filter((booking) => ['completed', 'terminated'].includes(booking.status))
    .slice(0, 5)

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row">
        <Card className="flex-1">
          <CardHeader>
            <CardTitle>Upcoming Bookings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{upcomingBookings.length}</div>
          </CardContent>
        </Card>

        <Card className="flex-1">
          <CardHeader>
            <CardTitle>Total Spent</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              $
              {bookings
                .reduce((sum, booking) => sum + booking.total_price, 0)
                .toFixed(2)}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="upcoming" className="space-y-4">
            <TabsList>
              <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
              <TabsTrigger value="recent">Recent</TabsTrigger>
            </TabsList>

            <TabsContent value="upcoming">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Partner</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead>Duration</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Price</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {upcomingBookings.map((booking) => (
                    <TableRow key={booking.id}>
                      <TableCell>{booking.partner.full_name}</TableCell>
                      <TableCell>
                        {format(new Date(booking.start_datetime), 'PPp')}
                      </TableCell>
                      <TableCell>{booking.duration_hours}h</TableCell>
                      <TableCell className="capitalize">
                        {booking.status}
                      </TableCell>
                      <TableCell className="text-right">
                        ${booking.total_price.toFixed(2)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TabsContent>

            <TabsContent value="recent">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Partner</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead>Duration</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Price</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recentBookings.map((booking) => (
                    <TableRow key={booking.id}>
                      <TableCell>{booking.partner.full_name}</TableCell>
                      <TableCell>
                        {format(new Date(booking.start_datetime), 'PPp')}
                      </TableCell>
                      <TableCell>{booking.duration_hours}h</TableCell>
                      <TableCell className="capitalize">
                        {booking.status}
                      </TableCell>
                      <TableCell className="text-right">
                        ${booking.total_price.toFixed(2)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard
