import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent } from '@/components/ui/card'
import { RegisterForm } from '@/components/auth/register-form'
import { useAuth } from '@/hooks/useAuth'

export default function RegisterPage() {
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard')
    }
  }, [isAuthenticated, navigate])

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-b from-primary-50 to-white">
      <Card className="w-full max-w-md">
        <CardContent className="pt-6">
          <RegisterForm />
        </CardContent>
      </Card>
    </div>
  )
}
