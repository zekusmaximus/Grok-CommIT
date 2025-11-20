import React, { useState } from 'react';

interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
}

interface ChatInterfaceProps {
    messages: Message[];
    onSendMessage: (content: string) => void;
    isLoading?: boolean;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ messages, onSendMessage, isLoading }) => {
    const [input, setInput] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;
        onSendMessage(input);
        setInput('');
    };

    return (
        <div className="flex flex-col h-full glass-panel rounded-lg overflow-hidden">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div
                            className={`max-w-[80%] p-3 rounded-lg text-sm
                ${msg.role === 'user'
                                    ? 'bg-dim/20 border border-dim/50 text-white'
                                    : 'bg-void border border-neon/30 text-neon/90 shadow-[0_0_10px_rgba(0,243,255,0.1)]'}
              `}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-void border border-neon/30 text-neon/90 p-3 rounded-lg text-sm shadow-[0_0_10px_rgba(0,243,255,0.1)] animate-pulse">
                            Thinking...
                        </div>
                    </div>
                )}
            </div>
            <form onSubmit={handleSubmit} className="p-4 border-t border-white/10 bg-black/20">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Speak to the Guide..."
                        className="flex-1 bg-void border border-dim/50 rounded px-4 py-2 text-white focus:outline-none focus:border-neon transition-colors"
                    />
                    <button
                        type="submit"
                        className="px-4 py-2 bg-neon/10 border border-neon text-neon rounded hover:bg-neon/20 transition-all uppercase text-xs font-bold tracking-widest"
                    >
                        Send
                    </button>
                </div>
            </form>
        </div>
    );
};
