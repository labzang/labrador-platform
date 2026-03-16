'use client'

import { useState } from 'react'
import AdminLayout from '@/components/AdminLayout'
import Dashboard from '@/components/Dashboard'
import MatchManagement from '@/components/MatchManagement'
import BettingSystem from '@/components/BettingSystem'
import ProductManagement from '@/components/ProductManagement'
import MemberManagement from '@/components/MemberManagement'

type TabType = 'dashboard' | 'matches' | 'betting' | 'products' | 'members'

export default function V1AdminPage() {
  const [activeTab, setActiveTab] = useState<TabType>('dashboard')

  const content: Record<TabType, React.ReactNode> = {
    dashboard: <Dashboard />,
    matches: <MatchManagement />,
    betting: <BettingSystem />,
    products: <ProductManagement />,
    members: <MemberManagement />,
  }

  return (
    <AdminLayout activeTab={activeTab} onTabChange={setActiveTab}>
      {content[activeTab]}
    </AdminLayout>
  )
}
