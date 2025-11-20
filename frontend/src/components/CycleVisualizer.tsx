import React from 'react';

interface CycleVisualizerProps {
    currentPhase: string;
}

const PHASES = ["Initiate", "Challenge", "Implement", "Document", "Review"];

export const CycleVisualizer: React.FC<CycleVisualizerProps> = ({ currentPhase }) => {
    return (
        <div className="flex items-center justify-between w-full p-4 mb-4 glass-panel rounded-lg">
            {PHASES.map((phase, index) => {
                const isActive = phase === currentPhase;
                const isPast = PHASES.indexOf(currentPhase) > index;

                return (
                    <div key={phase} className="flex flex-col items-center relative z-10">
                        <div
                            className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-500
                ${isActive ? 'border-neon bg-neon/20 text-neon shadow-[0_0_15px_rgba(0,243,255,0.5)]' :
                                    isPast ? 'border-sigil bg-sigil/10 text-sigil' : 'border-dim text-dim'}
              `}
                        >
                            {index + 1}
                        </div>
                        <span className={`mt-2 text-xs font-mono uppercase tracking-wider ${isActive ? 'text-neon' : 'text-dim'}`}>
                            {phase}
                        </span>

                        {/* Connector Line */}
                        {index < PHASES.length - 1 && (
                            <div className={`absolute top-5 left-1/2 w-full h-0.5 -z-10 
                ${isPast ? 'bg-sigil' : 'bg-dim/30'}`}
                                style={{ width: 'calc(100% + 2rem)', left: '50%' }}
                            />
                        )}
                    </div>
                );
            })}
        </div>
    );
};
