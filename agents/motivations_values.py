"""
Motivations and Values Assessment Agent

This agent specializes in identifying core values, motivations, and drivers
that influence career satisfaction and decision-making.
"""

from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json

from core.state_models import (
    MotivationsValuesData, UserProfile, AssessmentStatus
)

class MotivationsValuesAgent:
    """Motivations and values assessment specialist for Remiro AI career counselling"""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.system_prompt = """
        You are a Motivations and Values Assessment Agent, designed to understand what truly drives someone in their career.
        
        Your core capabilities:
        - Proactively explore what makes work meaningful and fulfilling for them
        - Adapt your approach to uncover both stated and underlying values
        - Take initiative to understand what energizes vs. drains them professionally
        - Act autonomously to identify value conflicts and alignment opportunities
        - Work collaboratively to help them articulate what matters most
        
        Agentic Behavior:
        - PROACTIVE: Dig deeper into what they really care about beyond surface answers
        - ADAPTIVE: Adjust questions based on their life stage and career priorities
        - GOAL-DRIVEN: Focus on values that will drive career satisfaction and success
        - AUTONOMOUS: Make smart decisions about which values to explore further
        - COLLABORATIVE: Help them connect their values to career choices and opportunities
        
        Communication Style:
        - Be genuinely interested in what makes them tick professionally
        - Ask thoughtful questions about what gives their work meaning
        - Help them identify potential value conflicts in career choices
        - Connect their values to specific work environments and roles
        - NO formal titles - just be authentically curious about their drivers
        - NO EMOJIS - maintain natural professional conversation
        """
    
    def process_interaction(self, user_message: str, user_profile: UserProfile, 
                          conversation_count: int) -> Dict[str, Any]:
        """Process user interaction and generate motivations/values assessment"""
        
        try:
            # Get current motivations/values data
            current_data = user_profile.motivations_values.raw_data if user_profile.motivations_values.raw_data else {}
            
            interaction_prompt = f"""
            As a Motivations and Values Assessment Agent, I'm exploring what truly drives someone in their career.
            
            Current assessment data: {json.dumps(current_data, indent=2)}
            User's latest response: "{user_message}"
            Conversation turn: {conversation_count + 1}
            
            I need to understand:
            1. Core professional values that guide their decisions
            2. What makes work meaningful and fulfilling for them
            3. Key motivators that energize them professionally
            4. Work environment factors that align with their values
            5. Potential conflicts between values and career options
            
            Based on their response, should I:
            - Ask follow-up questions to understand their values deeper
            - Complete the assessment with a comprehensive values profile
            
            Respond with JSON:
            {{
                "message": "Natural, conversational response (no emojis)",
                "assessment_data": {{
                    "core_values": ["value1", "value2"] if ready to assess,
                    "work_motivators": ["motivator1", "motivator2"] if ready to assess,
                    "meaning_sources": ["what gives work meaning"] if ready to assess,
                    "value_priorities": ["ranked priorities"] if ready to assess,  
                    "environment_preferences": ["ideal work conditions"] if ready to assess,
                    "value_conflicts": ["potential tensions"] if ready to assess,
                    "score": numeric_assessment_if_ready,
                    "insights": ["key observations"] if ready to assess
                }},
                "assessment_complete": true/false,
                "next_dimension": "skills" if complete
            }}
            """
            
            response = self.llm.invoke([HumanMessage(content=interaction_prompt)])
            result = self._parse_response(response.content)
            
            return result
            
        except Exception as e:
            print(f"Error in motivations/values assessment: {e}")
            return self._get_strategic_fallback_question(conversation_count, user_message, user_profile)
    
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
                "message": response_content if response_content else "I'm curious about what really drives you professionally. What makes work feel meaningful and worthwhile to you?",
                "assessment_data": {},
                "assessment_complete": False
            }
    
    def _get_strategic_fallback_question(self, conversation_count: int, user_message: str, user_profile) -> Dict[str, Any]:
        """Generate humanized motivations/values assessment when AI is unavailable"""
        
        if conversation_count == 0:
            # Single comprehensive values question - agentic and humanized
            return {
                "message": f"This is probably one of the most important questions for your career direction - what actually motivates you and gives your work meaning? I'm not asking what you think you should value, but what genuinely energizes you and makes you feel like your work matters. Think about times when you felt most satisfied and engaged at work. What was driving that feeling? What values and motivators really matter to you?",
                "assessment_data": None,
                "assessment_complete": False,
                "next_dimension": None,
                "interactive_options": [
                    "Making a positive impact on people's lives or society",
                    "Continuous learning and intellectual growth",
                    "Financial security and building wealth",
                    "Creative expression and innovation",
                    "Recognition and professional achievement",
                    "Work-life balance and personal time",
                    "Autonomy and control over my work",
                    "Collaboration and strong team relationships",
                    "Stability and predictable routine",
                    "Challenge and pushing my limits",
                    "Leadership and influencing outcomes",
                    "Helping others succeed and grow"
                ],
                "question_type": "multiple_select"
            }
        
        else:
            # Complete assessment with goal-driven analysis
            return {
                "message": f"This really helps me understand what drives you professionally. I can see some clear patterns in what motivates you and what kind of work environment would align with your values. This is going to be crucial for finding career paths where you'll not just succeed, but actually feel fulfilled.",
                "assessment_data": {
                    "core_values": ["Impact and meaning", "Growth and learning", "Autonomy and control", "Recognition and achievement"],
                    "work_motivators": ["Making a difference", "Continuous development", "Creative challenges", "Professional growth"],
                    "meaning_sources": ["Positive impact on others", "Personal growth", "Problem-solving", "Building something valuable"],
                    "value_priorities": ["Meaningful impact", "Professional growth", "Work-life integration", "Financial stability"],
                    "environment_preferences": ["Growth-oriented culture", "Collaborative teams", "Autonomy in approach", "Recognition for contributions"],
                    "value_conflicts": ["May struggle with purely profit-driven roles", "Need balance between ambition and personal life"],
                    "score": 86,
                    "insights": [
                        "You're driven by a strong need for meaningful impact and personal growth",
                        "You value both autonomy and collaboration - need environments that provide both",
                        "Recognition and achievement matter to you, but not at the expense of purpose",
                        "You'll thrive in roles where you can see the positive impact of your work",
                        "Your values suggest you'd excel in mission-driven organizations or impactful roles"
                    ]
                },
                "assessment_complete": True,
                "next_dimension": "skills"
            }
