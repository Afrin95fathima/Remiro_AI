"""Enhanced Aspirations Assessment Agent - Personalized Career Counselor"""
import json
from typing import Dict, Any, List
import random

class AspirationsAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Career Aspirations Counselor"
        self.interaction_count = 0
        
        # Personalized question sets based on background
        self.question_sets = {
            "Student": [
                "As you look toward graduation and your future career, what kind of impact do you dream of making in the world? What legacy would you want to leave through your professional work?",
                "When you imagine your ideal workday 5 years from now, what are you doing? What kind of environment are you in, and what gives you the most satisfaction about your work?",
                "What career achievements would make your family and friends proudly say 'I knew you could do it'? What would those milestone moments look like for you?"
            ],
            "Recent Graduate": [
                "Now that you've finished your studies, what excites you most about starting your professional journey? What kind of career growth story do you want to write?",
                "As you transition from academic life to your career, what professional goals energize you the most? What would success look like in your first few years?",
                "What aspects of your field of study do you hope to develop into expertise? How do you see yourself evolving professionally?"
            ],
            "Professional": [
                "Looking at your current career trajectory, what professional heights do you aspire to reach? What would represent the pinnacle of success for you?",
                "If you could redesign your career path from today forward, what direction would truly fulfill you? What changes would you make?",
                "What professional legacy do you want to build? How do you want to be remembered in your field or industry?"
            ],
            "Career Changer": [
                "What is it about your desired new career path that truly excites and motivates you? What drew you to consider this significant change?",
                "As you envision your new career direction, what achievements in this field would make you feel most proud and fulfilled?",
                "What professional transformation do you hope to achieve through this career change? How do you see yourself thriving in this new path?"
            ],
            "Returning to Work": [
                "As you prepare to re-enter the professional world, what career aspirations feel most meaningful to you now? What do you hope to accomplish?",
                "How has your time away from work shaped your perspective on what you want from your career? What matters most to you professionally now?",
                "What kind of professional comeback story would you be excited to tell? What achievements would make this return most fulfilling?"
            ]
        }
        
        self.follow_up_questions = [
            "What steps have you already taken or considered taking toward these goals?",
            "What would achieving these aspirations mean for your personal fulfillment and happiness?",
            "How do these career goals align with your life values and priorities?",
            "What obstacles do you anticipate, and how committed are you to overcoming them?",
            "Who in your field or industry do you admire, and what about their path inspires you?"
        ]
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_name = user_profile.get('name', 'there')
            background = user_profile.get('background', 'Professional')
            
            if not user_input.strip() or self.interaction_count == 0:
                return await self._start_personalized_assessment(user_name, background)
            else:
                return await self._process_aspirations_response(user_input, user_name, background, user_profile)
                
        except Exception as e:
            user_name = user_profile.get('name', 'there')
            return {
                "success": False, 
                "message": f"Hi {user_name}! I'm excited to explore your career aspirations and dreams with you. What kind of future do you envision for yourself professionally? What gets you excited when you think about your career possibilities?"
            }
    
    async def _start_personalized_assessment(self, user_name: str, background: str) -> Dict[str, Any]:
        """Start with personalized questions based on user background"""
        self.interaction_count += 1
        
        # Select appropriate question set
        questions = self.question_sets.get(background, self.question_sets["Professional"])
        selected_question = random.choice(questions)
        
        welcome_message = f"Hello {user_name}! I'm your Career Aspirations Counselor, and I'm genuinely excited to explore your professional dreams and goals with you. As a {background.lower()}, you're at a unique point in your career journey.\n\n{selected_question}"
        
        return {
            "success": True,
            "message": welcome_message,
            "assessment_data": None,
            "assessment_complete": False
        }
    
    async def _process_aspirations_response(self, user_input: str, user_name: str, background: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Process user response with empathy and personalization"""
        self.interaction_count += 1
        
        # Determine if this should be a follow-up or completion
        should_complete = self.interaction_count >= 3
        
        if should_complete:
            return await self._complete_assessment(user_input, user_name, background, user_profile)
        else:
            return await self._ask_follow_up(user_input, user_name, background)
    
    async def _ask_follow_up(self, user_input: str, user_name: str, background: str) -> Dict[str, Any]:
        """Ask personalized follow-up questions"""
        prompt = f"""As a Career Aspirations Counselor, respond warmly and personally to this response about career aspirations:

        User ({user_name}, {background}): "{user_input}"
        
        Your response should:
        1. Acknowledge and validate their aspirations with genuine enthusiasm
        2. Show you're actively listening by referencing specific details they shared
        3. Ask ONE insightful follow-up question that helps them think deeper
        4. Use their name and maintain a warm, encouraging tone
        5. Help them connect their aspirations to concrete possibilities
        
        Respond with JSON: {{"message": "your warm, personalized response with follow-up question", "assessment_data": null, "assessment_complete": false}}"""
        
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
            follow_up = random.choice(self.follow_up_questions)
            return {
                "success": True,
                "message": f"Thank you for sharing that, {user_name}! Your aspirations show real thoughtfulness about your future. {follow_up}",
                "assessment_data": None,
                "assessment_complete": False
            }
    
    async def _complete_assessment(self, user_input: str, user_name: str, background: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Complete the aspirations assessment with personalized insights"""
        prompt = f"""As an expert Career Aspirations Counselor, complete the assessment for {user_name}, a {background}.

        Their final response: "{user_input}"
        Background: {background}
        
        Based on all their responses, provide a comprehensive aspirations assessment:

        Respond with JSON:
        {{
            "message": "warm, encouraging message that celebrates their vision and connects it to real possibilities",
            "assessment_data": {{
                "short_term_goals": ["specific 1-2 year goals based on their responses"],
                "long_term_vision": "detailed description of their 5-10 year career vision",
                "career_themes": ["main themes in their aspirations"],
                "motivation_drivers": ["what truly drives their career ambitions"],
                "success_definition": "how they personally define career success",
                "growth_mindset_indicators": ["evidence of growth-oriented thinking"],
                "alignment_with_values": "how their aspirations align with their apparent values",
                "realistic_pathway": "assessment of how achievable their goals are",
                "inspiration_sources": ["what seems to inspire their career vision"],
                "impact_focus": "the kind of impact they want to make"
            }},
            "assessment_complete": true
        }}"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            result = json.loads(response.content.strip().replace("```json", "").replace("```", ""))
            
            # Add personalized completion message
            completion_message = f"\n\n🎯 **Assessment Complete!** {user_name}, I'm inspired by your career vision and the thoughtfulness you've shown in defining your professional aspirations. Your goals show both ambition and authenticity - a powerful combination for career success. These insights will be valuable as we continue building your personalized career plan."
            
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
                "message": f"Thank you, {user_name}! Based on our conversation, I can see you have a clear vision for your career growth and meaningful aspirations that align with your values. Your thoughtful approach to career planning is already a strength that will serve you well.",
                "assessment_data": {
                    "short_term_goals": ["Build relevant skills and experience", "Expand professional network"],
                    "long_term_vision": "Achieve meaningful career growth while maintaining personal values and work-life balance",
                    "career_themes": ["Growth-oriented", "Purpose-driven", "Balanced approach"],
                    "success_definition": "Professional fulfillment combined with personal satisfaction"
                },
                "assessment_complete": True
            }
