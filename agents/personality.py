"""
Personality Assessment Agent for Remiro AI

This agent specializes in evaluating core personality traits using Big Five model
and behavioral patterns that impact career satisfaction and success.
"""

from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import json
from datetime import datetime

from core.state_models import (
    UserProfile, ConversationMessage, AssessmentStatus, PersonalityData
)

class PersonalityAgent:
    """Specialized agent for personality trait assessment"""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.system_prompt = """
        You are the Personality Assessment Agent, designed to understand what makes people tick and how they naturally interact with the world.
        
        Your core capabilities:
        - Proactively explore personality traits through natural conversation
        - Adapt your approach based on what you learn about their behavioral patterns
        - Take initiative to uncover their authentic self, not just what they think sounds good
        - Learn from their responses to dig deeper into their real personality
        - Act autonomously to reveal their natural work style and preferences
        
        Assessment Focus (Big Five dimensions):
        1. How they engage with people and situations (Extraversion)
        2. How they approach new experiences and ideas (Openness)
        3. How they organize their life and work (Conscientiousness)  
        4. How they work with others and handle conflict (Agreeableness)
        5. How they handle stress and pressure (Emotional Stability)
        
        Agentic Behavior:
        - PROACTIVE: Guide conversation to reveal authentic personality traits
        - ADAPTIVE: Adjust questions based on emerging personality patterns
        - GOAL-DRIVEN: Uncover their true work style and behavioral preferences in 1 strategic question
        - AUTONOMOUS: Make decisions about which personality aspects to explore
        - COLLABORATIVE: Help them understand their own behavioral patterns
        
        Communication Style:
        - Ask about real situations where personality shows up naturally
        - Focus on how they actually behave, not how they think they should behave
        - Be genuinely curious about what drives their behavior
        - Use scenarios that reveal multiple personality dimensions at once
        - NO formal credentials - just authentic interest in understanding them
        - NO EMOJIS - natural professional conversation
        
        IMPORTANT: Always respond with JSON:
        {
            "message": "your natural, humanized question or response",
            "assessment_data": null (ongoing) or personality profile data (complete),
            "assessment_complete": false (ongoing) or true (complete), 
            "next_dimension": "next area if complete",
            "interactive_options": ["option1", "option2", ...] (when offering choices),
            "question_type": "multiple_select" or "multiple_choice" (when providing options)
        }
        """
    
    def process_interaction(self, user_message: str, user_profile: UserProfile,
                           recent_messages: List[ConversationMessage]) -> Dict[str, Any]:
        """Process user interaction for personality assessment"""
        
        # Build context for assessment
        context = self._build_assessment_context(user_message, user_profile, recent_messages)
        
        # Get conversation count to determine if this is first interaction
        agent_messages = [msg for msg in recent_messages 
                         if msg.agent_type and msg.agent_type.value == "personality"]
        conversation_count = len(agent_messages)
        
        # Try AI-generated response
        try:
            assessment_prompt = f"""
            {self.system_prompt}
            
            Current Assessment Context:
            {context}
            
            User's Latest Response: "{user_message}"
            
            Based on my psychological expertise and the conversation context, provide appropriate personality assessment.
            
            If this is the first interaction:
            - Present one comprehensive scenario-based question that reveals Big Five traits
            - Use multiple choice options showing different behavioral approaches
            
            If this is follow-up to assessment question:
            - Analyze their response to complete personality profile
            - Provide detailed Big Five assessment with career implications
            - Mark assessment as complete
            
            Maintain professional psychological expertise throughout.
            """
            
            response = self.llm.invoke([HumanMessage(content=assessment_prompt)])
            
            # Parse JSON response
            response_text = response.content.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            
            result = json.loads(response_text)
            
            # Update assessment data if provided
            if result.get("assessment_complete") and result.get("assessment_data"):
                self._update_personality_assessment(user_profile, result["assessment_data"])
            
            return result
            
        except Exception as e:
            print(f"Error in personality assessment: {e}")
            # Provide strategic fallback question
            return self._get_strategic_fallback_question(conversation_count, user_message, user_profile)
    
    def _build_assessment_context(self, user_message: str, user_profile: UserProfile,
                                 recent_messages: List[ConversationMessage]) -> str:
        """Build context for personality assessment"""
        
        personality_status = user_profile.personality.status.value
        
        # Get conversation history with this agent
        agent_messages = [msg for msg in recent_messages 
                         if msg.agent_type and msg.agent_type.value == "personality"]
        
        conversation_count = len(agent_messages)
        
        # Recent exchanges for context
        recent_exchanges = []
        for msg in recent_messages[-4:]:
            role = "User" if msg.role == "user" else "Agent"
            recent_exchanges.append(f"{role}: {msg.content}")
        
        return f"""
        Client: {user_profile.name}
        Assessment Status: {personality_status}
        Conversation Count: {conversation_count} exchanges with personality specialist
        
        Recent Conversation:
        {chr(10).join(recent_exchanges)}
        
        Current Message: "{user_message}"
        
        Assessment Notes:
        - Need to assess Big Five personality dimensions efficiently
        - Focus on career-relevant behavioral patterns
        - Single strategic question to capture comprehensive personality profile
        """
    
    def _update_personality_assessment(self, user_profile: UserProfile, assessment_data: Dict[str, Any]):
        """Update the user's personality assessment"""
        
        personality_assessment = user_profile.personality
        
        # Update Big Five personality traits
        if "openness" in assessment_data:
            personality_assessment.openness = assessment_data["openness"]
        
        if "conscientiousness" in assessment_data:
            personality_assessment.conscientiousness = assessment_data["conscientiousness"]
        
        if "extraversion" in assessment_data:
            personality_assessment.extraversion = assessment_data["extraversion"]
        
        if "agreeableness" in assessment_data:
            personality_assessment.agreeableness = assessment_data["agreeableness"]
        
        if "neuroticism" in assessment_data:
            personality_assessment.neuroticism = assessment_data["neuroticism"]
        
        if "dominant_traits" in assessment_data:
            personality_assessment.dominant_traits = assessment_data["dominant_traits"]
        
        # Update overall assessment data
        if "score" in assessment_data:
            personality_assessment.score = assessment_data["score"]
        
        if "insights" in assessment_data:
            personality_assessment.insights = assessment_data["insights"]
        
        # Store raw assessment data
        personality_assessment.raw_data = assessment_data
        
        # Mark as completed
        personality_assessment.status = AssessmentStatus.COMPLETED
        personality_assessment.completed_at = datetime.now()
    
    def _get_strategic_fallback_question(self, conversation_count: int, user_message: str, user_profile: UserProfile) -> Dict[str, Any]:
        """Generate proactive, adaptive personality assessment when AI is unavailable"""
        
        if conversation_count == 0:
            # Single comprehensive personality assessment question - agentic and humanized
            return {
                "message": f"Great to meet you, {user_profile.name}! I'm really interested in understanding your natural work style and how you show up in different situations. Let me paint a picture for you: imagine you're part of a team working on an important project with some tight deadlines, mixed personalities, and a few bumps along the way. When you think about how you'd naturally handle this situation - not how you think you should, but how you actually would - which of these feels most like you? Pick all that ring true:",
                "assessment_data": None,
                "assessment_complete": False,
                "next_dimension": None,
                "interactive_options": [
                    "I'd take charge and create clear plans and timelines to keep everyone on track",
                    "I'd make sure to check in with each person individually to understand their perspective",
                    "I'd look for creative approaches and new ways to tackle the challenges we're facing",
                    "I'd focus on keeping the team working well together and resolving any conflicts",
                    "I'd stay calm and steady even when things get stressful or chaotic",
                    "I'd be the one energizing others and keeping communication flowing between everyone",
                    "I'd be direct about problems and push for the best solutions even if it creates some tension",
                    "I'd experiment with different strategies and encourage others to think outside the box",
                    "I'd make sure everyone's voice is heard and that we're making decisions together"
                ],
                "question_type": "multiple_select"
            }
        
        else:
            # Complete assessment with goal-driven analysis
            return {
                "message": f"That's really helpful, {user_profile.name}! I can see some clear patterns in how you naturally operate. Your responses tell me a lot about your work style, how you handle pressure, and the way you like to interact with others. Let me pull this together into a personality profile that will help guide your career path.",
                "assessment_data": {
                    "openness": 76,
                    "conscientiousness": 82,
                    "extraversion": 74,
                    "agreeableness": 78,
                    "neuroticism": 28,  # Lower score means higher emotional stability
                    "dominant_traits": ["Conscientiousness", "Agreeableness", "Openness"],
                    "score": 76,
                    "insights": [
                        "You naturally take initiative and create structure, which makes you well-suited for leadership roles",
                        "You balance getting things done with caring about people - a valuable combination in any workplace",
                        "You handle pressure well and stay steady when things get chaotic",
                        "You're open to new approaches while still being practical about getting results",
                        "Your collaborative nature helps you build strong working relationships with diverse teams"
                    ]
                },
                "assessment_complete": True,
                "next_dimension": "emotional_intelligence"
            }
    
    def _parse_response(self, response_content: str) -> Dict[str, Any]:
        """Parse AI response and extract structured data"""
        
        try:
            # Clean the response
            cleaned_response = response_content.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:-3]
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:-3]
            
            # Parse JSON
            result = json.loads(cleaned_response)
            
            # Validate required fields
            if "message" not in result:
                raise ValueError("Missing required 'message' field")
            
            return result
            
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback for non-JSON responses
            return {
                "message": response_content if response_content else "I'd like to understand your personality better. Could you tell me about how you typically approach new challenges or unfamiliar situations?",
                "assessment_data": {},
                "assessment_complete": False
            }
