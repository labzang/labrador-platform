'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Loader2, Bot, User, Link, GitBranch } from 'lucide-react'
import { chatAPI, Message, DocumentSource } from '@/api/chatAPI'

type ChatMode = 'langchain' | 'langgraph'

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '스팸메일 판독기?',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [chatMode, setChatMode] = useState<ChatMode>('langchain')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // 컴포넌트 마운트 시 입력 필드에 자동 포커스
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    const messageContent = input.trim()
    setInput('')
    setIsLoading(true)

    try {
      // "상품추천" 키워드가 포함된 경우 상품추천 API 호출
      if (messageContent.includes('상품추천') || messageContent.includes('상품 추천')) {
        const response = await chatAPI.recommendProducts(messageContent)

        const assistantMessage: Message = {
          role: 'assistant',
          content: typeof response === 'string'
            ? response
            : JSON.stringify(response, null, 2),
          timestamp: new Date(),
        }

        setMessages((prev) => [...prev, assistantMessage])
      } else {
        // 선택된 모드에 따라 다른 API 엔드포인트 호출
        const response = chatMode === 'langchain'
          ? await chatAPI.sendMessage(messageContent, 3)
          : await chatAPI.sendGraphMessage(messageContent, 3)

        const assistantMessage: Message = {
          role: 'assistant',
          content: response.answer,
          timestamp: new Date(),
          sources: response.retrieved_documents?.map((doc) => ({
            content: doc.content,
            metadata: doc.metadata,
          })) || [],
        }

        setMessages((prev) => [...prev, assistantMessage])
      }
    } catch (error: any) {
      console.error('Error sending message:', error)

      let errorContent = '죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.'

      if (error.response?.status === 404) {
        errorContent = '서버에서 해당 엔드포인트를 찾을 수 없습니다. 백엔드 서버를 확인해주세요.'
      } else if (error.response?.status === 422) {
        errorContent = '요청 데이터 형식에 문제가 있습니다.'
      } else if (error.code === 'ECONNREFUSED' || error.message?.includes('Network Error')) {
        errorContent = '백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.'
      }

      const errorMessage: Message = {
        role: 'assistant',
        content: errorContent,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }


  return (
    <div className="flex flex-col h-[600px] bg-white rounded-lg shadow-lg overflow-hidden">
      {/* 모드 선택 버튼 */}
      <div className="flex-shrink-0 p-4 bg-gray-50 border-b border-gray-200">
        <div className="flex gap-2">
          <button
            onClick={() => setChatMode('langchain')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${chatMode === 'langchain'
              ? 'bg-blue-500 text-white shadow-md'
              : 'bg-white text-gray-600 border border-gray-300 hover:bg-gray-50'
              }`}
          >
            <Link className="w-4 h-4" />
            LangChain
          </button>
          <button
            onClick={() => setChatMode('langgraph')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${chatMode === 'langgraph'
              ? 'bg-green-500 text-white shadow-md'
              : 'bg-white text-gray-600 border border-gray-300 hover:bg-gray-50'
              }`}
          >
            <GitBranch className="w-4 h-4" />
            LangGraph
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          {chatMode === 'langchain'
            ? '🔗 LangChain RAG 체인을 사용합니다 → /api/chain'
            : '🌿 LangGraph 워크플로우를 사용합니다 → /api/graph'
          }
        </p>
      </div>

      {/* 메시지 영역 */}
      <div
        className="flex-1 overflow-y-auto p-4 space-y-4 chat-messages"
        style={{
          paddingBottom: '100px' // 입력 영역 공간 확보
        }}
      >
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex items-start gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
          >
            {message.role === 'assistant' && (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
            )}

            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${message.role === 'user'
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-gray-800'
                }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>

              {/* 소스 문서 표시 */}
              {message.sources && message.sources.length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-300">
                  <p className="text-xs font-semibold mb-1">참조 문서:</p>
                  {message.sources.map((source, idx) => (
                    <div
                      key={idx}
                      className="text-xs bg-white bg-opacity-50 rounded p-2 mb-1"
                    >
                      <p className="line-clamp-2">{source.content}</p>
                    </div>
                  ))}
                </div>
              )}

              {message.timestamp && (
                <p className="text-xs mt-1 opacity-70">
                  {message.timestamp.toLocaleTimeString('ko-KR', {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </p>
              )}
            </div>

            {message.role === 'user' && (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
                <User className="w-5 h-5 text-gray-600" />
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="bg-gray-100 rounded-lg px-4 py-2">
              <Loader2 className="w-5 h-5 animate-spin text-primary-500" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* 입력 영역 */}
      <div
        className="border-t border-gray-200 p-4 bg-white chat-input-area shadow-lg flex-shrink-0"
      >
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            onKeyDown={handleKeyPress}
            placeholder="메시지를 입력하세요..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 cursor-text text-gray-900"
            disabled={isLoading}
            autoFocus
            tabIndex={0}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
            <span>전송</span>
          </button>
        </div>
      </div>
    </div>
  )
}

