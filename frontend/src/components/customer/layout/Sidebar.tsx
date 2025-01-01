// src/components/customer/layout/Sidebar.tsx
import { NavLink } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Home, Calendar, Clock, MessageSquare, Settings, X } from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

const Sidebar = ({ isOpen, onClose }: SidebarProps) => {
  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Bookings', href: '/bookings', icon: Calendar },
    { name: 'History', href: '/history', icon: Clock },
    { name: 'Messages', href: '/messages', icon: MessageSquare },
    { name: 'Settings', href: '/settings', icon: Settings },
  ]

  return (
    <>
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 w-64 bg-background border-r transition-transform duration-300 ease-in-out md:translate-x-0',
          !isOpen && '-translate-x-full'
        )}
      >
        <div className="flex h-16 items-center gap-2 border-b px-4">
          <h2 className="text-lg font-semibold flex-1">SantaiRumah</h2>
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={onClose}
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        <ScrollArea className="h-[calc(100vh-4rem)]">
          <div className="space-y-1 p-2">
            {navigation.map((item) => (
              <NavLink
                key={item.name}
                to={item.href}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors',
                    isActive ? 'bg-secondary' : 'hover:bg-secondary/50'
                  )
                }
              >
                <item.icon className="h-5 w-5" />
                {item.name}
              </NavLink>
            ))}
          </div>
        </ScrollArea>
      </aside>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden"
          onClick={onClose}
        />
      )}
    </>
  )
}

export default Sidebar
