// src/pages/auth/RegisterPage.tsx
import { RegisterForm } from '@/components/auth/RegisterForm'
import { AuthCard } from '@/components/auth/AuthCard'
import { Link } from 'react-router-dom'

export const RegisterPage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-secondary-50 to-secondary-100 px-4 py-8">
      <AuthCard
        title="Create an account"
        description="Enter your information to create your account"
        footer={
          <p className="text-center text-sm text-secondary-500">
            Already have an account?{' '}
            <Link
              to="/login"
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              Sign in
            </Link>
          </p>
        }
      >
        <RegisterForm />
      </AuthCard>
    </div>
  )
}
