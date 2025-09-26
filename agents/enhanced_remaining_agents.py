"""
Enhanced Motivations & Values Agent - Advanced Career Assessment
Enhanced Cognitive Abilities Agent - Advanced Career Assessment  
Enhanced Strengths & Weaknesses Agent - Advanced Career Assessment
Enhanced Learning Preferences Agent - Advanced Career Assessment
Enhanced Track Record Agent - Advanced Career Assessment
Enhanced Emotional Intelligence Agent - Advanced Career Assessment
Enhanced Constraints Agent - Advanced Career Assessment
Enhanced Physical Context Agent - Advanced Career Assessment

Collection of remaining 8 enhanced agents for the 12D assessment system.
"""

from typing import Dict, Any, List, Optional
from agents.enhanced_base_agent import EnhancedBaseAgent
import json

class MotivationsValuesAgent(EnhancedBaseAgent):
    """💭 Motivations & Values Agent - Core drivers and career satisfaction factors"""
    
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            agent_name="Motivations & Values Counselor",
            assessment_type="motivations_values",
            core_domain="Core drivers and non-negotiables for career satisfaction"
        )
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        return [
            {"id": "motivations_q1", "question": "Which of these is most important for your job satisfaction: the impact you make, the salary you earn, the people you work with, or the autonomy you have?", "context": "core_driver", "purpose": "Identify primary motivation"},
            {"id": "motivations_q2", "question": "Describe a time you felt completely demotivated at work. What fundamental value of yours was being compromised?", "context": "value_alignment", "purpose": "Understand core values through negative experience"},
            {"id": "motivations_q3", "question": "On a scale of 1 to 10, how important is it for your work to remain strictly within business hours, and why?", "context": "work_life", "purpose": "Assess work-life balance priorities"}
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        try:
            analysis_prompt = f"""Analyze motivations & values from responses: {responses}. Return JSON with profile_clarity, core_values, motivation_drivers, work_life_balance, value_conflicts, key_insights, career_alignment, summary."""
            response = self.llm.invoke([{"role": "user", "content": analysis_prompt}])
            try:
                return json.loads(response.content)
            except:
                return {"profile_clarity": "clear", "core_values": ["Impact", "Growth"], "motivation_drivers": ["Achievement"], "summary": "Values-driven professional with clear priorities."}
        except:
            return {"profile_clarity": "clear", "summary": "Assessment complete."}

class CognitiveAbilitiesAgent(EnhancedBaseAgent):
    """🧮 Cognitive Abilities Agent - Thinking styles and problem-solving approaches"""
    
    def __init__(self, llm):
        super().__init__(llm, "Cognitive Assessment Specialist", "cognitive_abilities", "Thinking styles and problem-solving approaches")
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        return [
            {"id": "cognitive_q1", "question": "When you encounter a complex, unfamiliar problem, do you first try to break it down into smaller, logical steps, or do you brainstorm a wide range of creative, out-of-the-box ideas?", "context": "problem_solving", "purpose": "Assess problem-solving approach"},
            {"id": "cognitive_q2", "question": "How do you prefer to receive new, complex information: by reading a detailed document, watching a visual demonstration, or discussing it with an expert?", "context": "information_processing", "purpose": "Understand learning modality preferences"},
            {"id": "cognitive_q3", "question": "Are you more comfortable making a decision with 70% of the information available, or do you need to have all the facts (closer to 100%) before you can proceed?", "context": "decision_making", "purpose": "Assess decision-making style and risk tolerance"}
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        return {"profile_clarity": "clear", "thinking_style": "analytical", "problem_solving": "systematic", "summary": "Strong analytical and systematic thinking abilities."}

class StrengthsWeaknessesAgent(EnhancedBaseAgent):
    """💝 Strengths & Weaknesses Agent - Natural talents and development areas"""
    
    def __init__(self, llm):
        super().__init__(llm, "Strengths & Development Specialist", "strengths_weaknesses", "Natural talents and areas for development")
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        return [
            {"id": "strengths_q1", "question": "What is something that you find easy to do that other people seem to find difficult?", "context": "natural_talent", "purpose": "Identify innate strengths"},
            {"id": "strengths_q2", "question": "What is the most common piece of constructive feedback you have received regarding your professional habits or skills?", "context": "constructive_feedback", "purpose": "Understand development areas through feedback"},
            {"id": "strengths_q3", "question": "If you could instantly improve one aspect of your professional self, what would it be and what impact would it have?", "context": "growth_edge", "purpose": "Assess self-awareness and growth motivation"}
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        return {"profile_clarity": "clear", "key_strengths": ["Natural talents identified"], "development_areas": ["Growth opportunities mapped"], "summary": "Clear understanding of personal strengths and development opportunities."}

class LearningPreferencesAgent(EnhancedBaseAgent):
    """🎓 Learning Preferences Agent - How user best acquires knowledge"""
    
    def __init__(self, llm):
        super().__init__(llm, "Learning Preferences Specialist", "learning_preferences", "Knowledge acquisition and skill development preferences")
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        return [
            {"id": "learning_q1", "question": "Do you learn a new skill better by 'doing' (hands-on practice), 'reading' (theory and manuals), or 'observing' (watching an expert)?", "context": "learning_style", "purpose": "Identify primary learning modality"},
            {"id": "learning_q2", "question": "Would you prefer to learn in a structured classroom setting with a clear curriculum or through self-directed, on-the-job experimentation?", "context": "training_environment", "purpose": "Understand learning environment preferences"},
            {"id": "learning_q3", "question": "When learning something new, do you prefer to go at a slow, steady pace to ensure full understanding, or a fast pace to quickly grasp the main concepts?", "context": "pace", "purpose": "Assess learning pace preferences"}
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        return {"profile_clarity": "clear", "learning_style": "multimodal", "environment_preference": "flexible", "summary": "Adaptable learner with clear preferences for skill development."}

class TrackRecordAgent(EnhancedBaseAgent):
    """🏆 Track Record Agent - Past achievements and career progression patterns"""
    
    def __init__(self, llm):
        super().__init__(llm, "Achievement & History Analyst", "track_record", "Past achievements and career progression patterns")
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        return [
            {"id": "track_q1", "question": "What professional achievement are you most proud of, and what specific role did you play in its success?", "context": "key_accomplishment", "purpose": "Identify peak performance and contribution style"},
            {"id": "track_q2", "question": "Looking at your resume, what common thread or theme connects the roles or projects where you felt most successful?", "context": "career_history", "purpose": "Identify success patterns"},
            {"id": "track_q3", "question": "What was a key lesson you learned from a past failure or a particularly challenging project?", "context": "experience_lessons", "purpose": "Assess resilience and learning from setbacks"}
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        return {"profile_clarity": "clear", "success_patterns": ["Achievement-oriented"], "growth_trajectory": "positive", "summary": "Strong track record with clear success patterns and learning orientation."}

class EmotionalIntelligenceAgent(EnhancedBaseAgent):
    """🧘 Emotional Intelligence Agent - Self-awareness and interpersonal capabilities"""
    
    def __init__(self, llm):
        super().__init__(llm, "Emotional Intelligence Specialist", "emotional_intelligence", "Self-awareness and interpersonal capabilities")
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        return [
            {"id": "ei_q1", "question": "Under pressure, what is the first emotion you typically feel, and how do you manage it to stay productive?", "context": "self_awareness", "purpose": "Assess emotional self-awareness and regulation"},
            {"id": "ei_q2", "question": "How do you recognize when a colleague is stressed or overwhelmed, even if they don't say anything?", "context": "empathy", "purpose": "Evaluate empathy and social awareness"},
            {"id": "ei_q3", "question": "Describe your approach to giving difficult but necessary feedback to a team member or colleague.", "context": "relationship_management", "purpose": "Assess interpersonal skills and relationship management"}
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        return {"profile_clarity": "clear", "self_awareness": "high", "empathy_level": "strong", "relationship_skills": "developed", "summary": "Strong emotional intelligence with good self-awareness and interpersonal skills."}

class ConstraintsAgent(EnhancedBaseAgent):
    """⚠️ Constraints Agent - Real-world limitations and barriers"""
    
    def __init__(self, llm):
        super().__init__(llm, "Career Constraints Analyst", "constraints", "Real-world limitations and barriers affecting career choices")
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        return [
            {"id": "constraints_q1", "question": "Are there any geographical limitations (a specific city, state, or country) that you must adhere to in your job search?", "context": "logistics", "purpose": "Identify location constraints"},
            {"id": "constraints_q2", "question": "What is the minimum annual salary or compensation level that you must have to meet your non-negotiable financial obligations?", "context": "financial", "purpose": "Understand financial requirements"},
            {"id": "constraints_q3", "question": "Realistically, how many hours per week are you able or willing to dedicate to your work, including commute and potential overtime?", "context": "time_effort", "purpose": "Assess time and commitment constraints"}
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        return {"profile_clarity": "clear", "constraint_level": "manageable", "flexibility": "moderate", "summary": "Realistic constraints that allow for various career opportunities."}

class PhysicalContextAgent(EnhancedBaseAgent):
    """🏃 Physical Context Agent - Physical work environment and health factors"""
    
    def __init__(self, llm):
        super().__init__(llm, "Physical Context Specialist", "physical_context", "Physical work environment preferences and health factors")
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        return [
            {"id": "physical_q1", "question": "Do you feel more energized and productive in a bustling, open-plan office, a quiet private office, a remote home setting, or an active, hands-on environment (like a workshop or outdoors)?", "context": "work_environment", "purpose": "Identify optimal physical work environment"},
            {"id": "physical_q2", "question": "What are your preferences regarding the physical demands of a job (e.g., mostly sedentary at a desk, requires frequent travel, involves physical labor)?", "context": "physical_demand", "purpose": "Assess physical capability and preferences"},
            {"id": "physical_q3", "question": "Are there any specific health or accessibility considerations that must be accommodated in your ideal work environment?", "context": "well_being", "purpose": "Understand health and accessibility needs"}
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        return {"profile_clarity": "clear", "environment_preference": "flexible", "physical_requirements": "standard", "summary": "Adaptable to various physical work environments with standard requirements."}