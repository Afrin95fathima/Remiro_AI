"""
Enhanced Personality Assessment Agent - Personalized Career Counselor

This agent specializes in understanding personality traits, behavioral patterns,
and natural work preferences through empathetic, personalized conversations.
"""

import json
from typing import Dict, Any, List
import random

class PersonalityAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Personality & Work Style Counselor"
        self.interaction_count = 0
        
        # Personalized conversation starters based on background
        self.personality_explorations = {
            "Student": [
                "Think about group projects or study sessions - do you naturally take charge and organize everyone, or do you prefer to contribute your ideas and let others lead? What feels most comfortable for you?",
                "When you're facing a challenging assignment or exam, what's your natural approach? Do you dive in immediately, plan everything out first, or maybe seek support from others?",
                "In social situations at school - whether it's clubs, events, or just hanging out - what energizes you most? Large group activities or deeper one-on-one conversations?"
            ],
            "Recent Graduate": [
                "As you've transitioned from student life to the professional world, what aspects of teamwork and collaboration feel most natural to you? Do you thrive in leadership roles or prefer being a valued contributor?",
                "When you're learning something new for work or personal growth, what approach works best for you? Do you prefer structured training, hands-on experience, or self-directed learning?",
                "In your early career interactions, what kind of work environment makes you feel most confident and productive? Fast-paced and dynamic, or more structured and predictable?"
            ],
            "Professional": [
                "In your current role, when do you feel most energized and 'in your element'? Is it when you're leading projects, collaborating with others, or working independently on complex challenges?",
                "Think about the most satisfying workday you've had recently - what made it great? Was it the people interactions, problem-solving, creative work, or achieving specific results?",
                "When you're under pressure at work, what's your natural response style? Do you thrive on the energy, prefer to step back and plan, or work best when you can collaborate with others?"
            ],
            "Career Changer": [
                "As you consider this career change, what aspects of your personality do you feel weren't fully utilized in your previous role? What parts of yourself are you hoping to express more in your new direction?",
                "Looking at your work style preferences, what kind of environment and culture would allow your personality to truly shine? What would feel like the right 'fit' for who you are?",
                "When you think about your natural strengths and how you prefer to work, what type of role or responsibilities would make you excited to start each workday?"
            ],
            "Returning to Work": [
                "As you prepare to return to the professional world, how would you describe your natural work style and personality? What aspects of yourself do you want to make sure are recognized and valued?",
                "Think about past work experiences where you felt most fulfilled - what was it about those situations that brought out your best qualities and made you feel authentic?",
                "What kind of work environment and team dynamics would help you feel confident and supported as you transition back into your career?"
            ]
        }
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_name = user_profile.get('name', 'there')
            background = user_profile.get('background', 'Professional')
            
            if not user_input.strip() or self.interaction_count == 0:
                return await self._start_personality_assessment(user_name, background)
            else:
                return await self._process_personality_response(user_input, user_name, background, user_profile)
                
        except Exception as e:
            user_name = user_profile.get('name', 'there')
            return {
                "success": False, 
                "message": f"Hi {user_name}! I'm here to help you understand your natural work style and personality. Let's start by exploring how you naturally approach work and collaboration. What energizes you most in a work environment?"
            }
    
    async def _start_personality_assessment(self, user_name: str, background: str) -> Dict[str, Any]:
        """Start with personalized personality exploration"""
        self.interaction_count += 1
        
        # Select appropriate question set
        questions = self.personality_explorations.get(background, self.personality_explorations["Professional"])
        selected_question = random.choice(questions)
        
        welcome_message = f"Hello {user_name}! I'm your Personality & Work Style Counselor, and I'm excited to help you understand your natural preferences and how they translate to career success.\n\nAs a {background.lower()}, you have unique experiences that have shaped your work style. {selected_question}"
        
        return {
            "success": True,
            "message": welcome_message,
            "assessment_data": None,
            "assessment_complete": False
        }
    
    async def _process_personality_response(self, user_input: str, user_name: str, background: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Process user response and provide personality assessment"""
        self.interaction_count += 1
        
        # Determine if this should be a follow-up or completion
        should_complete = self.interaction_count >= 3
        
        if should_complete:
            return await self._complete_personality_assessment(user_input, user_name, background, user_profile)
        else:
            return await self._ask_personality_follow_up(user_input, user_name, background)
    
    async def _ask_personality_follow_up(self, user_input: str, user_name: str, background: str) -> Dict[str, Any]:
        """Ask personalized follow-up questions"""
        prompt = f"""As a Personality & Work Style Counselor, respond warmly to this response about work preferences:

        User ({user_name}, {background}): "{user_input}"
        
        Your response should:
        1. Acknowledge what you're learning about their personality with genuine interest
        2. Validate their preferences - show there are no "wrong" personality types
        3. Ask ONE follow-up question that explores a different personality dimension
        4. Use their name and connect insights to potential career strengths
        5. Make them feel understood and valued for who they are naturally
        
        Focus on exploring different aspects like:
        - How they handle change and new experiences
        - Their decision-making style
        - How they recharge and manage stress
        - Their communication and collaboration preferences
        
        Respond with JSON: {{"message": "your warm, validating response with insightful follow-up", "assessment_data": null, "assessment_complete": false}}"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            result = json.loads(response.content.strip().replace("```json", "").replace("```", ""))
            return {
                "success": True,
                "message": result["message"],
                "assessment_data": result.get("assessment_data"),
                "assessment_complete": result.get("assessment_complete", False)
            }
        except:
            return {
                "success": True,
                "message": f"That's really insightful, {user_name}! I'm getting a sense of your natural work style. To understand you better, how do you typically handle unexpected changes or new challenges at work? Do you get excited by the novelty, or do you prefer to have time to plan and prepare?",
                "assessment_data": None,
                "assessment_complete": False
            }
    
    async def _complete_personality_assessment(self, user_input: str, user_name: str, background: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Complete the personality assessment with comprehensive insights"""
        prompt = f"""As an expert Personality & Work Style Counselor, complete the assessment for {user_name}, a {background}.

        Their responses reveal important personality patterns. Based on all their responses, provide a comprehensive personality assessment:

        Final response: "{user_input}"
        Background: {background}
        
        Respond with JSON:
        {{
            "message": "warm, affirming message that celebrates their unique personality and connects it to career strengths",
            "assessment_data": {{
                "personality_profile": {{
                    "extroversion_level": "high/moderate/low with explanation",
                    "openness_to_experience": "description of their curiosity and adaptability",
                    "conscientiousness": "their organization and goal-orientation style",
                    "agreeableness": "their collaboration and interpersonal approach",
                    "emotional_stability": "how they handle stress and pressure"
                }},
                "work_style_preferences": {{
                    "ideal_work_environment": "detailed description",
                    "collaboration_style": "how they work best with others",
                    "leadership_approach": "natural leadership tendencies",
                    "decision_making_style": "how they make decisions",
                    "communication_preferences": "how they share ideas best"
                }},
                "career_strengths": ["personality-based strengths for their career"],
                "ideal_role_characteristics": ["what kind of roles would suit them"],
                "work_culture_fit": "description of cultures where they'd thrive",
                "stress_management_style": "how they naturally handle workplace pressure",
                "motivation_patterns": "what energizes and drives them at work",
                "growth_areas": "areas where awareness could enhance their effectiveness"
            }},
            "assessment_complete": true
        }}"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            result = json.loads(response.content.strip().replace("```json", "").replace("```", ""))
            
            # Add personalized completion message
            completion_message = f"\n\n🎯 **Assessment Complete!** {user_name}, your personality profile reveals some wonderful insights about your natural work style. Understanding these patterns will help you find roles and environments where you can be authentically successful. Every personality type brings unique value to the workplace - yours included!"
            
            result["message"] += completion_message
            
            return {
                "success": True,
                "message": result["message"],
                "assessment_data": result.get("assessment_data"),
                "assessment_complete": True
            }
        except:
            return {
                "success": True,
                "message": f"Thank you for sharing so openly, {user_name}! Your responses reveal someone who is thoughtful about their work style and values authentic relationships and meaningful work. These are tremendous strengths that will serve you well in your career journey.",
                "assessment_data": {
                    "personality_profile": {
                        "extroversion_level": "Balanced approach to social energy and collaboration",
                        "openness_to_experience": "Curious and thoughtful about new opportunities",
                        "conscientiousness": "Goal-oriented with attention to quality",
                        "agreeableness": "Values harmony and positive relationships",
                        "emotional_stability": "Steady and resilient in facing challenges"
                    },
                    "work_style_preferences": {
                        "ideal_work_environment": "Collaborative yet focused, with opportunities for both teamwork and independent work",
                        "collaboration_style": "Supportive team member who contributes thoughtfully",
                        "communication_preferences": "Clear, respectful, and purposeful communication"
                    },
                    "career_strengths": ["Reliability", "Thoughtfulness", "Adaptability", "Strong work ethic"]
                },
                "assessment_complete": True
            }
