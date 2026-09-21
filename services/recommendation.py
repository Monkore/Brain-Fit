import logging
from typing import List
from models.user import User
from models.checkin import Checkin
from models.activity import Activity
from core.constants import ModuleType
from core.database import get_connection

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    Age-Adaptive Cognitive Prescription Engine.
    Inputs: Age, Mood, Stress, Sleep, Energy, Preferences.
    Outputs: Activity recommendations (Daily Plan).
    """

    @staticmethod
    def _get_activities_by_module(module_type: str) -> List[Activity]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM activities WHERE module_type = ?", (module_type,))
            rows = cursor.fetchall()
            return [Activity(**dict(r)) for r in rows]
            
    @staticmethod
    def generate_daily_plan(user: User, checkin: Checkin) -> List[Activity]:
        plan = []
        
        # Rule 1: High Stress -> Prioritize Meditation / Breathing
        if checkin.stress >= 7 or checkin.anxiety >= 7:
            logger.info("High stress detected. Prioritizing Meditation and Breathing.")
            meditations = RecommendationEngine._get_activities_by_module(ModuleType.MEDITATION)
            breathings = RecommendationEngine._get_activities_by_module(ModuleType.BREATHING)
            if meditations: plan.append(meditations[0])
            if breathings: plan.append(breathings[0])
            # Only add one light cognitive task
            memories = RecommendationEngine._get_activities_by_module(ModuleType.MEMORY)
            if memories: plan.append(memories[0])
            return plan

        # Rule 2: Poor Sleep -> Recovery Day
        if checkin.sleep_hours < 5.0 or checkin.energy <= 4:
            logger.info("Poor sleep or low energy detected. Prescribing Recovery Day.")
            yogas = RecommendationEngine._get_activities_by_module(ModuleType.YOGA)
            if yogas: plan.append(yogas[0])
            breathings = RecommendationEngine._get_activities_by_module(ModuleType.BREATHING)
            if breathings: plan.append(breathings[0])
            return plan

        # Normal Day: Balanced Cognitive + Physical
        logger.info("Normal day. Prescribing balanced cognitive and physical plan.")
        
        # 1. Processing Speed (Highest Priority Module)
        speeds = RecommendationEngine._get_activities_by_module(ModuleType.PROCESSING_SPEED)
        if speeds: plan.append(speeds[0])

        # 2. Memory
        memories = RecommendationEngine._get_activities_by_module(ModuleType.MEMORY)
        if memories: plan.append(memories[0])

        # 3. Dual-Task (Flagship Module)
        dual_tasks = RecommendationEngine._get_activities_by_module(ModuleType.DUAL_TASK)
        if dual_tasks: plan.append(dual_tasks[0])
        
        return plan
