"""
Constraints Assessment Agent

This agent evaluates limitations, barriers, and constraints that might 
affect career choices and professional development.
"""

import json
from typing import Dict, Any, Optional, List

class EnhancedAgent:
    """Enhanced agent for constraints assessment with multiple choice questions"""
    
    def __init__(self, llm, agent_name="Constraints Analyst", assessment_type="constraints"):
        """Initialize the Enhanced Constraints Agent"""
        self.llm = llm
        self.agent_name = agent_name
        self.assessment_type = assessment_type
        self.assessment_focus = "career constraints and limitations"
        self.user_responses = []
        self.current_question_index = 0
        
        # Enhanced questions with multiple choice options
        self.questions = [
            {
                "question": "What geographic limitations do you have for your career?",
                "options": [
                    "I'm completely flexible and willing to relocate anywhere",
                    "I'm open to relocating within my country",
                    "I prefer to stay in my current region but could consider nearby areas",
                    "I need to stay in my current city due to family obligations",
                    "I can only work remotely due to personal circumstances",
                    "I have specific climate or location preferences"
                ]
            },
            {
                "question": "How do financial considerations affect your career choices?",
                "options": [
                    "I need immediate high income to support financial obligations",
                    "I can take moderate financial risk for career growth opportunities",
                    "I prioritize financial stability over rapid career advancement",
                    "I'm comfortable with lower initial pay if there's growth potential",
                    "I have financial support and can focus purely on career fit",
                    "I need benefits and job security more than high salary"
                ]
            },
            {
                "question": "What time commitments and schedule constraints do you face?",
                "options": [
                    "I can work any schedule including nights, weekends, and overtime",
                    "I prefer standard business hours but am flexible when needed",
                    "I need work-life balance and predictable schedules",
                    "I have family commitments that limit my available hours",
                    "I can only work part-time or flexible arrangements",
                    "I need remote or hybrid work options for scheduling flexibility"
                ]
            },
            {
                "question": "How do family or personal responsibilities impact your career decisions?",
                "options": [
                    "I have minimal personal commitments and full career flexibility",
                    "I need to balance career growth with family time",
                    "I'm the primary caregiver and need family-friendly employers",
                    "I have eldercare responsibilities that affect my availability",
                    "I need to consider my partner's career in decision-making",
                    "I have health considerations that impact work requirements"
                ]
            },
            {
                "question": "What educational or skill development constraints do you have?",
                "options": [
                    "I'm willing and able to pursue any additional education needed",
                    "I can do part-time learning or professional development",
                    "I prefer on-the-job training over formal education programs",
                    "I have time/financial limits on additional education",
                    "I learn best through practical experience rather than courses",
                    "I need employer support for any skill development programs"
                ]
            }
        ]
    
    async def get_initial_question(self, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get the first question for constraints assessment"""
        self.current_question_index = 0
        self.user_responses = []
        
        return {
            "success": True,
            "message": f"Hi {user_name}! I'm your Constraints Analyst. Understanding your limitations and constraints is crucial for finding realistic and sustainable career paths. Let's identify any factors that might influence your career decisions.",
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
                "message": f"Thank you, {user_name}! Understanding these constraints helps us find career paths that work within your real-world limitations.",
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
