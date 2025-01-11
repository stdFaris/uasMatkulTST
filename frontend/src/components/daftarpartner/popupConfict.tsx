import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'

interface BookingConflictAlertProps {
  isOpen: boolean
  onClose: () => void
  conflictDetails: {
    startTime: string
    endTime: string
  } | null
}

export function BookingConflictAlert({
  isOpen,
  onClose,
  conflictDetails,
}: BookingConflictAlertProps) {
  if (!conflictDetails) return null

  return (
    <AlertDialog open={isOpen} onOpenChange={onClose}>
      <AlertDialogContent className="sm:max-w-[425px] bg-white dark:bg-gray-800">
        <AlertDialogHeader>
          <AlertDialogTitle className="text-xl font-semibold text-red-600 dark:text-red-400">
            Partner Not Available
          </AlertDialogTitle>
          <AlertDialogDescription className="text-gray-600 dark:text-gray-300">
            The partner is not available during this time period. Please select
            a different time slot.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogAction
            className="bg-primary-600 hover:bg-primary-700 text-white"
            onClick={onClose}
          >
            Choose Another Time
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
