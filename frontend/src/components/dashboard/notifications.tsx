// src/components/dashboard/notifications
import { Notification, NotificationType } from '@/types/notification'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { formatDateTime } from '@/lib/utils'
import { Bell, CalendarClock, CalendarX, Check, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface NotificationsProps {
  notifications: Notification[]
  onRefresh: () => void
}

export function Notifications({
  notifications,
  onRefresh,
}: NotificationsProps) {
  const getNotificationIcon = (type: NotificationType) => {
    switch (type) {
      case NotificationType.BOOKING_REMINDER:
        return <CalendarClock className="h-5 w-5 text-blue-500" />
      case NotificationType.SCHEDULE_CHANGE:
        return <RefreshCw className="h-5 w-5 text-yellow-500" />
      case NotificationType.BOOKING_CONFIRMATION:
        return <Check className="h-5 w-5 text-green-500" />
      case NotificationType.PARTNER_UNAVAILABLE:
        return <CalendarX className="h-5 w-5 text-red-500" />
      default:
        return <Bell className="h-5 w-5 text-gray-500" />
    }
  }

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg font-medium">
          Recent Notifications
        </CardTitle>
        <Button
          variant="ghost"
          size="sm"
          onClick={onRefresh}
          className="hover:bg-gray-100"
        >
          <RefreshCw className="h-4 w-4 mr-1" />
          Refresh
        </Button>
      </CardHeader>
      <CardContent>
        {notifications.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <Bell className="h-12 w-12 text-gray-300 mb-3" />
            <p className="text-gray-500 font-medium">No new notifications</p>
            <p className="text-sm text-gray-400">
              When you receive notifications, they will appear here
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className="flex items-start space-x-4 p-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex-shrink-0">
                  {getNotificationIcon(notification.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900">
                    {notification.message}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {formatDateTime(notification.created_at)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
