"""Aspirations Assessment Agent"""
import json
from typing import Dict, Any

class AspirationsAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Aspirations Specialist"
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prompt = f"""As an Aspirations Specialist, explore career goals and future vision.
            User response: "{user_input}"
            Respond with JSON: {{"message": "response", "assessment_data": {{"short_term_goals": "list", "long_term_vision": "description"}}, "assessment_complete": false}}"""
            
            response = await self.llm.ainvoke(prompt)
            result = json.loads(response.content.strip().replace("```json", "").replace("```", ""))
            return {"success": True, "message": result["message"], "assessment_data": result.get("assessment_data"), "assessment_complete": result.get("assessment_complete", False)}
        except:
            return {"success": False, "message": "What are your career aspirations and long-term goals?"}
