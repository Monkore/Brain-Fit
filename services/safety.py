import logging
from typing import List
from models.user import User
from models.checkin import Checkin
from models.performance import PerformanceLog
from models.activity import Activity
from core.constants import FeedbackEnergy, ModuleType

logger = logging.getLogger(__name__)

class SafetyEngine:
    """
    Monitors fatigue and performance in real-time to avoid overloading older users.
    Prioritizes safety and consistency over rapid progress.
    """
    
    @staticmethod
    def evaluate_mid_session(user: User, remaining_activities: List[Activity], current_log: PerformanceLog) -> List[Activity]:
        """
        Called after every activity to determine if the rest of the session should be modified.
        """
        
        # If user reports Low energy during a session, truncate strenuous activities.
        if current_log.energy_after == FeedbackEnergy.LOW:
            logger.warning(f"User reported LOW energy post-activity. Safety Engine engaging.")
            
            # Filter out demanding cognitive or physical tasks
            safe_modules = [ModuleType.MEDITATION, ModuleType.BREATHING, ModuleType.YOGA]
            modified_plan = [act for act in remaining_activities if act.module_type in safe_modules]
            
            # If nothing left that is safe, add a breathing exercise to cool down
            if not modified_plan:
                # In a real implementation, we would query the DB for a breathing exercise here
                logger.info("Session truncated for safety. Suggesting immediate cooldown.")
                
            return modified_plan
            
        return remaining_activities
