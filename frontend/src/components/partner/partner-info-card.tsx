// components/partner/PartnerInfoCard.tsx
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Star } from 'lucide-react'
import { Partner } from '@/types/partner'

interface PartnerInfoCardProps {
  partner: Partner
}

export function PartnerInfoCard({ partner }: PartnerInfoCardProps) {
  return (
    <Card className="h-full bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-shadow duration-300">
      <CardHeader className="pb-2">
        <CardTitle className="text-2xl font-display text-gray-900 dark:text-white">
          {partner.full_name}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex items-center gap-2">
          <Star className="h-5 w-5 text-yellow-400" />
          <span className="text-gray-700 dark:text-gray-300">
            {partner.rating} ({partner.total_reviews} reviews)
          </span>
        </div>

        <div className="space-y-3">
          <h3 className="font-semibold text-gray-900 dark:text-white">
            Pricing
          </h3>
          <div className="grid grid-cols-1 gap-3 text-sm">
            {Object.entries(partner.pricing).map(([key, value]) => (
              <div
                key={key}
                className="flex justify-between items-center p-2 rounded-lg bg-gray-50 dark:bg-gray-700"
              >
                <span className="capitalize text-gray-600 dark:text-gray-300">
                  {key.replace('_rate', '')}
                </span>
                <span className="font-semibold text-gray-900 dark:text-white">
                  Rp {value.toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-3">
          <h3 className="font-semibold text-gray-900 dark:text-white">
            Specializations
          </h3>
          <div className="flex flex-wrap gap-2">
            {partner.specializations.map((spec) => (
              <span
                key={spec}
                className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-medium"
              >
                {spec}
              </span>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
