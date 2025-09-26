"""
Enhanced Skills Agent - Advanced Career Assessment

This agent assesses current competencies and identifies areas for skill development.
It provides empathetic analysis of existing skills and growth opportunities.
"""

from typing import Dict, Any, List, Optional
from agents.enhanced_base_agent import EnhancedBaseAgent
import json

class SkillsAgent(EnhancedBaseAgent):
    """🛠️ Skills Agent - Assesses current competencies and skill development needs"""
    
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            agent_name="Skills Assessment Specialist",
            assessment_type="skills", 
            core_domain="Current competencies and skill development opportunities"
        )
        
        # Skill categories for analysis
        self.skill_categories = {
            "Technical": ["programming", "software", "tools", "technology", "systems"],
            "Communication": ["writing", "speaking", "presentation", "negotiation", "interpersonal"],
            "Leadership": ["management", "team", "leadership", "delegation", "coaching"],
            "Analytical": ["analysis", "problem-solving", "critical thinking", "data", "research"],
            "Creative": ["design", "creativity", "innovation", "brainstorming", "artistic"],
            "Organizational": ["planning", "project management", "time management", "coordination"]
        }
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        """Return the 3 predefined questions for skills assessment"""
        return [
            {
                "id": "skills_q1",
                "question": "I'm really curious about this - what's that one thing you're really good at that people always come to you for help with? Like, what's your superpower that consistently gets great results?",
                "context": "current_state",
                "purpose": "Identify strongest existing competency"
            },
            {
                "id": "skills_q2",
                "question": "You know that feeling when you're trying to do something and you think 'man, if I just knew how to do X, this would be so much easier'? What's that skill X for you right now?",
                "context": "gap_analysis", 
                "purpose": "Identify critical skill gaps"
            },
            {
                "id": "skills_q3",
                "question": "If someone handed you a learning budget and said 'go develop yourself!' - what course, certification, or skill would you jump on first to level up your career game?",
                "context": "development",
                "purpose": "Understand development priorities and career advancement awareness"
            }
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        """Analyze user responses to determine their skills profile"""
        
        try:
            analysis_prompt = f"""
            As a Skills Assessment Specialist, analyze these user responses to assess their skills profile:
            
            Responses:
            1. Their strongest skill that delivers results: {responses[0] if len(responses) > 0 else 'Not provided'}
            2. Skill they wish they had: {responses[1] if len(responses) > 1 else 'Not provided'}
            3. Course/certification they would pursue: {responses[2] if len(responses) > 2 else 'Not provided'}
            
            Provide a JSON response with:
            {{
                "profile_clarity": "clear" or "unclear",
                "primary_skill_categories": ["list of main skill categories they possess"],
                "strongest_skills": ["list of their top 3-5 skills"],
                "skill_gaps": ["list of skills they need to develop"],
                "development_readiness": "high" or "medium" or "low",
                "skill_marketability": "high" or "medium" or "low",
                "key_insights": ["2-3 insights about their skill profile"],
                "recommended_development": ["specific development recommendations"],
                "career_impact": "how their skills align with career goals",
                "summary": "2-3 sentence summary of their skills assessment"
            }}
            
            Skill Categories:
            - Technical: programming, software, tools, technology
            - Communication: writing, speaking, presentation
            - Leadership: management, team leadership, coaching
            - Analytical: problem-solving, critical thinking, data analysis
            - Creative: design, innovation, artistic abilities
            - Organizational: planning, project management, coordination
            """
            
            response = self.llm.invoke([{"role": "user", "content": analysis_prompt}])
            
            try:
                analysis = json.loads(response.content)
                return analysis
            except json.JSONDecodeError:
                return self._create_fallback_analysis(responses)
                
        except Exception as e:
            print(f"Error in skills analysis: {e}")
            return self._create_fallback_analysis(responses)
    
    def _create_fallback_analysis(self, responses: List[str]) -> Dict[str, Any]:
        """Create fallback analysis if AI analysis fails"""
        
        combined_text = " ".join(responses).lower()
        
        # Detect skill categories
        detected_categories = []
        for category, keywords in self.skill_categories.items():
            if any(keyword in combined_text for keyword in keywords):
                detected_categories.append(category)
        
        return {
            "profile_clarity": "clear" if responses else "unclear",
            "primary_skill_categories": detected_categories[:3] if detected_categories else ["General"],
            "strongest_skills": ["Skills assessment needed"],
            "skill_gaps": ["Gap analysis required"],
            "development_readiness": "medium",
            "skill_marketability": "medium",
            "key_insights": ["Skills require detailed assessment", "Development opportunities identified"],
            "recommended_development": ["Comprehensive skills audit recommended"],
            "career_impact": "Skills alignment needs evaluation",
            "summary": "User demonstrates awareness of skill development needs and shows readiness for professional growth."
        }
    
    def get_interaction_requirements(self) -> Dict[str, List[str]]:
        """Define interaction requirements with other agents"""
        return {
            "requires_input_from": ["interests", "track_record", "aspirations"],
            "provides_input_to": ["learning_preferences", "constraints", "aspirations"],
            "cross_reference_with": ["cognitive_abilities", "strengths_weaknesses"],
            "influence_description": "Skills assessment informs development priorities and must align with interests and career aspirations while considering learning preferences."
        }