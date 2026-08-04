import { useState, useRef, useEffect } from "react"
import axios from "axios"
import ReactMarkdown from "react-markdown"

const API_URL = "http://127.0.0.1:8000"

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  // Auto-scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const sendQuery = async () => {
    if (!input.trim() || loading) return

    const userMessage = { role: "user", content: input }
    setMessages(prev => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/query`, {
        query: input,
        history: [...messages, userMessage]
      })
      const agentMessage = {
        role: "agent",
        content: response.data.answer
      }
      setMessages(prev => [...prev, agentMessage])
    } catch (error) {
      setMessages(prev => [...prev, {
        role: "agent",
        content: "Something went wrong. Please try again."
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendQuery()
    }
  }

  // Markdown component overrides for agent messages
  const markdownComponents = {
    p: ({ children }) => (
      <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>
    ),
    a: ({ href, children }) => (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-indigo-400 underline underline-offset-2 hover:text-indigo-300 transition-colors duration-150"
      >
        {children}
      </a>
    ),
    strong: ({ children }) => (
      <strong className="font-semibold text-white">{children}</strong>
    ),
    em: ({ children }) => (
      <em className="italic text-gray-300">{children}</em>
    ),
    ul: ({ children }) => (
      <ul className="list-disc list-inside space-y-1 mb-2 text-gray-200">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal list-inside space-y-1 mb-2 text-gray-200">{children}</ol>
    ),
    li: ({ children }) => (
      <li className="leading-relaxed">{children}</li>
    ),
    code: ({ inline, children }) =>
      inline ? (
        <code className="bg-black/40 text-indigo-300 px-1.5 py-0.5 rounded text-xs font-mono">
          {children}
        </code>
      ) : (
        <pre className="bg-black/50 border border-white/10 rounded-xl p-3 my-2 overflow-x-auto">
          <code className="text-indigo-200 text-xs font-mono whitespace-pre">{children}</code>
        </pre>
      ),
    blockquote: ({ children }) => (
      <blockquote className="border-l-2 border-indigo-400/50 pl-3 my-2 text-gray-400 italic">
        {children}
      </blockquote>
    ),
    h1: ({ children }) => <h1 className="text-lg font-semibold text-white mb-2">{children}</h1>,
    h2: ({ children }) => <h2 className="text-base font-semibold text-white mb-2">{children}</h2>,
    h3: ({ children }) => <h3 className="text-sm font-semibold text-white mb-1">{children}</h3>,
  }

  return (
    <div className="min-h-screen bg-[#0b0b0f] text-white flex flex-col items-center">

      {/* Header */}
      <header className="w-full max-w-4xl px-4 py-5 flex items-center border-b border-white/10">
        <h1 className="text-xl font-semibold tracking-tight bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
          ResearchAgent
        </h1>
      </header>

      {/* Messages */}
      <main className="w-full max-w-4xl flex-1 overflow-y-auto px-4 py-6 space-y-5 pb-44 scroll-smooth">
        {messages.length === 0 && (
          <div className="relative text-center text-gray-400 mt-28 flex flex-col items-center">
            <div className="absolute h-28 w-64 rounded-full bg-indigo-500/20 blur-3xl animate-pulse" />
            <p className="relative text-5xl font-semibold tracking-tight bg-gradient-to-r from-indigo-300 to-purple-300 bg-clip-text text-transparent">
              Search the web. Run code. Get answers.
            </p>
            <div className="relative mt-7 flex flex-wrap items-center justify-center gap-2 text-xs text-gray-300">
              <span className="px-3 py-1 rounded-full border border-white/10 bg-white/5">🌐 Web Search</span>
              <span className="px-3 py-1 rounded-full border border-white/10 bg-white/5">🐍 Run Code</span>
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in duration-200`}
          >
            <div className={`max-w-2xl ${msg.role === "user" ? "items-end" : "items-start"} flex flex-col`}>
              <span className="mb-1 px-1 text-[11px] uppercase tracking-wide text-gray-500">
                {msg.role === "user" ? "You" : "Agent"}
              </span>
              <div className={`w-full px-4 py-3 rounded-2xl text-sm transition-all duration-200 ${
                msg.role === "user"
                  ? "bg-gradient-to-br from-indigo-500 to-violet-500 text-white"
                  : "bg-[#17171d] border-l border-indigo-400/60 text-gray-100"
              }`}>
                {msg.role === "agent" ? (
                  <ReactMarkdown components={markdownComponents}>
                    {msg.content}
                  </ReactMarkdown>
                ) : (
                  msg.content
                )}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start animate-in fade-in duration-200">
            <div className="flex flex-col items-start">
              <span className="mb-1 px-1 text-[11px] uppercase tracking-wide text-gray-500">Agent</span>
              <div className="bg-[#17171d] border-l border-indigo-400/60 px-4 py-3 rounded-2xl">
                <div className="flex items-center gap-1.5">
                  <span className="h-1.5 w-1.5 rounded-full bg-indigo-300 animate-bounce" />
                  <span className="h-1.5 w-1.5 rounded-full bg-indigo-300 animate-bounce [animation-delay:120ms]" />
                  <span className="h-1.5 w-1.5 rounded-full bg-indigo-300 animate-bounce [animation-delay:240ms]" />
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>

      {/* Input */}
      <footer className="fixed bottom-0 w-full max-w-4xl px-4 pb-6">
        <div className="flex items-end gap-2 bg-black/35 backdrop-blur-xl border border-white/10 rounded-2xl px-4 py-3 shadow-2xl transition-all duration-200">
          <textarea
            className="flex-1 bg-transparent field-sizing-content resize-none outline-none text-sm text-white placeholder-gray-500 max-h-[7.5rem]"
            rows={1}
            placeholder="Ask anything..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            onClick={sendQuery}
            disabled={loading || !input.trim()}
            className="bg-gradient-to-r from-indigo-500 to-violet-500 hover:from-indigo-400 hover:to-violet-400 disabled:from-gray-600 disabled:to-gray-600 disabled:text-gray-300 disabled:opacity-70 text-white text-sm px-4 py-2 rounded-xl transition-all duration-200"
          >
            Send
          </button>
        </div>
        <p className="text-center text-xs text-gray-500 mt-2">Enter to send · Shift+Enter for new line</p>
      </footer>

    </div>
  )
}
