// src/components/customer/layout/DashboardLayout.tsx
import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import Sidebar from './Sidebar'

const DashboardLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  return (
    <div>
      <Navbar onMenuClick={() => setIsSidebarOpen(true)} />
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
      <main className="md:pl-64 pt-16 min-h-screen">
        <div className="container p-4 mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

export default DashboardLayout
