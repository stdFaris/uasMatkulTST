import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { RefreshCw, Star, MapPin, Languages, Briefcase } from 'lucide-react'
import { formatPrice } from '@/lib/utils'
import { Partner, PartnerRole } from '@/types/partner'

const roleLabels = {
  [PartnerRole.PEMBANTU]: 'Pembantu',
  [PartnerRole.TUKANG_KEBUN]: 'Tukang Kebun',
  [PartnerRole.TUKANG_PIJAT]: 'Tukang Pijat',
}

const roleColors = {
  [PartnerRole.PEMBANTU]: 'bg-blue-100 text-blue-800',
  [PartnerRole.TUKANG_KEBUN]: 'bg-green-100 text-green-800',
  [PartnerRole.TUKANG_PIJAT]: 'bg-purple-100 text-purple-800',
}

interface RecommendedPartnersProps {
  partners: Partner[]
  onRefresh: (roles?: PartnerRole[]) => void
}

export function RecommendedPartners({
  partners,
  onRefresh,
}: RecommendedPartnersProps) {
  const navigate = useNavigate()
  const [selectedRoles, setSelectedRoles] = useState<PartnerRole[]>([])

  const handleRoleToggle = (role: PartnerRole) => {
    setSelectedRoles((current) => {
      const newRoles = current.includes(role)
        ? current.filter((r) => r !== role)
        : [...current, role]
      onRefresh(newRoles.length > 0 ? newRoles : undefined)
      return newRoles
    })
  }

  const handlePartnerClick = (
    partnerId: string | number,
    isAvailable: boolean
  ) => {
    if (!isAvailable) return
    navigate(`/partners/${partnerId.toString()}`)
  }

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0 pb-4">
        <div>
          <CardTitle className="text-lg sm:text-xl font-bold">
            Recommended Partners
          </CardTitle>
          <p className="text-xs sm:text-sm text-muted-foreground mt-1">
            {selectedRoles.length === 0
              ? 'Select roles to see recommendations'
              : `Top rated partners for selected roles`}
          </p>
        </div>
        <Button
          onClick={() => onRefresh()}
          variant="ghost"
          size="icon"
          className="self-end sm:self-auto"
        >
          <RefreshCw className="w-4 h-4" />
        </Button>
      </CardHeader>

      <CardContent>
        <div className="mb-4 sm:mb-6">
          <div className="flex flex-wrap gap-2">
            {Object.entries(roleLabels).map(([role, label]) => (
              <Button
                key={role}
                variant={
                  selectedRoles.includes(role as PartnerRole)
                    ? 'default'
                    : 'secondary'
                }
                size="sm"
                onClick={() => handleRoleToggle(role as PartnerRole)}
                className={`text-xs sm:text-sm h-7 sm:h-8 ${
                  selectedRoles.includes(role as PartnerRole)
                    ? ''
                    : 'opacity-60 hover:opacity-100'
                }`}
              >
                {label}
              </Button>
            ))}
          </div>
        </div>

        <div className="space-y-3 sm:space-y-4">
          {partners.length === 0 ? (
            <div className="text-center py-6 sm:py-8 bg-secondary/10 rounded-lg">
              <p className="text-sm text-muted-foreground px-4">
                {selectedRoles.length === 0
                  ? 'Please select at least one role to see recommendations'
                  : 'No recommended partners available for selected roles'}
              </p>
            </div>
          ) : (
            partners.map((partner) => (
              <div
                key={partner.id}
                onClick={() =>
                  handlePartnerClick(partner.id, partner.is_available)
                }
                className={`p-3 sm:p-4 rounded-lg space-y-2 sm:space-y-3 transition-colors ${
                  partner.is_available
                    ? 'bg-secondary/10 hover:bg-secondary/20 cursor-pointer'
                    : 'bg-gray-100 cursor-not-allowed opacity-60'
                }`}
                role="button"
                tabIndex={partner.is_available ? 0 : -1}
                onKeyDown={(e) => {
                  if (
                    (e.key === 'Enter' || e.key === ' ') &&
                    partner.is_available
                  ) {
                    handlePartnerClick(partner.id, partner.is_available)
                  }
                }}
              >
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2 sm:gap-0">
                  <div>
                    <h3 className="font-semibold text-sm sm:text-base">
                      {partner.full_name}
                    </h3>
                    <div className="flex gap-2 mt-1">
                      <Badge
                        variant="secondary"
                        className={`text-xs ${roleColors[partner.role]}`}
                      >
                        {roleLabels[partner.role]}
                      </Badge>
                      {!partner.is_available && (
                        <Badge
                          variant="secondary"
                          className="bg-gray-200 text-gray-700 text-xs"
                        >
                          Currently Unavailable
                        </Badge>
                      )}
                    </div>
                  </div>
                  <div className="text-left sm:text-right">
                    <p className="font-semibold text-sm sm:text-base">
                      {formatPrice(partner.pricing.hourly_rate)}
                    </p>
                    <p className="text-xs sm:text-sm text-muted-foreground">
                      per hour
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs sm:text-sm">
                  <div className="flex items-center gap-1">
                    <Star className="w-3 h-3 sm:w-4 sm:h-4 text-yellow-500" />
                    <span>
                      {partner.rating} ({partner.total_reviews} reviews)
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Briefcase className="w-3 h-3 sm:w-4 sm:h-4 text-muted-foreground" />
                    <span>{partner.experience_years} years exp.</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <MapPin className="w-3 h-3 sm:w-4 sm:h-4 text-muted-foreground" />
                    <span className="truncate">{partner.kecamatan}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Languages className="w-3 h-3 sm:w-4 sm:h-4 text-muted-foreground" />
                    <span className="truncate">
                      {partner.languages.join(', ')}
                    </span>
                  </div>
                </div>

                {partner.specializations.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {partner.specializations.map((spec) => (
                      <Badge
                        key={spec}
                        variant="outline"
                        className="text-[10px] sm:text-xs px-1.5 py-0.5"
                      >
                        {spec}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}
