// src/components/auth/RegisterForm.tsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Icons } from '@/components/shared/icons'
import { RegisterFormData } from '@/types/auth'
import { register } from '@/services/auth'

export const RegisterForm = () => {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState<RegisterFormData>({
    email: '',
    password: '',
    full_name: '',
    phone: '',
  })
  const [errors, setErrors] = useState<Partial<RegisterFormData>>({})

  // Validasi form
  const validateForm = () => {
    const newErrors: Partial<RegisterFormData> = {}

    // Validasi email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    // Validasi phone (format internasional)
    const phoneRegex = /^\+?[1-9]\d{1,14}$/
    if (!phoneRegex.test(formData.phone)) {
      newErrors.phone = 'Please enter a valid phone number (e.g. +628123456789)'
    }

    // Validasi full name
    if (formData.full_name.length < 2) {
      newErrors.full_name = 'Full name is too short'
    }

    // Validasi password
    if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setErrors({})

    // Validasi form sebelum submit
    if (!validateForm()) {
      setIsLoading(false)
      return
    }

    try {
      // Format phone number jika belum ada kode negara
      const formattedData = {
        ...formData,
        phone: formData.phone.startsWith('+')
          ? formData.phone
          : `+${formData.phone}`,
      }

      await register(formattedData)
      navigate('/login')
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.detail || 'Registration failed. Please try again.'
      setErrors({ submit: errorMessage })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="full_name">Full Name</Label>
          <Input
            id="full_name"
            type="text"
            placeholder="John Doe"
            value={formData.full_name}
            onChange={(e) =>
              setFormData({ ...formData, full_name: e.target.value })
            }
            disabled={isLoading}
            className={`bg-secondary-50 ${
              errors.full_name ? 'border-red-500' : ''
            }`}
            required
          />
          {errors.full_name && (
            <p className="text-sm text-red-500">{errors.full_name}</p>
          )}
        </div>
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="name@example.com"
            value={formData.email}
            onChange={(e) =>
              setFormData({ ...formData, email: e.target.value })
            }
            disabled={isLoading}
            className={`bg-secondary-50 ${
              errors.email ? 'border-red-500' : ''
            }`}
            required
          />
          {errors.email && (
            <p className="text-sm text-red-500">{errors.email}</p>
          )}
        </div>
        <div className="space-y-2">
          <Label htmlFor="phone">Phone</Label>
          <Input
            id="phone"
            type="tel"
            placeholder="+628123456789"
            value={formData.phone}
            onChange={(e) =>
              setFormData({ ...formData, phone: e.target.value })
            }
            disabled={isLoading}
            className={`bg-secondary-50 ${
              errors.phone ? 'border-red-500' : ''
            }`}
            required
          />
          {errors.phone && (
            <p className="text-sm text-red-500">{errors.phone}</p>
          )}
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            placeholder="••••••••"
            value={formData.password}
            onChange={(e) =>
              setFormData({ ...formData, password: e.target.value })
            }
            disabled={isLoading}
            className={`bg-secondary-50 ${
              errors.password ? 'border-red-500' : ''
            }`}
            required
          />
          {errors.password && (
            <p className="text-sm text-red-500">{errors.password}</p>
          )}
        </div>
      </div>
      {errors.submit && (
        <div className="text-sm text-destructive text-center font-medium">
          {errors.submit}
        </div>
      )}
      <Button
        type="submit"
        className="w-full bg-primary-600 hover:bg-primary-700 text-white"
        disabled={isLoading}
      >
        {isLoading && <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />}
        Create account
      </Button>
    </form>
  )
}
