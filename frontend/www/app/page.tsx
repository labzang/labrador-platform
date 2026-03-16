'use client'

import { useState } from 'react'
import Link from 'next/link'
import {
  Search,
  Cpu,
  Settings,
  Terminal,
  Smartphone,
  BookOpen,
  GitBranch,
  Sparkles,
} from 'lucide-react'
import { cn } from '@/lib/utils'

/**
 * 모바일 퍼스트 AI 교육 블로그 메인 랜딩
 * - Flutter 화면 구성과 동일. 웹은 shadcn 스타일 + 데스크톱에서 가로 여유 있게.
 */
export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')

  const explorerCategories = [
    { href: '#', label: 'AI/ML', icon: Cpu, ariaLabel: 'AI·머신러닝 카테고리' },
    { href: '#', label: '환경설정', icon: Settings, ariaLabel: '환경 설정 카테고리' },
    { href: '#', label: 'FastAPI', icon: Terminal, ariaLabel: 'FastAPI 카테고리' },
    { href: '#', label: 'Flutter', icon: Smartphone, ariaLabel: 'Flutter 카테고리' },
  ]

  const bestThree = [
    {
      href: '#',
      title: '개발환경 설정 한 번에',
      tag: '#환경설정',
      description: 'Python, CUDA, 가상환경부터 IDE까지',
      gradient: 'from-violet-500/20 to-indigo-500/20',
    },
    {
      href: '#',
      title: 'AI 입문 가이드',
      tag: '#AI입문',
      description: '머신러닝·딥러닝 기초와 실습',
      gradient: 'from-amber-500/20 to-orange-500/20',
    },
    {
      href: '#',
      title: 'FastAPI 데이터 흐름',
      tag: '#FastAPI',
      description: 'API 설계와 요청 흐름도',
      gradient: 'from-emerald-500/20 to-teal-500/20',
    },
  ]

  const flowLinks = [
    { title: '데이터 파이프라인', tag: '#ETL', href: '#' },
    { title: '모델 아키텍처', tag: '#NeuralNet', href: '#' },
    { title: 'API 요청 흐름', tag: '#FastAPI', href: '#' },
  ]

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      // TODO: 검색 라우트 또는 Fuse.js 연동
      console.log('Search:', searchQuery)
    }
  }

  return (
    <div className="min-h-screen overflow-x-hidden bg-muted/30">
      {/* 중앙 컨테이너: 모바일 500px, 웹에서 가로 여유 (max-w-2xl) */}
      <div className="mx-auto min-h-screen max-w-[500px] bg-card shadow-sm md:max-w-2xl md:rounded-b-lg md:border md:border-border md:border-t-0">
        {/* Hero Section - 구글 스타일 검색 (shadcn 토큰) */}
        <header className="px-4 pt-8 pb-6 md:px-8 md:pt-10">
          <div className="mb-6 flex items-center justify-center gap-2">
            <Sparkles className="h-6 w-6 text-foreground/80" aria-hidden />
            <span className="text-lg font-semibold text-foreground">AI 강의 자료실</span>
          </div>
          <p className="mb-4 text-center text-sm text-muted-foreground">
            무엇을 도와드릴까요?
          </p>
          <form onSubmit={handleSearch} className="relative">
            <Search
              className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground"
              aria-hidden
            />
            <input
              type="search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="키워드 또는 태그로 검색..."
              className={cn(
                'w-full rounded-full border border-input bg-background py-3.5 pl-12 pr-4',
                'text-base text-foreground placeholder:text-muted-foreground',
                'focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/20',
                'transition-shadow hover:shadow-sm'
              )}
              aria-label="검색"
            />
          </form>
        </header>

        {/* Explorer Section - 주요 카테고리 (shadcn card/muted) */}
        <section className="px-4 pb-8 md:px-8" aria-label="주요 카테고리">
          <h2 className="mb-4 text-sm font-semibold text-foreground">
            주요 카테고리
          </h2>
          <div className="grid grid-cols-4 gap-3 md:gap-4">
            {explorerCategories.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.label}
                  href={item.href}
                  aria-label={item.ariaLabel}
                  className={cn(
                    'flex flex-col items-center gap-2 rounded-lg border border-border bg-muted/50 p-4',
                    'text-card-foreground transition-colors',
                    'hover:bg-muted hover:border-border',
                    'active:bg-muted focus-visible:ring-2 focus-visible:ring-ring',
                    'touch-manipulation'
                  )}
                >
                  <span className="flex h-12 w-12 items-center justify-center rounded-full border border-border bg-card shadow-sm">
                    <Icon className="h-6 w-6 text-muted-foreground" />
                  </span>
                  <span className="text-xs font-medium leading-tight text-muted-foreground">
                    {item.label}
                  </span>
                </Link>
              )
            })}
          </div>
        </section>

        {/* Featured Cards - Best 3 (shadcn card) */}
        <section className="px-4 pb-8 md:px-8" aria-label="학생들이 가장 많이 찾는 자료">
          <h2 className="mb-4 text-sm font-semibold text-foreground">
            Best 3
          </h2>
          <ul className="flex flex-col gap-4">
            {bestThree.map((card) => (
              <li key={card.title}>
                <Link
                  href={card.href}
                  className={cn(
                    'flex gap-4 rounded-lg border border-border bg-card p-4',
                    'shadow-sm transition-all hover:border-border hover:shadow-md',
                    'active:scale-[0.99] touch-manipulation',
                    'focus-visible:ring-2 focus-visible:ring-ring'
                  )}
                >
                  <div
                    className={cn(
                      'h-20 w-24 shrink-0 rounded-md bg-gradient-to-br',
                      card.gradient,
                      'flex items-center justify-center'
                    )}
                  >
                    <BookOpen className="h-8 w-8 text-muted-foreground/70" aria-hidden />
                  </div>
                  <div className="min-w-0 flex-1">
                    <span className="text-xs font-medium text-muted-foreground">
                      {card.tag}
                    </span>
                    <h3 className="mt-0.5 font-semibold text-card-foreground line-clamp-1">
                      {card.title}
                    </h3>
                    <p className="mt-1 text-sm text-muted-foreground line-clamp-1">
                      {card.description}
                    </p>
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        </section>

        {/* 데이터 흐름도 & 아키텍처 (shadcn 스타일) */}
        <section className="px-4 pb-24 md:px-8">
          <h2 className="mb-4 text-sm font-semibold text-foreground">
            데이터 흐름도 & 아키텍처
          </h2>
          <div className="flex flex-col gap-3">
            {flowLinks.map((item) => (
              <Link
                key={item.title}
                href={item.href}
                className={cn(
                  'flex items-center justify-between rounded-lg border border-border bg-muted/30 px-4 py-3',
                  'transition-colors hover:bg-muted',
                  'focus-visible:ring-2 focus-visible:ring-ring'
                )}
              >
                <div className="flex items-center gap-3">
                  <GitBranch className="h-5 w-5 text-muted-foreground" aria-hidden />
                  <div>
                    <span className="text-xs text-muted-foreground">{item.tag}</span>
                    <p className="font-medium text-card-foreground">{item.title}</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>

      {/* App Promotion - 스티키 하단 (웹에서도 컨테이너 너비에 맞춤) */}
      <div
        className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-card/95 px-4 py-3 backdrop-blur-sm"
        role="banner"
        aria-label="앱 설치 안내"
      >
        <div className="mx-auto flex max-w-[500px] items-center justify-between gap-4 md:max-w-2xl">
          <p className="text-sm font-medium text-foreground">
            전용 앱으로 더 편하게 보세요
          </p>
          <Link
            href="#"
            className={cn(
              'shrink-0 rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground',
              'hover:bg-primary/90 active:bg-primary transition-colors',
              'touch-manipulation focus-visible:ring-2 focus-visible:ring-ring'
            )}
          >
            설치하기
          </Link>
        </div>
      </div>
    </div>
  )
}
