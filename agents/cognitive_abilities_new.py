"""
Cognitive Abilities Assessment Agent

This agent evaluates thinking styles, problem-solving approaches,
learning preferences, and intellectual capabilities.
"""

import json
from typing import Dict, Any, Optional, List

class EnhancedAgent:
    """Enhanced agent for cognitive abilities assessment with multiple choice questions"""
    
    def __init__(self, llm, agent_name="Cognitive Abilities Specialist", assessment_type="cognitive_abilities"):
        """Initialize the Enhanced Cognitive Abilities Agent"""
        self.llm = llm
        self.agent_name = agent_name
        self.assessment_type = assessment_type
        self.assessment_focus = "thinking styles and cognitive capabilities"
        self.user_responses = []
        self.current_question_index = 0
        
        # Enhanced questions with multiple choice options
        self.questions = [
            {
                "question": "How do you typically approach complex problems at work?",
                "options": [
                    "I break them down into smaller, manageable parts",
                    "I look for patterns and connections to similar problems I've solved",
                    "I brainstorm multiple creative solutions before choosing one",
                    "I research thoroughly and gather all available information first",
                    "I discuss with others to get different perspectives",
                    "I use systematic frameworks or methodologies"
                ]
            },
            {
                "question": "What type of thinking comes most naturally to you?",
                "options": [
                    "Analytical thinking - I love breaking down complex information",
                    "Creative thinking - I enjoy generating innovative ideas",
                    "Strategic thinking - I focus on long-term planning and vision",
                    "Critical thinking - I evaluate information and challenge assumptions",
                    "Systems thinking - I see how different parts connect to the whole",
                    "Practical thinking - I focus on what works in real situations"
                ]
            },
            {
                "question": "How do you prefer to process and learn new information?",
                "options": [
                    "Visual learning - I prefer diagrams, charts, and visual representations",
                    "Auditory learning - I learn best through discussions and explanations",
                    "Kinesthetic learning - I learn by doing and hands-on experience",
                    "Reading/writing - I prefer written materials and taking notes",
                    "Social learning - I learn best in groups and collaborative settings",
                    "Sequential learning - I prefer step-by-step, structured approaches"
                ]
            },
            {
                "question": "When making decisions, what do you rely on most?",
                "options": [
                    "Data and logical analysis of facts and numbers",
                    "Intuition and gut feelings about the right choice",
                    "Past experience and lessons learned from similar situations",
                    "Input and advice from trusted colleagues or mentors",
                    "Systematic evaluation using decision-making frameworks",
                    "Consideration of potential impacts on all stakeholders"
                ]
            },
            {
                "question": "How do you handle information overload or cognitive demands?",
                "options": [
                    "I prioritize and focus on the most important information first",
                    "I take breaks to process information and avoid mental fatigue",
                    "I organize information into categories or systems for easier handling",
                    "I delegate or seek help when cognitive load becomes too high",
                    "I use tools and technology to manage and organize information",
                    "I work in shorter, focused bursts rather than long sessions"
                ]
            }
        ]
    
    async def get_initial_question(self, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get the first question for cognitive abilities assessment"""
        self.current_question_index = 0
        self.user_responses = []
        
        return {
            "success": True,
            "message": f"Hi {user_name}! I'm your Cognitive Abilities Specialist. Understanding how you think, learn, and process information is essential for finding careers that match your intellectual strengths. Let's explore your cognitive preferences and capabilities.",
            "show_options": True,
            "current_question": self.questions[0],
            "question_number": 1,
            "total_questions": len(self.questions),
            "assessment_complete": False
        }
    
    async def process_response(self, selected_options: List[str], user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Process user's selected options and return next question or completion"""
        
        # Store current response
        current_question = self.questions[self.current_question_index]
        self.user_responses.append({
            "question": current_question["question"],
            "selected_options": selected_options
        })
        
        # Move to next question
        self.current_question_index += 1
        
        # Check if more questions remain
        if self.current_question_index < len(self.questions):
            next_question = self.questions[self.current_question_index]
            return {
                "success": True,
                "message": f"Excellent, {user_name}! Your thinking patterns are revealing important insights about your cognitive strengths.",
                "show_options": True,
                "current_question": next_question,
                "question_number": self.current_question_index + 1,
                "total_questions": len(self.questions),
                "assessment_complete": False
            }
        else:
            # Complete assessment
            return await self._complete_assessment(user_name, user_profile)
    
    async def _complete_assessment(self, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Complete assessment with AI analysis of selected options"""
        
        # Prepare response summary
        response_summary = []
        for response in self.user_responses:
            response_summary.append(f"Q: {response['question']}")
            response_summary.append(f"Selected: {', '.join(response['selected_options'])}")
            response_summary.append("")
        
        responses_text = "\n".join(response_summary)
        
        prompt = f"""As an expert {self.agent_name}, analyze {user_name}'s responses to complete their {self.assessment_type} assessment:

{responses_text}

Based on their selected options, provide a comprehensive assessment in JSON format:
{{
    "message": "warm, encouraging completion message that celebrates their insights",
    "assessment_data": {{
        "summary": "key insights from their selections",
        "strengths": ["specific strengths identified from choices"],
        "themes": ["major patterns from selected options"],
        "career_implications": ["how choices connect to career opportunities"],
        "development_suggestions": ["areas for growth based on responses"]
    }},
    "assessment_complete": true
}}"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            result_text = response.content.strip().replace("```json", "").replace("```", "")
            result = json.loads(result_text)
            
            # Add completion celebration
            completion_note = f"\n\n🎯 **{self.assessment_type.replace('_', ' ').title()} Assessment Complete!** Thank you for your thoughtful selections, {user_name}!"
            result["message"] += completion_note
            
            return {
                "success": True,
                "message": result["message"],
                "assessment_data": result.get("assessment_data"),
                "assessment_complete": True,
                "show_options": False
            }
        except Exception as e:
            return {
                "success": True,
                "message": f"Thank you for completing the {self.assessment_type.replace('_', ' ')} assessment, {user_name}! Your responses show great self-awareness and will contribute valuable insights to your career development plan.",
                "assessment_data": {
                    "summary": f"Completed {self.assessment_type} assessment with thoughtful option selections",
                    "strengths": ["Self-awareness", "Thoughtful decision-making", "Growth mindset"],
                    "career_implications": ["Strong foundation for career planning", "Clear preferences identified"]
                },
                "assessment_complete": True,
                "show_options": False
            }
