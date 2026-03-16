import Link from 'next/link'

/**
 * App Router 404 페이지
 */
export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <h1 className="text-4xl font-bold text-gray-900">404</h1>
      <p className="mt-2 text-gray-600">요청한 페이지를 찾을 수 없습니다.</p>
      <Link
        href="/"
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        홈으로 돌아가기
      </Link>
    </div>
  )
}
