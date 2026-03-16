'use client'

import { useEffect } from 'react'

/**
 * 루트 에러 바운더리 (App Router)
 * 하위에서 throw 된 에러를 잡아 표시
 */
export default function RootError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error('App error:', error)
  }, [error])

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <h1 className="text-xl font-bold text-gray-900">오류가 발생했습니다</h1>
      <p className="mt-2 text-gray-600 text-center text-sm max-w-md">
        {error.message || '일시적인 오류입니다. 다시 시도해 주세요.'}
      </p>
      <button
        onClick={reset}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        다시 시도
      </button>
    </div>
  )
}
