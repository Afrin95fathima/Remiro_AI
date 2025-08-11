"""Track Record Assessment Agent"""
import json
from typing import Dict, Any

class TrackRecordAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Background Assessment Specialist"
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prompt = f"""As a Background Assessment Specialist, evaluate experience and achievements.
            User response: "{user_input}"
            Respond with JSON: {{"message": "response", "assessment_data": {{"experience": "summary", "achievements": "list"}}, "assessment_complete": false}}"""
            
            response = await self.llm.ainvoke(prompt)
            result = json.loads(response.content.strip().replace("```json", "").replace("```", ""))
            return {"success": True, "message": result["message"], "assessment_data": result.get("assessment_data"), "assessment_complete": result.get("assessment_complete", False)}
        except:
            return {"success": False, "message": "Could you share your professional background and key achievements?"}
