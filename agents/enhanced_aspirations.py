"""
Enhanced Aspirations Agent - Advanced Career Assessment

This agent explores long-term goals and user's vision for their future career
through empathetic conversation and personalized exploration.
"""

from typing import Dict, Any, List, Optional
from agents.enhanced_base_agent import EnhancedBaseAgent
import json

class AspirationsAgent(EnhancedBaseAgent):
    """🎯 Aspirations Agent - Explores career goals, ambitions, and future vision"""
    
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            agent_name="Career Aspirations Counselor",
            assessment_type="aspirations",
            core_domain="Long-term goals and career vision"
        )
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        """Return the 3 predefined questions for aspirations assessment"""
        return [
            {
                "id": "aspirations_q1",
                "question": "Let's dream a little! Fast forward five years and your career is absolutely crushing it - like, you're living your best professional life. What's your typical Tuesday looking like?",
                "context": "vision",
                "purpose": "Visualize ideal future career state"
            },
            {
                "id": "aspirations_q2",
                "question": "If you could have any job title or role in the world - like, go completely wild with your ambitions - what would make you feel like you've really 'made it'?",
                "context": "ambition",
                "purpose": "Identify career ceiling and ambition level"
            },
            {
                "id": "aspirations_q3",
                "question": "Okay, bringing it back to reality for a sec - what's the very next thing you could actually do (like, this month or next) that would get you one step closer to that dream?",
                "context": "milestone",
                "purpose": "Assess goal-setting and planning capability"
            }
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        """Analyze user responses to determine aspirations profile"""
        
        try:
            analysis_prompt = f"""
            As a Career Aspirations Counselor, analyze these responses:
            
            1. Five-year career vision: {responses[0] if len(responses) > 0 else 'Not provided'}
            2. Ultimate career ambition: {responses[1] if len(responses) > 1 else 'Not provided'}
            3. Next concrete step: {responses[2] if len(responses) > 2 else 'Not provided'}
            
            Provide JSON analysis:
            {{
                "profile_clarity": "clear" or "unclear",
                "vision_clarity": "crystal_clear" or "general_direction" or "exploring",
                "ambition_level": "high" or "medium" or "low",
                "goal_specificity": "specific" or "general" or "vague",
                "planning_capability": "strong" or "moderate" or "needs_development",
                "career_focus": ["main career areas of interest"],
                "timeline_awareness": "realistic" or "optimistic" or "unclear",
                "key_insights": ["insights about their aspirations"],
                "potential_challenges": ["challenges they may face"],
                "success_factors": ["what will drive their success"],
                "summary": "aspirations profile summary"
            }}
            """
            
            response = self.llm.invoke([{"role": "user", "content": analysis_prompt}])
            
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                return self._create_fallback_analysis(responses)
                
        except Exception as e:
            return self._create_fallback_analysis(responses)
    
    def _create_fallback_analysis(self, responses: List[str]) -> Dict[str, Any]:
        """Create fallback analysis"""
        return {
            "profile_clarity": "clear" if responses else "unclear",
            "vision_clarity": "general_direction",
            "ambition_level": "medium",
            "goal_specificity": "general",
            "planning_capability": "moderate",
            "career_focus": ["Professional growth"],
            "timeline_awareness": "realistic",
            "key_insights": ["Shows career motivation", "Goal-oriented thinking"],
            "potential_challenges": ["Goal refinement needed"],
            "success_factors": ["Motivation", "Planning skills"],
            "summary": "User demonstrates career motivation with opportunity to refine specific goals and planning."
        }