// src/components/partners/partner-filters.tsx
import { PartnerFilter } from '@/types/partner'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { UserRound, Timer, Star } from 'lucide-react'

interface PartnerFiltersProps {
  filters: PartnerFilter
  onFilterChange: (filters: PartnerFilter) => void
}

export function PartnerFilters({
  filters,
  onFilterChange,
}: PartnerFiltersProps) {
  const handleChange = (key: keyof PartnerFilter, value: any) => {
    onFilterChange({ ...filters, [key]: value })
  }

  return (
    <Card className="bg-secondary-50 border-secondary-200">
      <CardHeader className="pb-4">
        <CardTitle className="text-lg font-display text-secondary-900">
          Filters
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-secondary-700">
            <UserRound className="h-4 w-4" />
            <label className="text-sm font-medium">Partner Role</label>
          </div>
          <Select
            value={filters.role}
            onValueChange={(value) => handleChange('role', value)}
          >
            <SelectTrigger className="bg-white border-secondary-200 text-secondary-900">
              <SelectValue placeholder="Select role" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="pembantu">
                <span className="flex items-center gap-2">
                  Pembantu
                  <Badge
                    variant="secondary"
                    className="bg-primary-100 text-primary-700"
                  >
                    Home
                  </Badge>
                </span>
              </SelectItem>
              <SelectItem value="tukang_kebun">
                <span className="flex items-center gap-2">
                  Tukang Kebun
                  <Badge
                    variant="secondary"
                    className="bg-success-100 text-success-700"
                  >
                    Garden
                  </Badge>
                </span>
              </SelectItem>
              <SelectItem value="tukang_pijat">
                <span className="flex items-center gap-2">
                  Tukang Pijat
                  <Badge
                    variant="secondary"
                    className="bg-success-100 text-success-700"
                  >
                    Massage
                  </Badge>
                </span>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Separator className="bg-secondary-200" />

        <div className="space-y-2">
          <div className="flex items-center gap-2 text-secondary-700">
            <Star className="h-4 w-4" />
            <label className="text-sm font-medium">Minimum Rating</label>
          </div>
          <Input
            type="number"
            min="0"
            max="5"
            step="0.5"
            value={filters.min_rating || ''}
            onChange={(e) =>
              handleChange(
                'min_rating',
                e.target.value ? Number(e.target.value) : undefined
              )
            }
            className="bg-white border-secondary-200"
            placeholder="Enter minimum rating"
          />
        </div>

        <div className="space-y-2">
          <div className="flex items-center gap-2 text-secondary-700">
            <Timer className="h-4 w-4" />
            <label className="text-sm font-medium">Minimum Experience</label>
          </div>
          <Input
            type="number"
            min="0"
            value={filters.min_experience || ''}
            onChange={(e) =>
              handleChange(
                'min_experience',
                e.target.value ? Number(e.target.value) : undefined
              )
            }
            className="bg-white border-secondary-200"
            placeholder="Enter years of experience"
          />
        </div>
      </CardContent>
    </Card>
  )
}
