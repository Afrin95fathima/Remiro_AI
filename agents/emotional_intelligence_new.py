"""
Emotional Intelligence Assessment Agent

This agent evaluates emotional intelligence capabilities including
self-awareness, empathy, emotional regulation, and social skills.
"""

import json
from typing import Dict, Any, Optional, List

class EnhancedAgent:
    """Enhanced agent for emotional intelligence assessment with multiple choice questions"""
    
    def __init__(self, llm, agent_name="Emotional Intelligence Specialist", assessment_type="emotional_intelligence"):
        """Initialize the Enhanced Emotional Intelligence Agent"""
        self.llm = llm
        self.agent_name = agent_name
        self.assessment_type = assessment_type
        self.assessment_focus = "emotional intelligence and interpersonal skills"
        self.user_responses = []
        self.current_question_index = 0
        
        # Enhanced questions with multiple choice options
        self.questions = [
            {
                "question": "How do you typically handle workplace stress and pressure?",
                "options": [
                    "I stay calm and focused, using stress as motivation",
                    "I take regular breaks and practice mindfulness techniques",
                    "I talk through challenges with colleagues or mentors",
                    "I organize and prioritize tasks to manage workload",
                    "I sometimes feel overwhelmed but push through",
                    "I seek support when stress becomes unmanageable"
                ]
            },
            {
                "question": "When working in a team, how do you handle conflicts or disagreements?",
                "options": [
                    "I listen actively to understand different perspectives",
                    "I try to find common ground and compromise solutions",
                    "I address issues directly but diplomatically",
                    "I prefer to avoid confrontation when possible",
                    "I focus on facts and data to resolve disputes",
                    "I involve a mediator or supervisor when needed"
                ]
            },
            {
                "question": "How do you typically read and respond to others' emotional states?",
                "options": [
                    "I'm very intuitive about others' feelings and moods",
                    "I pay attention to body language and tone of voice",
                    "I ask direct questions about how people are feeling",
                    "I adjust my communication style based on the person",
                    "I sometimes miss social cues but learn from feedback",
                    "I prefer clear, direct communication over reading between lines"
                ]
            },
            {
                "question": "How do you manage your own emotions in professional settings?",
                "options": [
                    "I'm very self-aware and can regulate my emotions well",
                    "I use breathing techniques or brief mental breaks",
                    "I express emotions appropriately and constructively",
                    "I sometimes struggle but work on emotional control",
                    "I keep emotions separate from work decisions",
                    "I seek advice on handling difficult emotional situations"
                ]
            },
            {
                "question": "How do you typically motivate and inspire others?",
                "options": [
                    "I lead by example and maintain positive energy",
                    "I recognize and celebrate others' achievements",
                    "I provide emotional support during challenging times",
                    "I help others see the bigger picture and purpose",
                    "I offer practical help and resources when needed",
                    "I encourage open communication and feedback"
                ]
            }
        ]
    
    async def get_initial_question(self, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get the first question for emotional intelligence assessment"""
        self.current_question_index = 0
        self.user_responses = []
        
        return {
            "success": True,
            "message": f"Hi {user_name}! I'm your Emotional Intelligence Specialist. I'll help assess your emotional intelligence and interpersonal skills - crucial capabilities for career success and leadership. Let's explore how you handle emotions and relationships in professional settings.",
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
                "message": f"Great insights, {user_name}! Your emotional intelligence patterns are becoming clearer.",
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
