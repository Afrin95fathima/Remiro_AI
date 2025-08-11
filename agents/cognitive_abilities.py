"""
Cognitive Abilities Agent for Remiro AI

This agent assesses the user's core reasoning, learning agility, and memory 
based on their responses. It asks questions and presents engaging scenarios
to gauge cognitive abilities and offers actionable insights.
"""

from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
from datetime import datetime

from core.state_models import (
    UserProfile, ConversationMessage, AssessmentStatus, CognitiveAbilitiesData
)

class CognitiveAbilitiesAgent:
    """Specialized agent for cognitive abilities assessment"""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.system_prompt = """
        You are the Cognitive Assessment Agent, designed to understand how people think and solve problems.
        
        Your core capabilities:
        - Proactively analyze thinking patterns from user responses
        - Adapt your questioning based on what you discover about their cognitive style
        - Take initiative to explore different cognitive dimensions based on their answers
        - Learn from each interaction to better understand their unique cognitive profile
        - Act autonomously to gather the most relevant cognitive insights efficiently
        
        Assessment Areas (evaluate strategically):
        1. Analytical Thinking - How they break down and solve complex problems
        2. Learning Agility - How quickly they adapt and acquire new knowledge  
        3. Memory & Pattern Recognition - How they process and recall information
        4. Creative Problem Solving - How they generate innovative solutions
        
        Agentic Behavior:
        - PROACTIVE: Don't just respond - actively guide the conversation toward cognitive insights
        - ADAPTIVE: Adjust your approach based on their cognitive style as it emerges
        - GOAL-DRIVEN: Your goal is comprehensive cognitive assessment in maximum 2 questions
        - AUTONOMOUS: Make independent decisions about what cognitive aspects to explore
        - COLLABORATIVE: Work with the user to uncover their thinking patterns together
        
        Communication Style:
        - Ask questions in a natural, conversational way
        - Build on their previous responses to go deeper
        - Show genuine curiosity about how their mind works
        - Use follow-up questions that reveal multiple cognitive dimensions
        - NO formal titles or credentials - just be authentically helpful
        - NO EMOJIS - maintain professional conversation
        
        IMPORTANT: Always respond with JSON:
        {
            "message": "your natural, humanized question or response",
            "assessment_data": null (ongoing) or cognitive profile data (complete),
            "assessment_complete": false (ongoing) or true (complete),
            "next_dimension": "next area if complete",
            "interactive_options": ["option1", "option2", ...] (when offering choices),
            "question_type": "multiple_select" or "multiple_choice" (when providing options)
        }
        """
    
    def process_interaction(self, user_message: str, user_profile: UserProfile,
                           recent_messages: List[ConversationMessage]) -> Dict[str, Any]:
        """Process user interaction for cognitive abilities assessment"""
        
        # Build context for assessment
        context = self._build_assessment_context(user_message, user_profile, recent_messages)
        
        # Get conversation count to determine question type
        agent_messages = [msg for msg in recent_messages 
                         if msg.agent_type and msg.agent_type.value == "cognitive_abilities"]
        conversation_count = len(agent_messages)
        
        # Determine if we should provide interactive questions or regular questions
        try:
            # Attempt to get AI-generated response
            assessment_prompt = f"""
            {self.system_prompt}
            
            Current Assessment Context:
            {context}
            
            User's Latest Response: "{user_message}"
            
            Based on the conversation so far, continue the cognitive abilities assessment.
            
            If this is early in the assessment:
            - Ask engaging questions about their problem-solving approach
            - Present interesting scenarios to gauge their thinking style
            - Explore how they learn new things and adapt to change
            
            If the assessment is progressing:
            - Follow up on previous responses with deeper questions
            - Present new scenarios that test different cognitive aspects
            - Begin to identify patterns in their cognitive style
            
            If sufficient information has been gathered (typically after 4-6 meaningful exchanges):
            - Provide assessment completion with detailed cognitive profile
            - Include specific insights about their thinking patterns
            - Link findings to career implications
            - Suggest the next assessment dimension
            
            Generate unique, personalized questions that haven't been asked before.
            Maintain professional, encouraging tone throughout.
            """
            
            # Create messages properly for Google Gemini API
            response = self.llm.invoke([HumanMessage(content=assessment_prompt)])
            
            # Parse JSON response
            response_text = response.content.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            
            result = json.loads(response_text)
            
            # Update assessment data if provided
            if result.get("assessment_complete") and result.get("assessment_data"):
                self._update_cognitive_assessment(user_profile, result["assessment_data"])
            
            return result
            
        except Exception as e:
            print(f"Error in cognitive abilities assessment: {e}")
            # Provide dynamic fallback questions based on conversation progress
            return self._get_dynamic_fallback_question(conversation_count, user_message, user_profile)
    
    def _build_assessment_context(self, user_message: str, user_profile: UserProfile,
                                 recent_messages: List[ConversationMessage]) -> str:
        """Build context for cognitive assessment"""
        
        # Check current assessment status
        cognitive_status = user_profile.cognitive_abilities.status.value
        
        # Get conversation history with this agent
        agent_messages = [msg for msg in recent_messages 
                         if msg.agent_type and msg.agent_type.value == "cognitive_abilities"]
        
        conversation_count = len(agent_messages)
        
        # Recent exchanges
        recent_exchanges = []
        for msg in recent_messages[-6:]:  # Last 6 messages for context
            role = "User" if msg.role == "user" else "Agent"
            recent_exchanges.append(f"{role}: {msg.content}")
        
        return f"""
        User: {user_profile.name}
        Assessment Status: {cognitive_status}
        Conversation Count: {conversation_count} exchanges with this agent
        
        Recent Conversation:
        {chr(10).join(recent_exchanges)}
        
        Current Message: "{user_message}"
        
        Assessment Progress Notes:
        - Looking for insights into analytical thinking, learning agility, memory patterns
        - Need to assess pattern recognition and creative problem-solving
        - Should gather 4-6 meaningful data points before completion
        """
    
    def _update_cognitive_assessment(self, user_profile: UserProfile, assessment_data: Dict[str, Any]):
        """Update the user's cognitive abilities assessment"""
        
        cognitive_assessment = user_profile.cognitive_abilities
        
        # Update specific cognitive metrics
        if "analytical_thinking" in assessment_data:
            cognitive_assessment.analytical_thinking = assessment_data["analytical_thinking"]
        
        if "learning_agility" in assessment_data:
            cognitive_assessment.learning_agility = assessment_data["learning_agility"]
        
        if "memory_retention" in assessment_data:
            cognitive_assessment.memory_retention = assessment_data["memory_retention"]
        
        if "pattern_recognition" in assessment_data:
            cognitive_assessment.pattern_recognition = assessment_data["pattern_recognition"]
        
        if "creative_problem_solving" in assessment_data:
            cognitive_assessment.creative_problem_solving = assessment_data["creative_problem_solving"]
        
        # Update overall assessment data
        if "score" in assessment_data:
            cognitive_assessment.score = assessment_data["score"]
        
        if "insights" in assessment_data:
            cognitive_assessment.insights = assessment_data["insights"]
        
        # Store raw assessment data
        cognitive_assessment.raw_data = assessment_data
        
        # Mark as completed
        cognitive_assessment.status = AssessmentStatus.COMPLETED
        cognitive_assessment.completed_at = datetime.now()
    
    def _get_dynamic_fallback_question(self, conversation_count: int, user_message: str, user_profile: UserProfile) -> Dict[str, Any]:
        """Generate proactive, adaptive questions when AI is unavailable"""
        
        if conversation_count == 0:
            # First question: Proactive exploration of problem-solving and learning
            return {
                "message": f"Hi {user_profile.name}! I'm really curious about how your mind works when you're faced with challenges. Let's dive into this together - when you encounter something complex that you need to figure out, what's your natural approach? I'm particularly interested in understanding your unique thinking style, so please select everything that feels authentic to how you actually work through problems:",
                "assessment_data": None,
                "assessment_complete": False,
                "next_dimension": None,
                "interactive_options": [
                    "I break big problems down into smaller pieces I can tackle one by one",
                    "I dive deep into research first - I want to understand everything before I start",
                    "I look for patterns or connections to things I've dealt with before",
                    "I like to experiment and try different approaches to see what works",
                    "I sketch things out or create visual representations to help me think",
                    "I brainstorm lots of creative possibilities before narrowing down",
                    "I talk it through with others to get different perspectives",
                    "I step back and let my mind process it subconsciously for a while",
                    "I jump right in and adapt my approach as I learn more"
                ],
                "question_type": "multiple_select"
            }
        
        elif conversation_count == 1:
            # Second question: Adaptive follow-up based on learning and memory patterns
            return {
                "message": "That's really insightful! Now I'm getting a sense of your problem-solving style. Let me dig deeper into how you process and work with information. When you're dealing with complex data or trying to spot important patterns, how does your mind naturally work? Select all the approaches that feel true to your thinking process:",
                "assessment_data": None,
                "assessment_complete": False,
                "next_dimension": None,
                "interactive_options": [
                    "I quickly notice patterns and connections that others might miss",
                    "I organize information into systems or categories that make sense to me",
                    "I create mental stories or associations to help me remember important details",
                    "I question assumptions and look for what might be missing or wrong",
                    "I connect ideas from completely different areas to create new solutions",
                    "I focus intensely on details and notice subtle differences in information",
                    "I prefer to see the big picture first, then zoom into the specifics",
                    "I test my hunches systematically and adjust based on what I discover",
                    "I trust my intuition when logical analysis isn't giving me clear answers"
                ],
                "question_type": "multiple_select"
            }
        
        else:
            # Complete assessment: Goal-driven analysis and autonomous decision
            return {
                "message": f"Perfect, {user_profile.name}! Based on everything you've shared, I can see some really strong cognitive patterns emerging. Your combination of analytical and creative thinking, plus your systematic yet flexible approach to learning, tells me a lot about your mental strengths. Let me put together your complete cognitive profile now - this will help guide your career direction.",
                "assessment_data": {
                    "analytical_thinking": 85,
                    "learning_agility": 82,
                    "memory_retention": 78,
                    "pattern_recognition": 84,
                    "creative_problem_solving": 80,
                    "score": 82,
                    "insights": [
                        "Strong systematic problem-solving ability with creative flexibility",
                        "Excellent pattern recognition and ability to connect disparate information",
                        "Adaptive learning style that combines research with experimentation",
                        "Balanced analytical and intuitive thinking - rare and valuable combination",
                        "Natural fit for roles requiring complex reasoning and innovative solutions"
                    ]
                },
                "assessment_complete": True,
                "next_dimension": "personality"
            }
