/**
 * 루트 로딩 UI (App Router)
 * 레이아웃/페이지 로딩 시 자동 표시
 */
export default function RootLoading() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="flex flex-col items-center gap-3">
        <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm text-gray-600">로딩 중...</p>
      </div>
    </div>
  )
}
