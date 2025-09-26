"""
Physical Context Assessment Agent

This agent evaluates physical work preferences, environment needs,
and accessibility requirements for optimal career matching.
"""

import json
from typing import Dict, Any, Optional, List

class EnhancedAgent:
    """Enhanced agent for physical context assessment with multiple choice questions"""
    
    def __init__(self, llm, agent_name="Physical Context Specialist", assessment_type="physical_context"):
        """Initialize the Enhanced Physical Context Agent"""
        self.llm = llm
        self.agent_name = agent_name
        self.assessment_type = assessment_type
        self.assessment_focus = "physical work environment and requirements"
        self.user_responses = []
        self.current_question_index = 0
        
        # Enhanced questions with multiple choice options
        self.questions = [
            {
                "question": "What type of physical work environment do you prefer?",
                "options": [
                    "Traditional office setting with desk work",
                    "Open collaborative workspace with flexible seating",
                    "Home office or remote work setup",
                    "Outdoor or field-based work environments",
                    "Laboratory, workshop, or specialized facility",
                    "Mixed environments - variety throughout the day/week"
                ]
            },
            {
                "question": "How much physical activity do you prefer in your work?",
                "options": [
                    "Primarily sedentary work with minimal physical demands",
                    "Light physical activity - walking, standing occasionally",
                    "Moderate activity - some lifting, walking, or movement",
                    "High activity - significant physical demands and movement",
                    "Variable activity levels depending on project needs",
                    "I have physical limitations that require accommodation"
                ]
            },
            {
                "question": "What are your preferences for work location and commuting?",
                "options": [
                    "I prefer working from home or remotely",
                    "I enjoy a short, easy commute to a nearby office",
                    "I don't mind longer commutes for the right opportunity",
                    "I prefer multiple work locations for variety",
                    "I like travel-based work with changing locations",
                    "Public transportation access is important to me"
                ]
            },
            {
                "question": "How important are specific environmental conditions for your productivity?",
                "options": [
                    "I need quiet, distraction-free environments to focus well",
                    "I thrive in busy, energetic environments with activity",
                    "I prefer natural light and windows in my workspace",
                    "Temperature control and comfortable seating are crucial",
                    "I need access to specialized equipment or technology",
                    "I'm very adaptable to different environmental conditions"
                ]
            },
            {
                "question": "Do you have any accessibility needs or physical considerations?",
                "options": [
                    "No special accommodations needed",
                    "I need ergonomic workspace setup for health reasons",
                    "I require accessibility features (ramps, elevators, etc.)",
                    "I have vision or hearing considerations that need support",
                    "I need flexible scheduling due to health conditions",
                    "I prefer not to discuss specific needs at this time"
                ]
            }
        ]
    
    async def get_initial_question(self, user_name: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get the first question for physical context assessment"""
        self.current_question_index = 0
        self.user_responses = []
        
        return {
            "success": True,
            "message": f"Hi {user_name}! I'm your Physical Context Specialist. Understanding your physical work preferences and any accommodation needs helps ensure you find careers in environments where you can be comfortable and productive. Let's explore your physical work preferences.",
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
                "message": f"Thank you, {user_name}! Understanding your physical work preferences helps us identify environments where you'll be most comfortable and productive.",
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
