import { useState } from 'react'
import { CycleVisualizer } from './components/CycleVisualizer'
import { ChatInterface } from './components/ChatInterface'
import { ArtifactEditor } from './components/ArtifactEditor'
import { sendMessage } from './api'

function App() {
  const [phase, setPhase] = useState('Initiate')
  const [messages, setMessages] = useState<any[]>([
    { role: 'assistant', content: 'The Cycle is Ridiculous. I am your Guide. What are we building today?' }
  ])
  const [artifact, setArtifact] = useState('# New Project\n\nWaiting for initiation...')
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (content: string) => {
    const newMessages = [...messages, { role: 'user', content }]
    setMessages(newMessages)
    setIsLoading(true)

    try {
      const response = await sendMessage(content, messages)
      setMessages(prev => [...prev, { role: 'assistant', content: response.content }])
      if (response.phase) {
        setPhase(response.phase)
      }
    } catch (error) {
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-void p-8 flex flex-col">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tighter mb-1">
            Grok<span className="text-sigil">-</span>CommIT
          </h1>
          <p className="text-dim text-sm font-mono">COGNITIVE OPERATING SYSTEM v4.0</p>
        </div>
        <div className="text-right">
          <div className="text-neon text-xs font-mono">SYSTEM STATUS: ONLINE</div>
          <div className="text-dim text-xs font-mono">MEMORY: LOCAL</div>
        </div>
      </header>

      <CycleVisualizer currentPhase={phase} />

      <div className="flex-1 grid grid-cols-2 gap-6 min-h-0">
        <ChatInterface messages={messages} onSendMessage={handleSendMessage} isLoading={isLoading} />
        <ArtifactEditor content={artifact} onChange={setArtifact} />
      </div>
    </div>
  )
}

export default App
