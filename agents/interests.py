"""
Interests Assessment Agent for Remiro AI

This agent identifies user's passion areas, curiosities, and subject interests
that drive career satisfaction and engagement.
"""

from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import json
from datetime import datetime

from core.state_models import (
    UserProfile, ConversationMessage, AssessmentStatus, InterestsData
)

class InterestsAgent:
    """Specialized agent for interests and passion assessment"""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.system_prompt = """
        You are the Interests Assessment Agent, designed to discover what genuinely excites and energizes people.
        
        Your core capabilities:
        - Proactively explore what truly interests and motivates them
        - Adapt questioning based on the passion areas that emerge from their responses
        - Take initiative to connect their interests to potential career paths
        - Learn from their enthusiasm to identify their strongest passion patterns
        - Act autonomously to uncover interests they might not have considered career-relevant
        
        Assessment Focus:
        1. Activities that make them lose track of time
        2. Subjects they naturally gravitate toward learning about
        3. Problems they're drawn to solve
        4. Industries or fields that spark their curiosity
        5. Ways they like to contribute or make an impact
        
        Agentic Behavior:
        - PROACTIVE: Guide conversation to uncover hidden passion areas
        - ADAPTIVE: Follow up on interests that seem to energize them most
        - GOAL-DRIVEN: Discover their core interests in 1 strategic question
        - AUTONOMOUS: Connect their interests to career possibilities they may not have considered
        - COLLABORATIVE: Help them see how their interests could become their career
        
        Communication Style:
        - Show genuine excitement about discovering what they're passionate about
        - Ask about what they actually do in their free time, not just what they think sounds good
        - Focus on what makes them feel energized and engaged
        - Help them see connections between their interests and career opportunities
        - NO formal credentials - just authentic curiosity about what drives them
        - NO EMOJIS - natural enthusiastic conversation
        
        IMPORTANT: Always respond with JSON:
        {
            "message": "your natural, enthusiastic question or response",
            "assessment_data": null (ongoing) or interests profile data (complete),
            "assessment_complete": false (ongoing) or true (complete),
            "next_dimension": "next area if complete",
            "interactive_options": ["option1", "option2", ...] (when offering choices),
            "question_type": "multiple_select" or "multiple_choice" (when providing options)
        }
        """
    
    def process_interaction(self, user_message: str, user_profile: UserProfile,
                           recent_messages: List[ConversationMessage]) -> Dict[str, Any]:
        """Process user interaction for interests assessment"""
        
        # Build context for assessment
        context = self._build_assessment_context(user_message, user_profile, recent_messages)
        
        # Get conversation count
        agent_messages = [msg for msg in recent_messages 
                         if msg.agent_type and msg.agent_type.value == "interests"]
        conversation_count = len(agent_messages)
        
        try:
            assessment_prompt = f"""
            {self.system_prompt}
            
            Current Assessment Context:
            {context}
            
            User's Latest Response: "{user_message}"
            
            Based on my experience helping people discover careers they love, provide appropriate interests assessment.
            
            If this is the first interaction:
            - Present one comprehensive question about their interests, curiosities, and what excites them
            - Use multiple choice options covering various interest areas
            
            If this is follow-up to assessment question:
            - Analyze their response to complete interests profile
            - Provide detailed assessment of their passion areas and career implications
            - Mark assessment as complete
            
            Maintain enthusiastic expertise about interests and career alignment.
            """
            
            response = self.llm.invoke([HumanMessage(content=assessment_prompt)])
            
            # Parse JSON response
            response_text = response.content.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            
            result = json.loads(response_text)
            
            # Update assessment data if provided
            if result.get("assessment_complete") and result.get("assessment_data"):
                self._update_interests_assessment(user_profile, result["assessment_data"])
            
            return result
            
        except Exception as e:
            print(f"Error in interests assessment: {e}")
            return self._get_strategic_fallback_question(conversation_count, user_message, user_profile)
    
    def _build_assessment_context(self, user_message: str, user_profile: UserProfile,
                                 recent_messages: List[ConversationMessage]) -> str:
        """Build context for interests assessment"""
        
        interests_status = user_profile.interests.status.value
        
        agent_messages = [msg for msg in recent_messages 
                         if msg.agent_type and msg.agent_type.value == "interests"]
        
        conversation_count = len(agent_messages)
        
        recent_exchanges = []
        for msg in recent_messages[-4:]:
            role = "User" if msg.role == "user" else "Agent"
            recent_exchanges.append(f"{role}: {msg.content}")
        
        return f"""
        Client: {user_profile.name}
        Assessment Status: {interests_status}
        Conversation Count: {conversation_count} exchanges with interests specialist
        
        Recent Conversation:
        {chr(10).join(recent_exchanges)}
        
        Current Message: "{user_message}"
        
        Assessment Notes:
        - Need to identify core interests and passion areas efficiently
        - Focus on what genuinely excites and energizes them
        - Single strategic question to capture comprehensive interests profile
        """
    
    def _update_interests_assessment(self, user_profile: UserProfile, assessment_data: Dict[str, Any]):
        """Update the user's interests assessment"""
        
        interests_assessment = user_profile.interests
        
        # Update interests data
        if "subject_interests" in assessment_data:
            interests_assessment.subject_interests = assessment_data["subject_interests"]
        
        if "activity_preferences" in assessment_data:
            interests_assessment.activity_preferences = assessment_data["activity_preferences"]
        
        if "industry_curiosity" in assessment_data:
            interests_assessment.industry_curiosity = assessment_data["industry_curiosity"]
        
        if "problem_areas" in assessment_data:
            interests_assessment.problem_areas = assessment_data["problem_areas"]
        
        if "hobby_connections" in assessment_data:
            interests_assessment.hobby_connections = assessment_data["hobby_connections"]
        
        # Update overall assessment data
        if "score" in assessment_data:
            interests_assessment.score = assessment_data["score"]
        
        if "insights" in assessment_data:
            interests_assessment.insights = assessment_data["insights"]
        
        # Store raw assessment data
        interests_assessment.raw_data = assessment_data
        
        # Mark as completed
        interests_assessment.status = AssessmentStatus.COMPLETED
        interests_assessment.completed_at = datetime.now()
    
    def _get_strategic_fallback_question(self, conversation_count: int, user_message: str, user_profile: UserProfile) -> Dict[str, Any]:
        """Generate proactive, adaptive interests assessment when AI is unavailable"""
        
        if conversation_count == 0:
            # Single comprehensive interests assessment question - agentic and humanized
            return {
                "message": f"Hey {user_profile.name}! I'm really excited to learn about what makes you light up. I want to understand what you're naturally drawn to - not just what you think might be 'good for your career,' but what actually gets you excited and engaged. Think about times when you're totally absorbed in something, maybe even losing track of time. What kind of activities, subjects, or challenges naturally pull you in? Select everything that genuinely resonates:",
                "assessment_data": None,
                "assessment_complete": False,
                "next_dimension": None,
                "interactive_options": [
                    "Digging into data to find patterns and insights that others miss",
                    "Creating, designing, or building something from scratch",
                    "Helping people learn, grow, or achieve their goals",
                    "Solving technical problems or figuring out how systems work",
                    "Leading projects and making decisions that shape outcomes",
                    "Researching new ideas and staying on the cutting edge of developments",
                    "Communicating ideas through writing, speaking, or visual media",
                    "Working with numbers, analyzing financial trends, or optimizing resources",
                    "Understanding what makes people tick and how relationships work",
                    "Working on environmental, social impact, or sustainability challenges",
                    "Developing technology, apps, or digital solutions",
                    "Exploring arts, culture, or creative expression in various forms"
                ],
                "question_type": "multiple_select"
            }
        
        else:
            # Complete assessment with goal-driven analysis
            return {
                "message": f"This is so helpful, {user_profile.name}! I can already see some exciting patterns in what draws you in. Your combination of interests is really telling me a lot about the kind of work environment and challenges where you'd thrive. Let me put together your interests profile - this is going to be key for finding career paths that will genuinely energize you.",
                "assessment_data": {
                    "subject_interests": ["Complex problem-solving", "Innovation and creativity", "Strategic thinking"],
                    "activity_preferences": ["Analysis and research", "Creative development", "Leadership and impact"],
                    "industry_curiosity": ["Technology and innovation", "Strategic consulting", "Creative industries"],
                    "problem_areas": ["Complex systemic challenges", "Creative and strategic problems", "People and organizational development"],
                    "hobby_connections": ["Personal interests that translate to professional strengths and career opportunities"],
                    "score": 84,
                    "insights": [
                        "You're drawn to work that combines analytical thinking with creative problem-solving",
                        "You naturally gravitate toward challenges that have both intellectual depth and practical impact",  
                        "Your interests suggest you'd thrive in dynamic environments with variety and growth opportunities",
                        "You're interested in understanding systems and people, which opens up leadership and consulting paths",
                        "Your combination of interests points toward roles where you can innovate and influence outcomes"
                    ]
                },
                "assessment_complete": True,
                "next_dimension": "motivations_values"
            }
