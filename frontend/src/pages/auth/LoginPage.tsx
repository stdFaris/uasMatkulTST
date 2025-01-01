// src/pages/auth/LoginPage.tsx
import { LoginForm } from '@/components/auth/LoginForm'
import { AuthCard } from '@/components/auth/AuthCard'
import { Link } from 'react-router-dom'

export const LoginPage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-secondary-50 to-secondary-100 px-4 py-8">
      <AuthCard
        title="Welcome back"
        description="Enter your credentials to access your account"
        footer={
          <p className="text-center text-sm text-secondary-500">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              Create an account
            </Link>
          </p>
        }
      >
        <LoginForm />
      </AuthCard>
    </div>
  )
}
