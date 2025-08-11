"""
Physical Context Assessment Agent

This agent evaluates physical work environment preferences,
mobility requirements, and physical capabilities for career planning.
"""

import json
from typing import Dict, Any

class PhysicalContextAgent:
    """Agent for physical context and work environment assessment"""
    
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Work Environment Specialist"
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Process user interaction for physical context assessment"""
        
        try:
            prompt = f"""
            As a Work Environment Specialist, assess physical work preferences and requirements.
            
            User response: "{user_input}"
            
            Focus areas:
            - Work environment preferences (office, remote, outdoor, etc.)
            - Physical activity requirements
            - Travel tolerance and preferences
            - Technology comfort level
            - Workspace organization preferences
            
            Respond with JSON:
            {{
                "message": "Professional response about physical work preferences",
                "assessment_data": {{
                    "work_environment": "preference if assessed",
                    "physical_activity": "tolerance if assessed",
                    "travel_preference": "level if assessed",
                    "technology_comfort": "level if assessed",
                    "workspace_style": "preference if assessed"
                }},
                "assessment_complete": false
            }}
            """
            
            response = await self.llm.ainvoke(prompt)
            result = self._parse_response(response.content)
            
            return {
                "success": True,
                "message": result["message"],
                "assessment_data": result.get("assessment_data"),
                "assessment_complete": result.get("assessment_complete", False)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Let's discuss your ideal work environment. Do you prefer office settings, remote work, or something else?"
            }
    
    def _parse_response(self, response_content: str) -> Dict[str, Any]:
        try:
            cleaned = response_content.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:-3]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:-3]
            return json.loads(cleaned)
        except:
            return {
                "message": response_content or "What type of work environment energizes you most?",
                "assessment_data": {},
                "assessment_complete": False
            }
