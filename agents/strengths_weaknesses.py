"""
Strengths and Weaknesses Assessment Agent
"""

import json
from typing import Dict, Any

class StrengthsWeaknessesAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Strengths & Weaknesses Specialist"
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prompt = f"""As a Strengths & Weaknesses Specialist, assess personal strengths and development areas.
            User response: "{user_input}"
            Respond with JSON: {{"message": "response", "assessment_data": {{"strengths": "list", "weaknesses": "areas"}}, "assessment_complete": false}}"""
            
            response = await self.llm.ainvoke(prompt)
            result = json.loads(response.content.strip().replace("```json", "").replace("```", ""))
            return {"success": True, "message": result["message"], "assessment_data": result.get("assessment_data"), "assessment_complete": result.get("assessment_complete", False)}
        except:
            return {"success": False, "message": "What would you consider your greatest professional strengths?"}
    
    def _parse_response(self, content): return {"message": content, "assessment_data": {}, "assessment_complete": False}
