"""
Enhanced Personality Agent - Advanced Career Assessment

This agent understands natural behavioral patterns and work style preferences
through empathetic conversation and personalized questions.
"""

from typing import Dict, Any, List, Optional
from agents.enhanced_base_agent import EnhancedBaseAgent
import json

class PersonalityAgent(EnhancedBaseAgent):
    """🧠 Personality Agent - Understands behavioral patterns and work style preferences"""
    
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            agent_name="Personality & Work Style Specialist",
            assessment_type="personality",
            core_domain="Natural behavioral patterns and work style preferences"
        )
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        """Return the 3 predefined questions for personality assessment"""
        return [
            {
                "id": "personality_q1",
                "question": "So here's something I'm wondering about you - do you thrive when you're bouncing ideas off teammates and working together, or are you more of a 'give me some quiet time to focus and I'll blow your mind' kind of person?",
                "context": "work_style",
                "purpose": "Identify collaboration vs independent work preferences"
            },
            {
                "id": "personality_q2",
                "question": "Picture your perfect work day - would it be in a place that's buzzing with energy and constant new challenges, or somewhere more chill and predictable where you know what to expect?",
                "context": "environment",
                "purpose": "Understand environmental preferences and change tolerance"
            },
            {
                "id": "personality_q3",
                "question": "When there's drama or disagreement at work (we've all been there!), what's your instinct - jump right in and talk it out, try to help everyone find middle ground, or step back and think it through before you say anything?",
                "context": "communication",
                "purpose": "Assess conflict resolution and communication style"
            }
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        """Analyze user responses to determine personality profile"""
        
        try:
            analysis_prompt = f"""
            As a Personality & Work Style Specialist, analyze these responses:
            
            1. Work preference (team vs solo): {responses[0] if len(responses) > 0 else 'Not provided'}
            2. Ideal work environment: {responses[1] if len(responses) > 1 else 'Not provided'}  
            3. Conflict resolution approach: {responses[2] if len(responses) > 2 else 'Not provided'}
            
            Provide JSON analysis:
            {{
                "profile_clarity": "clear" or "unclear",
                "work_style": "collaborative" or "independent" or "balanced",
                "environment_preference": "dynamic" or "structured" or "flexible", 
                "communication_style": "direct" or "diplomatic" or "analytical",
                "personality_traits": ["list of key traits identified"],
                "team_dynamics": "how they work in teams",
                "leadership_potential": "high" or "medium" or "low",
                "key_insights": ["personality insights"],
                "career_fit_indicators": ["suitable work environments/roles"],
                "summary": "personality profile summary"
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
            "work_style": "balanced",
            "environment_preference": "flexible",
            "communication_style": "diplomatic", 
            "personality_traits": ["Adaptable", "Professional"],
            "team_dynamics": "Works well in various team settings",
            "leadership_potential": "medium",
            "key_insights": ["Personality assessment complete", "Shows professional adaptability"],
            "career_fit_indicators": ["Various professional environments"],
            "summary": "User demonstrates professional adaptability and balanced work style preferences."
        }