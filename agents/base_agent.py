"""
Simple Enhanced Agent Template for Remiro AI
All agents inherit from this base pattern for consistency
"""

import json
from typing import Dict, Any, List
import random

class BaseAgent:
    """Base class for all Remiro AI career counseling agents"""
    
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Career Counselor"
        self.interaction_count = 0
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Main interaction processing - override in subclasses"""
        try:
            user_name = user_profile.get('name', 'there')
            
            if not user_input.strip() or self.interaction_count == 0:
                return await self._start_assessment(user_name, user_profile)
            else:
                return await self._process_response(user_input, user_name, user_profile)
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Hi {user_profile.get('name', 'there')}! I'm here to help you on your career journey. Let's explore this together."
            }
    
    async def _start_assessment(self, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Start the assessment - override in subclasses"""
        self.interaction_count += 1
        return {
            "success": True,
            "message": f"Hello {user_name}! Let's begin exploring this aspect of your career journey.",
            "assessment_data": None,
            "assessment_complete": False
        }
    
    async def _process_response(self, user_input: str, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Process user response - override in subclasses"""
        self.interaction_count += 1
        
        if self.interaction_count >= 3:
            return await self._complete_assessment(user_input, user_name, user_profile)
        else:
            return await self._ask_follow_up(user_input, user_name, user_profile)
    
    async def _ask_follow_up(self, user_input: str, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Ask follow-up question - override in subclasses"""
        return {
            "success": True,
            "message": f"Thank you for sharing that, {user_name}. Could you tell me more about that?",
            "assessment_data": None,
            "assessment_complete": False
        }
    
    async def _complete_assessment(self, user_input: str, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Complete the assessment - override in subclasses"""
        return {
            "success": True,
            "message": f"Thank you {user_name}! I've learned a lot about you through our conversation.",
            "assessment_data": {"summary": "Assessment completed"},
            "assessment_complete": True
        }
