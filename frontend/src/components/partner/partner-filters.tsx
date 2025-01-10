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
    <div className="space-y-4">
      <Select
        value={filters.role}
        onValueChange={(value) => handleChange('role', value)}
      >
        <SelectTrigger>
          <SelectValue placeholder="Select role" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="pembantu">Pembantu</SelectItem>
          <SelectItem value="tukang_kebun">Tukang Kebun</SelectItem>
          <SelectItem value="tukang_pijat">Tukang Pijat</SelectItem>
        </SelectContent>
      </Select>

      <Separator />

      <div className="space-y-2">
        <label className="text-sm font-medium">Minimum Rating</label>
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
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">
          Minimum Experience (years)
        </label>
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
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">Maximum Hourly Rate</label>
        <Input
          type="number"
          min="0"
          value={filters.max_hourly_rate || ''}
          onChange={(e) =>
            handleChange(
              'max_hourly_rate',
              e.target.value ? Number(e.target.value) : undefined
            )
          }
        />
      </div>
    </div>
  )
}
