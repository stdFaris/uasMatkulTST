// src/components/layout/main-layout.tsx
import { Outlet } from 'react-router-dom'
import { Header } from './header'

export function MainLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
}