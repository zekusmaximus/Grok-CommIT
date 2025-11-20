from .models import Cycle

class CommITEngine:
    PHASES = ["Initiate", "Challenge", "Implement", "Document", "Review"]
    
    @staticmethod
    def advance_phase(cycle: Cycle) -> Cycle:
        current_index = CommITEngine.PHASES.index(cycle.phase)
        if current_index < len(CommITEngine.PHASES) - 1:
            cycle.phase = CommITEngine.PHASES[current_index + 1]
        else:
            cycle.phase = "Complete" # Or loop back?
        return cycle

    @staticmethod
    def get_next_phase(current_phase: str) -> str:
        try:
            current_index = CommITEngine.PHASES.index(current_phase)
            if current_index < len(CommITEngine.PHASES) - 1:
                return CommITEngine.PHASES[current_index + 1]
        except ValueError:
            pass
        return "Complete"
