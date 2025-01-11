// src/components/dashboard/stats-card.tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface StatsCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  description?: string
}

export function StatsCard({ title, value, icon, description }: StatsCardProps) {
  return (
    <Card className="bg-white shadow-soft hover:shadow-lg transition-shadow duration-200">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 border-b border-primary-100">
        <CardTitle className="text-sm font-semibold text-primary-700">
          {title}
        </CardTitle>
        {icon}
      </CardHeader>
      <CardContent className="pt-4">
        <div className="text-2xl font-bold text-primary-900">{value}</div>
        {description && (
          <p className="text-xs text-primary-600 mt-1">{description}</p>
        )}
      </CardContent>
    </Card>
  )
}
