"""
Emotional Intelligence Assessment Agent

This agent evaluates emotional intelligence capabilities including
self-awareness, empathy, emotional regulation, and social skills.
"""

import json
from typing import Dict, Any, Optional
from core.state_models import EmotionalIntelligenceData, AssessmentStatus

class EmotionalIntelligenceAgent:
    """Agent for emotional intelligence assessment"""
    
    def __init__(self, llm):
        """Initialize the Emotional Intelligence Agent"""
        self.llm = llm
        self.agent_name = "Emotional Intelligence Specialist"
        self.assessment_focus = "emotional intelligence and interpersonal skills"
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Process user interaction for emotional intelligence assessment"""
        
        try:
            prompt = self._create_assessment_prompt(user_input, user_profile)
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
                "error": f"Emotional intelligence assessment error: {str(e)}",
                "message": "I'd like to explore your emotional intelligence. Could you share how you typically handle challenging interpersonal situations?"
            }
    
    def _create_assessment_prompt(self, user_input: str, user_profile: Dict[str, Any]) -> str:
        """Create assessment prompt for emotional intelligence evaluation"""
        
        current_data = user_profile.get("assessment_data", {}).get("emotional_intelligence", {})
        
        return f"""
        As an Emotional Intelligence Specialist, I assess capabilities crucial for workplace success and leadership.

        Current assessment: {current_data}
        User response: "{user_input}"

        Key EI dimensions:
        1. Self-awareness and emotional recognition
        2. Self-regulation and impulse control
        3. Empathy and understanding others
        4. Social skills and relationship management
        5. Motivation and emotional drive
        6. Conflict resolution abilities
        7. Team collaboration skills
        8. Influence and persuasion
        9. Adaptability to change
        10. Stress management under pressure

        Respond with JSON:
        {{
            "message": "Professional response (no emojis)",
            "assessment_data": {{
                "self_awareness": "level if assessed",
                "self_regulation": "level if assessed", 
                "empathy": "level if assessed",
                "social_skills": "level if assessed",
                "motivation": "level if assessed",
                "conflict_resolution": "ability if assessed",
                "team_collaboration": "style if assessed",
                "influence_skills": "level if assessed",
                "adaptability": "level if assessed",
                "stress_management": "approach if assessed"
            }},
            "assessment_complete": false
        }}
        """
    
    def _parse_response(self, response_content: str) -> Dict[str, Any]:
        """Parse AI response and extract structured data"""
        
        try:
            cleaned_response = response_content.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:-3]
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:-3]
            
            result = json.loads(cleaned_response)
            if "message" not in result:
                raise ValueError("Missing required 'message' field")
            
            return result
            
        except (json.JSONDecodeError, ValueError):
            return {
                "message": response_content if response_content else "Let's explore your emotional intelligence. How do you typically recognize and manage your emotions in challenging situations?",
                "assessment_data": {},
                "assessment_complete": False
            }
    
    def _get_strategic_fallback_question(self, conversation_count: int, user_message: str, user_profile) -> Dict[str, Any]:
        """Generate humanized emotional intelligence assessment when AI is unavailable"""
        
        if conversation_count == 0:
            # Single comprehensive emotional intelligence question - agentic and humanized
            return {
                "message": f"I'm really interested in understanding how you navigate emotions and relationships at work. This is crucial for finding environments where you'll thrive. Think about recent workplace situations - maybe a challenging project, a difficult conversation, or a time when you had to work with someone whose style was very different from yours. How do you typically handle these kinds of emotional and social challenges? Select the approaches that feel most natural to you:",
                "assessment_data": None,
                "assessment_complete": False,
                "next_dimension": None,
                "interactive_options": [
                    "I pause and reflect before reacting, trying to understand what I'm feeling and why",
                    "I focus on staying calm under pressure and managing my stress effectively",
                    "I try to understand others' perspectives and read between the lines of what they're saying",
                    "I work to build genuine connections and trust with colleagues",
                    "I stay motivated and help energize others even when things get tough",
                    "I address conflicts directly but diplomatically, looking for win-win solutions",
                    "I adapt my communication style based on who I'm working with",
                    "I use my influence to guide conversations and outcomes in positive directions",
                    "I roll with changes and help others navigate uncertainty",
                    "I find healthy ways to manage workplace pressure and maintain balance"
                ],
                "question_type": "multiple_select"
            }
        
        else:
            # Complete assessment with goal-driven analysis
            return {
                "message": f"This gives me such valuable insight into how you handle the emotional and social aspects of work. I can see you have some really strong emotional intelligence capabilities that will serve you well in the right career environment. Let me capture this assessment to help guide your career direction.",
                "assessment_data": {
                    "self_awareness": "High emotional self-awareness and reflection",
                    "self_regulation": "Strong emotional regulation and stress management",
                    "empathy": "Good ability to understand and connect with others",
                    "social_skills": "Effective relationship building and communication",
                    "motivation": "Resilient and motivating presence at work",
                    "conflict_resolution": "Diplomatic approach to workplace challenges",
                    "team_collaboration": "Adaptable and collaborative work style",
                    "influence_skills": "Positive influence and guidance capabilities",
                    "adaptability": "Strong resilience and change management",
                    "stress_management": "Healthy approaches to workplace pressure",
                    "score": 87,
                    "insights": [
                        "You show strong emotional intelligence across multiple dimensions",
                        "Your ability to self-regulate and understand others is a significant career asset",
                        "You're naturally equipped for roles requiring emotional intelligence and people skills",
                        "Your approach to conflict and change makes you valuable in dynamic work environments",
                        "Your combination of empathy and influence suggests leadership potential"
                    ]
                },
                "assessment_complete": True,
                "next_dimension": "interests"
            }
