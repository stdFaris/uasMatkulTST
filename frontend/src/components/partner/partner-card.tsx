// src/components/partners/partner-card.tsx
import { Partner } from '@/types/partner'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Star, Clock, CreditCard, Languages } from 'lucide-react'

interface PartnerCardProps {
  partner: Partner
  onSelect: (partner: Partner) => void
  isSelected: boolean
}

export function PartnerCard({
  partner,
  onSelect,
  isSelected,
}: PartnerCardProps) {
  const unavailableStyles = !partner.is_available
    ? 'opacity-75 cursor-not-allowed bg-gray-50'
    : 'hover:scale-[1.02]'

  return (
    <Card
      className={`group relative transition-all duration-200 hover:shadow-soft ${
        isSelected && partner.is_available
          ? 'ring-2 ring-primary-500 shadow-soft'
          : unavailableStyles
      }`}
      onClick={() => onSelect(partner)}
      role="button"
      tabIndex={partner.is_available ? 0 : -1}
      onKeyPress={(e) =>
        e.key === 'Enter' && partner.is_available && onSelect(partner)
      }
    >
      <CardHeader className="flex flex-row items-center gap-4 pb-4">
        <div className="relative h-20 w-20 rounded-full overflow-hidden bg-secondary-100">
          <img
            src={partner.profile_image || '/api/placeholder/80/80'}
            alt="img"
            className={`h-full w-full object-cover transition-transform duration-200 ${
              partner.is_available ? 'group-hover:scale-110' : 'grayscale'
            }`}
          />
          {partner.is_available ? (
            <div className="absolute bottom-0 right-0 h-4 w-4 rounded-full bg-success-500 border-2 border-white" />
          ) : (
            <div className="absolute bottom-0 right-0 h-4 w-4 rounded-full bg-gray-400 border-2 border-white" />
          )}
        </div>
        <div className="flex-1 space-y-1">
          <CardTitle className="font-display text-xl text-foreground">
            {partner.full_name}
          </CardTitle>
          <div className="flex items-center gap-1.5">
            <Star className="h-4 w-4 fill-warning-500 text-warning-500" />
            <span className="text-sm font-medium text-foreground">
              {partner.rating.toFixed(1)}
            </span>
            <span className="text-sm text-muted-foreground">
              ({partner.total_reviews} reviews)
            </span>
          </div>
          <div className="flex gap-2">
            <Badge
              variant="secondary"
              className="capitalize text-xs font-medium"
            >
              {partner.role.replace('_', ' ')}
            </Badge>
            {!partner.is_available && (
              <Badge
                variant="secondary"
                className="bg-gray-200 text-gray-700 text-xs font-medium"
              >
                Currently Unavailable
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <Clock className="h-4 w-4 text-primary-500" />
            <div>
              <p className="text-sm font-medium text-foreground">Experience</p>
              <p className="text-sm text-muted-foreground">
                {partner.experience_years} years
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <CreditCard className="h-4 w-4 text-primary-500" />
            <div>
              <p className="text-sm font-medium text-foreground">Hourly Rate</p>
              <p className="text-sm text-muted-foreground">
                Rp {partner.pricing.hourly_rate.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        {partner.languages && (
          <div className="flex items-center gap-2">
            <Languages className="h-4 w-4 text-primary-500" />
            <p className="text-sm text-muted-foreground">
              {partner.languages.join(', ')}
            </p>
          </div>
        )}

        <div className="flex flex-wrap gap-1.5">
          {partner.specializations.map((spec) => (
            <Badge
              key={spec}
              variant="outline"
              className="text-xs bg-secondary-50 text-secondary-700 border-secondary-200"
            >
              {spec}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
