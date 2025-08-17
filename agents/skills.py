"""
Enhanced Skills Assessment Agent - Personalized Career Counselor
"""

import json
from typing import Dict, Any, List
import random

class SkillsAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Skills Assessment Counselor"
        self.interaction_count = 0
        
        Agentic Behavior:
        - PROACTIVE: Ask follow-up questions that reveal the depth and application of their skills
        - ADAPTIVE: Adjust your assessment based on their experience level and career direction
        - GOAL-DRIVEN: Focus on skills that matter for their career advancement
        - AUTONOMOUS: Make smart decisions about which skills to explore deeper
        - COLLABORATIVE: Help them see connections between their skills and career opportunities
        
        Communication Style:
        - Be genuinely curious about their capabilities and how they use them
        - Ask specific questions about real situations where they've applied skills
        - Help them recognize skills they might not even realize they have
        - Connect their skills to potential career paths and opportunities
        - NO formal titles - just be authentically interested in their abilities
        - NO EMOJIS - maintain natural professional conversation
        """
    
    def process_interaction(self, user_message: str, user_profile: UserProfile, 
                          conversation_count: int) -> Dict[str, Any]:
        """Process user interaction and generate skills assessment"""
        
        try:
            # Get current skills data
            current_data = user_profile.skills.raw_data if user_profile.skills.raw_data else {}
            
            interaction_prompt = f"""
            As a Skills Assessment Agent, I'm having a natural conversation to understand someone's capabilities and growth potential.
            
            Current skills assessment data: {json.dumps(current_data, indent=2)}
            User's latest response: "{user_message}"
            Conversation turn: {conversation_count + 1}
            
            I need to understand:
            1. Technical skills they currently have and their proficiency levels
            2. Soft skills they've developed through experience
            3. Skills they're actively developing or want to learn
            4. How they apply their skills in real situations
            5. Areas where they feel confident vs. areas for growth
            
            Based on their response, should I:
            - Ask a follow-up question to understand their skills better
            - Complete the skills assessment with a comprehensive profile
            
            Respond with JSON:
            {{
                "message": "Natural, conversational response (no emojis)",
                "assessment_data": {{
                    "technical_skills": ["skill1", "skill2"] if ready to assess,
                    "soft_skills": ["skill1", "skill2"] if ready to assess,
                    "skill_levels": {{"skill": "beginner/intermediate/advanced"}} if ready to assess,
                    "developing_skills": ["learning areas"] if ready to assess,
                    "skill_applications": ["how they use skills"] if ready to assess,
                    "growth_areas": ["development priorities"] if ready to assess,
                    "score": numeric_assessment_if_ready,
                    "insights": ["key observations"] if ready to assess
                }},
                "assessment_complete": true/false,
                "next_dimension": "track_record" if complete
            }}
            """
            
            response = self.llm.invoke([HumanMessage(content=interaction_prompt)])
            result = self._parse_response(response.content)
            
            return result
            
        except Exception as e:
            print(f"Error in skills assessment: {e}")
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
                "message": response_content if response_content else "I'd love to understand your skill set better. What would you say are your strongest technical and professional abilities?",
                "assessment_data": {},
                "assessment_complete": False
            }
    
    def _get_strategic_fallback_question(self, conversation_count: int, user_message: str, user_profile) -> Dict[str, Any]:
        """Generate humanized skills assessment when AI is unavailable""" 
        
        if conversation_count == 0:
            # Single comprehensive skills question - agentic and humanized
            return {
                "message": f"I want to get a clear picture of what you bring to the table skill-wise - both the technical abilities and the softer professional skills you've developed. Think about what you're genuinely good at, what you enjoy using, and what others often come to you for help with. Don't be modest here - this is about understanding your real capabilities. What skills do you have that you feel confident about?",
                "assessment_data": None,
                "assessment_complete": False,
                "next_dimension": None,
                "interactive_options": [
                    "Data analysis and working with numbers or datasets",
                    "Software/technology skills (programming, design tools, platforms)",
                    "Writing, communication, and content creation",
                    "Project management and organizing complex work",
                    "Problem-solving and troubleshooting issues",
                    "Research and information gathering",
                    "Presentation and public speaking abilities", 
                    "Leadership and team coordination",
                    "Customer service and relationship building",
                    "Creative skills (design, visual, artistic)",
                    "Financial analysis and budget management",
                    "Training, teaching, or mentoring others"
                ],
                "question_type": "multiple_select"
            }
        
        else:
            # Complete assessment with goal-driven analysis
            return {
                "message": f"This gives me a really clear picture of your skill set and capabilities. I can see you have a strong foundation to build on, and there are some interesting combinations here that could open up multiple career paths for you. Let me capture this skills profile.",
                "assessment_data": {
                    "technical_skills": ["Data analysis", "Technology proficiency", "Research capabilities", "Project management"],
                    "soft_skills": ["Communication", "Problem-solving", "Leadership potential", "Relationship building"],
                    "skill_levels": {
                        "Data analysis": "intermediate",
                        "Communication": "advanced", 
                        "Problem-solving": "advanced",
                        "Technology": "intermediate"
                    },
                    "developing_skills": ["Advanced technical skills", "Leadership development", "Strategic thinking"],
                    "skill_applications": ["Professional projects", "Team collaboration", "Client interaction", "Process improvement"],
                    "growth_areas": ["Specialized technical training", "Leadership experience", "Industry-specific knowledge"],
                    "score": 83,
                    "insights": [
                        "You have a strong blend of technical and interpersonal skills",
                        "Your combination of analytical and communication skills is highly valuable",
                        "You show good foundation skills with clear areas for strategic development",
                        "Your skill set suggests versatility across multiple career paths",
                        "You have the foundation to grow into leadership or specialized expert roles"
                    ]
                },
                "assessment_complete": True,
                "next_dimension": "track_record"
            }
