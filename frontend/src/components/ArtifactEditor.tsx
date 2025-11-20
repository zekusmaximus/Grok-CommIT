import React from 'react';

interface ArtifactEditorProps {
    content: string;
    onChange?: (content: string) => void;
}

export const ArtifactEditor: React.FC<ArtifactEditorProps> = ({ content, onChange }) => {
    return (
        <div className="flex flex-col h-full glass-panel rounded-lg overflow-hidden">
            <div className="p-2 border-b border-white/10 bg-black/20 flex justify-between items-center">
                <span className="text-xs font-mono text-dim uppercase">Artifact Buffer</span>
                <div className="flex gap-2">
                    <div className="w-2 h-2 rounded-full bg-red-500/50"></div>
                    <div className="w-2 h-2 rounded-full bg-yellow-500/50"></div>
                    <div className="w-2 h-2 rounded-full bg-green-500/50"></div>
                </div>
            </div>
            <textarea
                className="flex-1 bg-void/50 p-4 text-sm font-mono text-gray-300 focus:outline-none resize-none"
                value={content}
                onChange={(e) => onChange && onChange(e.target.value)}
                spellCheck={false}
            />
        </div>
    );
};
