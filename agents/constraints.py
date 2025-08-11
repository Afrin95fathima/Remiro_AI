"""Constraints Assessment Agent"""
import json
from typing import Dict, Any

class ConstraintsAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Constraints Analysis Specialist"
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prompt = f"""As a Constraints Analysis Specialist, identify limitations and requirements.
            User response: "{user_input}"
            Respond with JSON: {{"message": "response", "assessment_data": {{"constraints": "list", "requirements": "list"}}, "assessment_complete": false}}"""
            
            response = await self.llm.ainvoke(prompt)
            result = json.loads(response.content.strip().replace("```json", "").replace("```", ""))
            return {"success": True, "message": result["message"], "assessment_data": result.get("assessment_data"), "assessment_complete": result.get("assessment_complete", False)}
        except:
            return {"success": False, "message": "Are there any constraints or requirements I should consider for your career path?"}
