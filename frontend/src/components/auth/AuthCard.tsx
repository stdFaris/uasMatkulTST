import * as React from 'react'
import { cn } from '@/lib/utils'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

interface AuthCardProps extends React.HTMLAttributes<HTMLDivElement> {
  title: string
  description?: string
  footer?: React.ReactNode
  children: React.ReactNode
}

export function AuthCard({
  title,
  description,
  footer,
  children,
  className,
  ...props
}: AuthCardProps) {
  return (
    <Card className={cn('w-full max-w-lg', className)} {...props}>
      <CardHeader className="space-y-1 text-center">
        <CardTitle className="text-3xl font-display font-semibold">
          {title}
        </CardTitle>
        {description && (
          <CardDescription className="text-sm text-secondary-500">
            {description}
          </CardDescription>
        )}
      </CardHeader>
      <CardContent>{children}</CardContent>
      {footer && <CardFooter>{footer}</CardFooter>}
    </Card>
  )
}
