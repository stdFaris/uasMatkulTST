// PartnersPage.tsx updates
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Partner, PartnerFilter } from '@/types/partner'
import { PartnerCard } from '@/components/partner/partner-card'
import { PartnerFilters } from '@/components/partner/partner-filters'
import { usePartners } from '@/hooks/usePartners'
import { Search, Loader2 } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
export function PartnersPage() {
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPartner, setSelectedPartner] = useState<Partner | null>(null)
  const [filters, setFilters] = useState<PartnerFilter>({})

  const { user } = useAuth()
  const { partners, loading, error } = usePartners(
    user?.kecamatan || '',
    filters
  )

  const filteredPartners = partners.filter(
    (partner) =>
      partner.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      partner.specializations.some((spec) =>
        spec.toLowerCase().includes(searchTerm.toLowerCase())
      )
  )

  const handlePartnerSelect = (partner: Partner) => {
    if (partner.is_available) {
      setSelectedPartner(partner)
    }
  }

  const handleContinue = () => {
    if (selectedPartner) {
      if (selectedPartner.is_available) {
        navigate(`/partners/${selectedPartner.id}`)
      }
    }
  }

  return (
    <>
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-3">
            <div className="sticky top-4">
              <PartnerFilters filters={filters} onFilterChange={setFilters} />
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-9 space-y-6">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="relative w-full sm:w-96">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search by name or specialization..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-9 w-full"
                />
              </div>
              <Button
                size="lg"
                onClick={handleContinue}
                disabled={!selectedPartner}
                className="w-full sm:w-auto"
              >
                Continue with Selected Partner
              </Button>
            </div>

            {loading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary-500" />
              </div>
            )}

            {error && (
              <div className="rounded-lg bg-error-50 p-4 text-error-500 text-center">
                {error}
              </div>
            )}

            <ScrollArea className="h-[calc(100vh-12rem)]">
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {filteredPartners.map((partner) => (
                  <PartnerCard
                    key={partner.id}
                    partner={partner}
                    onSelect={handlePartnerSelect}
                    isSelected={selectedPartner?.id === partner.id}
                  />
                ))}
              </div>
              {!loading && filteredPartners.length === 0 && (
                <div className="text-center py-12">
                  <p className="text-lg font-medium text-foreground">
                    No partners found
                  </p>
                  <p className="text-muted-foreground">
                    Try adjusting your filters or search terms
                  </p>
                </div>
              )}
            </ScrollArea>
          </div>
        </div>
      </div>
    </>
  )
}
