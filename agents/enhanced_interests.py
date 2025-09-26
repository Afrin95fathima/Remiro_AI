"""
Enhanced Interests Agent - Advanced Career Assessment

This agent explores what truly engages a person, focusing on passions and areas 
of intrinsic curiosity. It uses empathetic conversation and personalized questions
to understand career interests deeply.
"""

from typing import Dict, Any, List, Optional
from agents.enhanced_base_agent import EnhancedBaseAgent
import json

class InterestsAgent(EnhancedBaseAgent):
    """🎪 Interests Agent - Explores career interests, passions, and engagement drivers"""
    
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            agent_name="Career Interests Specialist", 
            assessment_type="interests",
            core_domain="Career interests, passions, and engagement drivers"
        )
        
        # Holland Code categories for analysis
        self.holland_codes = {
            "Realistic": "hands-on work, building, fixing, working with tools and machines",
            "Investigative": "research, analysis, problem-solving, scientific inquiry", 
            "Artistic": "creative expression, design, writing, performing, innovative thinking",
            "Social": "helping others, teaching, counseling, community service",
            "Enterprising": "leadership, sales, persuasion, business development",
            "Conventional": "organization, data management, detail-oriented tasks, structured work"
        }
    
    def get_predefined_questions(self) -> List[Dict[str, str]]:
        """Return the 3 predefined questions for interests assessment"""
        return [
            {
                "id": "interests_q1",
                "question": "You know what, I'm really curious - what kind of stuff do you find yourself doing where you just completely lose track of time? Like, you look up and suddenly hours have passed?",
                "context": "exploration",
                "purpose": "Identify intrinsic interests and flow states"
            },
            {
                "id": "interests_q2", 
                "question": "When you think about work or projects you've really enjoyed, what was it about them that got you excited? Was it the hands-on building stuff, figuring out complex problems, helping people, leading teams, organizing things, or creating something totally new?",
                "context": "pattern_recognition",
                "purpose": "Map to Holland Code categories"
            },
            {
                "id": "interests_q3",
                "question": "If someone said 'hey, you've got a whole day to just learn about whatever you want - no pressure, no tests, just pure curiosity' - what would you dive into and why?",
                "context": "application", 
                "purpose": "Understand learning motivations and curiosity drivers"
            }
        ]
    
    def get_spectrum_analysis(self, responses: List[str]) -> Dict[str, Any]:
        """Analyze user responses to determine their interests profile clarity"""
        
        try:
            # Create analysis prompt
            analysis_prompt = f"""
            As a Career Interests Specialist, analyze these user responses to assess their interests profile:
            
            Responses:
            1. Activities that make them lose track of time: {responses[0] if len(responses) > 0 else 'Not provided'}
            2. Nature of work they enjoyed most: {responses[1] if len(responses) > 1 else 'Not provided'}
            3. Subject they'd love to learn about: {responses[2] if len(responses) > 2 else 'Not provided'}
            
            Analyze and provide a JSON response with:
            {{
                "profile_clarity": "clear" or "unclear",
                "primary_holland_codes": ["list of 1-3 most relevant Holland codes"],
                "interest_themes": ["list of 3-5 key interest themes identified"],
                "passion_level": "high" or "medium" or "low",
                "career_alignment": "strong" or "moderate" or "needs_exploration",
                "key_insights": ["list of 2-3 key insights about their interests"],
                "development_areas": ["areas where interests could be further explored"],
                "summary": "2-3 sentence summary of their interests profile"
            }}
            
            Holland Codes Reference:
            - Realistic: hands-on, building, tools, machines
            - Investigative: research, analysis, problem-solving
            - Artistic: creative expression, design, innovation
            - Social: helping others, teaching, community service  
            - Enterprising: leadership, sales, persuasion
            - Conventional: organization, data management, structure
            """
            
            response = self.llm.invoke([{"role": "user", "content": analysis_prompt}])
            
            # Try to parse JSON response
            try:
                analysis = json.loads(response.content)
                return analysis
            except json.JSONDecodeError:
                # Fallback analysis
                return self._create_fallback_analysis(responses)
                
        except Exception as e:
            print(f"Error in interests analysis: {e}")
            return self._create_fallback_analysis(responses)
    
    def _create_fallback_analysis(self, responses: List[str]) -> Dict[str, Any]:
        """Create fallback analysis if AI analysis fails"""
        
        combined_text = " ".join(responses).lower()
        
        # Simple keyword mapping to Holland codes
        code_keywords = {
            "Realistic": ["build", "fix", "tool", "machine", "hands-on", "craft", "technical"],
            "Investigative": ["research", "analyze", "solve", "investigate", "study", "science"],
            "Artistic": ["create", "design", "art", "music", "write", "creative", "innovative"],
            "Social": ["help", "teach", "counsel", "people", "community", "social"],
            "Enterprising": ["lead", "sell", "persuade", "business", "manage", "entrepreneur"],
            "Conventional": ["organize", "data", "detail", "structure", "plan", "systematic"]
        }
        
        detected_codes = []
        for code, keywords in code_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                detected_codes.append(code)
        
        return {
            "profile_clarity": "clear" if len(detected_codes) <= 3 else "unclear",
            "primary_holland_codes": detected_codes[:3] if detected_codes else ["Investigative"],
            "interest_themes": ["General exploration needed"],
            "passion_level": "medium",
            "career_alignment": "needs_exploration",
            "key_insights": ["Interests require deeper exploration", "Multiple potential paths identified"],
            "development_areas": ["Interest clarification", "Career exploration"],
            "summary": "User shows varied interests that would benefit from further exploration and career counseling."
        }
    
    def get_interaction_requirements(self) -> Dict[str, List[str]]:
        """Define interaction requirements with other agents"""
        return {
            "requires_input_from": ["skills", "constraints"],
            "provides_input_to": ["aspirations", "motivations_values", "track_record"],
            "cross_reference_with": ["personality", "learning_preferences"],
            "influence_description": "Interest findings guide skill development priorities and must be validated against practical constraints and existing capabilities."
        }