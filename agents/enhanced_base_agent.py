"""
Enhanced Base Agent for Remiro AI Career Assessment System

This is the foundation class for all 12D career assessment agents, providing:
- Empathetic conversational capabilities
- Personalized question generation
- Emotional tone matching
- Assessment completion tracking
"""

import json
from typing import Dict, Any, List, Optional, Union
from abc import ABC, abstractmethod
import re
from datetime import datetime

class EnhancedBaseAgent(ABC):
    """Base class for all enhanced career assessment agents"""
    
    def __init__(self, llm, agent_name: str, assessment_type: str, core_domain: str):
        self.llm = llm
        self.agent_name = agent_name
        self.assessment_type = assessment_type
        self.core_domain = core_domain
        self.user_responses = []
        self.assessment_complete = False
        self.interaction_count = 0
        self.emotional_state = "neutral"
        
    @abstractmethod
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        """Return the 3 predefined questions for this agent"""
        pass
    
    @abstractmethod
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        """Analyze user responses to determine their profile clarity"""
        pass
    
    def detect_emotional_tone(self, user_input: str) -> str:
        """Detect the emotional tone of user input"""
        user_lower = user_input.lower()
        
        # Sad/negative indicators
        sad_keywords = ["sad", "disappointed", "frustrated", "worried", "anxious", "depressed", 
                       "upset", "stressed", "overwhelmed", "confused", "lost", "stuck", "difficult", "hard"]
        
        # Happy/positive indicators  
        happy_keywords = ["excited", "happy", "thrilled", "motivated", "passionate", "love", "enjoy",
                         "great", "amazing", "wonderful", "fantastic", "awesome", "perfect", "brilliant"]
        
        # Neutral/professional indicators
        neutral_keywords = ["think", "believe", "consider", "understand", "analyze", "evaluate"]
        
        sad_count = sum(1 for word in sad_keywords if word in user_lower)
        happy_count = sum(1 for word in happy_keywords if word in user_lower)
        
        if happy_count > sad_count and happy_count > 0:
            return "positive"
        elif sad_count > happy_count and sad_count > 0:
            return "negative" 
        else:
            return "neutral"
    
    def generate_empathetic_response(self, emotional_tone: str, base_response: str) -> str:
        """Add empathetic framing based on detected emotional tone"""
        
        if emotional_tone == "positive":
            empathy_starters = [
                "I can feel your enthusiasm! That's wonderful to hear. ",
                "Your positive energy really comes through! ",
                "It's great to sense your excitement about this. ",
                "I love hearing that passion in your response! "
            ]
        elif emotional_tone == "negative":
            empathy_starters = [
                "I understand this might feel challenging right now. ",
                "I hear that this is a difficult topic for you. ",
                "It's completely normal to feel uncertain about these things. ",
                "I appreciate you sharing these concerns with me. "
            ]
        else:
            empathy_starters = [
                "Thank you for that thoughtful response. ",
                "I appreciate you taking the time to reflect on this. ",
                "That's a very insightful perspective. "
            ]
        
        import random
        starter = random.choice(empathy_starters)
        return starter + base_response
    
    def generate_personalized_followup(self, user_response: str, question_context: str) -> Optional[str]:
        """Generate a personalized follow-up question based on user's response"""
        
        try:
            # Create a prompt for generating personalized follow-up
            prompt = f"""
            As a {self.agent_name}, analyze this user response and generate ONE personalized follow-up question if needed.
            
            Context: {question_context}
            User's Response: {user_response}
            
            Guidelines:
            - Only ask a follow-up if the response needs clarification or could be explored deeper
            - Make it conversational and empathetic 
            - Keep it brief and specific
            - If the response is complete and clear, return "NONE"
            
            Follow-up question (or NONE):
            """
            
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            followup = response.content.strip()
            
            if followup and followup != "NONE" and "?" in followup:
                return followup
            return None
            
        except Exception as e:
            print(f"Error generating follow-up: {e}")
            return None
    
    def process_response(self, user_input: str, current_question_index: int) -> Dict[str, Any]:
        """Process user response with emotional intelligence"""
        
        # Detect emotional tone
        emotional_tone = self.detect_emotional_tone(user_input)
        self.emotional_state = emotional_tone
        
        # Store response
        self.user_responses.append({
            "question_index": current_question_index,
            "response": user_input,
            "emotional_tone": emotional_tone,
            "timestamp": datetime.now().isoformat()
        })
        
        self.interaction_count += 1
        
        # Check if we have enough responses
        predefined_questions = self.get_predefined_questions()
        
        if len(self.user_responses) >= len(predefined_questions):
            # Assessment complete - generate analysis
            self.assessment_complete = True
            analysis = self.get_spectrum_analysis([r["response"] for r in self.user_responses])
            
            return {
                "type": "assessment_complete",
                "analysis": analysis,
                "emotional_tone": emotional_tone,
                "agent_name": self.agent_name
            }
        
        else:
            # Continue assessment - ask next question or follow-up
            next_question_index = len(self.user_responses)
            
            # Generate follow-up if needed
            if current_question_index < len(predefined_questions):
                current_q = predefined_questions[current_question_index]
                followup = self.generate_personalized_followup(user_input, current_q["question"])
                
                if followup:
                    response_text = self.generate_empathetic_response(
                        emotional_tone, 
                        followup
                    )
                    
                    return {
                        "type": "followup_question",
                        "question": response_text,
                        "question_index": current_question_index,
                        "emotional_tone": emotional_tone
                    }
            
            # Ask next predefined question
            if next_question_index < len(predefined_questions):
                next_q = predefined_questions[next_question_index]
                response_text = self.generate_empathetic_response(
                    emotional_tone,
                    f"Great insight! {next_q['question']}"
                )
                
                return {
                    "type": "next_question", 
                    "question": response_text,
                    "question_index": next_question_index,
                    "emotional_tone": emotional_tone
                }
        
        # Fallback
        return {
            "type": "assessment_complete",
            "analysis": self.get_spectrum_analysis([r["response"] for r in self.user_responses]),
            "emotional_tone": emotional_tone,
            "agent_name": self.agent_name
        }
    
    def get_assessment_summary(self) -> Dict[str, Any]:
        """Get complete assessment summary"""
        return {
            "agent_name": self.agent_name,
            "assessment_type": self.assessment_type,
            "core_domain": self.core_domain,
            "total_interactions": self.interaction_count,
            "assessment_complete": self.assessment_complete,
            "responses": self.user_responses,
            "analysis": self.get_spectrum_analysis([r["response"] for r in self.user_responses]) if self.assessment_complete else None
        }