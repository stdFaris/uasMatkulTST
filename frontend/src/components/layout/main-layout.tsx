// src/components/layout/main-layout.tsx
import { Outlet } from 'react-router-dom'
import { Header } from './header'

export function MainLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      <Header />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 bg-gradient-to-b from-primary-50 to-white">
        <Outlet />
      </main>
    </div>
  )
}
