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
      <AlertDialogContent className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md mx-auto p-6 rounded-lg shadow-soft bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
        <AlertDialogHeader className="space-y-4">
          <AlertDialogTitle className="text-xl font-display font-semibold text-error-600 dark:text-error-500">
            Partner Tidak Tersedia
          </AlertDialogTitle>
          <AlertDialogDescription className="text-base text-secondary-600 dark:text-secondary-300">
            Partner tidak tersedia pada waktu yang dipilih. Silakan pilih waktu
            lain.
          </AlertDialogDescription>
        </AlertDialogHeader>

        <AlertDialogFooter className="mt-8 flex justify-end">
          <AlertDialogAction
            onClick={onClose}
            className="w-full sm:w-auto min-w-[120px] px-6 py-2.5 text-base font-medium bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
          >
            Pilih Waktu Lain
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
