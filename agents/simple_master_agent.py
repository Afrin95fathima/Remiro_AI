"""
Simple Master Agent - Fallback Implementation

This is a simplified version of the master agent that can work independently
if the full enhanced system is not available.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class SimpleMasterAgent:
    """Simple master agent for basic career assistance"""
    
    def __init__(self, llm):
        self.llm = llm
        self.conversation_history = []
        self.assessment_progress = {}
        
        # Basic 12D questions
        self.assessment_questions = {
            'interests': [
                "What activities or topics make you lose track of time?",
                "What type of work have you enjoyed most in the past?",
                "What subject would you love to learn about?"
            ],
            'skills': [
                "What skill do you possess that delivers the best results?",
                "What skill do you wish you had to make work easier?", 
                "What course would you take for professional development?"
            ],
            'personality': [
                "Do you work better alone or in teams?",
                "Do you prefer fast-paced or structured environments?",
                "How do you handle workplace conflicts?"
            ],
            'aspirations': [
                "What does your successful career look like in 5 years?",
                "What represents your ultimate professional ambition?",
                "What's your next concrete career step?"
            ]
        }
        
        self.current_agent = None
        self.current_question_index = 0
    
    def process_conversation(self, user_input: str, user_id: str = "default") -> Dict[str, Any]:
        """Process user conversation"""
        
        self.conversation_history.append({
            "user": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        user_lower = user_input.lower()
        
        # Check for assessment requests
        assessment_keywords = ['assessment', '12d', 'career test', 'start', 'begin']
        if any(keyword in user_lower for keyword in assessment_keywords):
            return self.start_assessment()
        
        # Check if in assessment
        if self.current_agent:
            return self.continue_assessment(user_input)
        
        # General conversation
        return self.generate_general_response(user_input)
    
    def start_assessment(self) -> Dict[str, Any]:
        """Start the assessment process"""
        
        self.current_agent = 'interests'
        self.current_question_index = 0
        
        if 'interests' not in self.assessment_progress:
            self.assessment_progress['interests'] = {
                'started': True,
                'completed': False,
                'responses': []
            }
        
        first_question = self.assessment_questions['interests'][0]
        
        return {
            "type": "assessment_question",
            "message": f"Great! Let's start your 12D career assessment. {first_question}",
            "current_agent": "interests",
            "question_index": 0,
            "progress": "1/4 - Interests Assessment"
        }
    
    def continue_assessment(self, user_input: str) -> Dict[str, Any]:
        """Continue current assessment"""
        
        # Store response
        self.assessment_progress[self.current_agent]['responses'].append(user_input)
        self.current_question_index += 1
        
        questions = self.assessment_questions[self.current_agent]
        
        # Check if more questions for current agent
        if self.current_question_index < len(questions):
            next_question = questions[self.current_question_index]
            return {
                "type": "assessment_question",
                "message": f"Thank you! {next_question}",
                "current_agent": self.current_agent,
                "question_index": self.current_question_index,
                "progress": f"1/4 - {self.current_agent.title()} Assessment"
            }
        
        # Move to next agent
        self.assessment_progress[self.current_agent]['completed'] = True
        
        agent_order = ['interests', 'skills', 'personality', 'aspirations']
        current_index = agent_order.index(self.current_agent)
        
        if current_index + 1 < len(agent_order):
            # Next agent
            next_agent = agent_order[current_index + 1]
            self.current_agent = next_agent
            self.current_question_index = 0
            
            if next_agent not in self.assessment_progress:
                self.assessment_progress[next_agent] = {
                    'started': True,
                    'completed': False,
                    'responses': []
                }
            
            first_question = self.assessment_questions[next_agent][0]
            
            return {
                "type": "assessment_question", 
                "message": f"Excellent! Now let's explore your {next_agent}. {first_question}",
                "current_agent": next_agent,
                "question_index": 0,
                "progress": f"{current_index + 2}/4 - {next_agent.title()} Assessment"
            }
        
        # Assessment complete
        return self.complete_assessment()
    
    def complete_assessment(self) -> Dict[str, Any]:
        """Complete assessment and provide analysis"""
        
        self.current_agent = None
        
        # Generate simple analysis
        analysis = self.generate_simple_analysis()
        
        return {
            "type": "assessment_complete",
            "message": """🎉 Congratulations! Your career assessment is complete! 

Based on your responses, I've analyzed your profile and generated personalized recommendations for your career development.

Your assessment covers your interests, skills, personality, and aspirations. Would you like me to provide specific career recommendations or discuss any particular aspect in more detail?""",
            "analysis": analysis,
            "completion_time": datetime.now().isoformat()
        }
    
    def generate_simple_analysis(self) -> Dict[str, Any]:
        """Generate simple career analysis"""
        
        try:
            # Collect all responses
            all_responses = {}
            for agent, data in self.assessment_progress.items():
                if data.get('responses'):
                    all_responses[agent] = data['responses']
            
            # Generate AI analysis
            prompt = f"""
            Based on these career assessment responses, provide career recommendations:
            
            Assessment Data: {json.dumps(all_responses, indent=2)}
            
            Provide recommendations as JSON:
            {{
                "role_recommendations": [
                    {{"title": "Role Title", "match_score": 90, "reasons": ["reason1", "reason2"]}}
                ],
                "skill_development_plan": [
                    {{"skill": "Skill Name", "priority": "high", "timeline": "6 months"}}
                ],
                "career_roadmap": {{
                    "6_months": ["goal1", "goal2"],
                    "1_year": ["goal1", "goal2"],
                    "3_years": ["goal1", "goal2"]
                }},
                "summary": "Brief career profile summary"
            }}
            """
            
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            
            try:
                return json.loads(response.content)
            except:
                return self.create_fallback_analysis()
        
        except Exception as e:
            return self.create_fallback_analysis()
    
    def create_fallback_analysis(self) -> Dict[str, Any]:
        """Create basic fallback analysis"""
        return {
            "role_recommendations": [
                {"title": "Career Professional", "match_score": 85, "reasons": ["Strong assessment completion", "Clear career focus"]}
            ],
            "skill_development_plan": [
                {"skill": "Leadership", "priority": "high", "timeline": "6 months"}
            ],
            "career_roadmap": {
                "6_months": ["Complete skill assessment", "Build professional network"],
                "1_year": ["Pursue target role", "Gain relevant experience"],
                "3_years": ["Achieve leadership position", "Mentor others"]
            },
            "summary": "You have demonstrated strong career awareness and are ready for focused professional development."
        }
    
    def generate_general_response(self, user_input: str) -> Dict[str, Any]:
        """Generate general conversational response"""
        
        try:
            prompt = f"""
            You are Remiro AI, a career assistant. Respond helpfully to: {user_input}
            
            Be conversational, professional, and offer relevant career guidance.
            If appropriate, mention your 12D career assessment capability.
            """
            
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            
            return {
                "type": "general_response",
                "message": response.content,
                "suggestions": ["Start 12D Assessment", "Get Career Advice", "Ask About Skills"]
            }
        
        except Exception as e:
            return {
                "type": "general_response", 
                "message": "I'm here to help with your career questions! Would you like to start your 12D career assessment or discuss specific career topics?",
                "suggestions": ["Start Assessment", "Career Advice", "Industry Insights"]
            }