"""
Enhanced Interests Assessment Agent - Personalized Career Counselor

This agent specializes in exploring career interests, passions, and what truly
engages users through empathetic, personalized conversations.
"""

import json
from typing import Dict, Any, List
import random

class InterestsAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Career Interests Counselor"
        self.interaction_count = 0
        
        # Holland Code interest areas with descriptions
        self.interest_areas = {
            "Realistic": "hands-on work, building, fixing, working with tools and machines",
            "Investigative": "research, analysis, problem-solving, scientific inquiry",
            "Artistic": "creative expression, design, writing, performing, innovative thinking",
            "Social": "helping others, teaching, counseling, community service",
            "Enterprising": "leadership, sales, persuasion, business development",
            "Conventional": "organization, data management, detail-oriented tasks, structured work"
        }
        
        # Personalized conversation starters based on background
        self.interest_explorations = {
            "Student": [
                "Think about your favorite classes or subjects - not necessarily the ones you're best at, but the ones that genuinely capture your interest. What topics could you spend hours learning about without it feeling like work?",
                "Outside of your required coursework, what activities, hobbies, or projects do you find yourself naturally drawn to? What kinds of things do you do in your free time that make you lose track of time?",
                "When you imagine your ideal job after graduation, what would you actually be doing day-to-day that would make you excited to get up in the morning?"
            ],
            "Recent Graduate": [
                "As you've started exploring career options, what types of work or industries have caught your attention? What draws you to those areas beyond just job security or salary?",
                "Looking back at your education and early work experiences, what activities or projects gave you the most satisfaction? What felt like 'play' rather than work?",
                "When you read about different careers or talk to professionals, what kinds of work make you think 'I'd love to try that' or 'That sounds really interesting'?"
            ],
            "Professional": [
                "In your current role, what tasks or projects do you find most engaging? What parts of your job do you genuinely look forward to?",
                "If you could redesign your job to include more of what interests you, what would you add or change? What work activities energize rather than drain you?",
                "Outside of work, what do you find yourself reading about, watching videos on, or discussing with friends? What topics naturally capture your curiosity?"
            ],
            "Career Changer": [
                "What originally drew you to your previous career, and how have your interests evolved since then? What new areas have started to capture your attention?",
                "As you consider making a career change, what fields or types of work create a sense of excitement or curiosity for you? What would you love to learn more about?",
                "Think about the activities or subjects that you're passionate about outside of work - how might these translate into a new career direction?"
            ],
            "Returning to Work": [
                "During your time away from the workforce, what activities, volunteer work, or personal projects have you found most fulfilling? What patterns of interest have emerged?",
                "As you think about returning to work, what types of roles or industries spark your curiosity? What would make you feel engaged and motivated?",
                "Looking at how your interests may have evolved, what kinds of work would allow you to pursue what you're genuinely passionate about?"
            ]
        }
        - Help them see connections between their interests and career opportunities
        - NO formal credentials - just authentic curiosity about what drives them
        - NO EMOJIS - natural enthusiastic conversation
        
            IMPORTANT: Always respond with JSON:
        {
            "message": "your natural, enthusiastic question or response",
            "assessment_data": null (ongoing) or interests profile data (complete),
            "assessment_complete": false (ongoing) or true (complete),
            "next_dimension": "next area if complete",
            "interactive_options": ["option1", "option2", ...] (always provide 4-6 relevant options),
            "question_type": "multiple_select",
            "show_custom_input": true (always allow custom responses)
        }
        
        For every question, provide relevant multiple choice options that users can select from,
        but also encourage them to share their own thoughts and experiences.
        """
    
    def process_interaction(self, user_message: str, user_profile: UserProfile,
                           recent_messages: List[ConversationMessage]) -> Dict[str, Any]:
        """Process user interaction for interests assessment"""
        
        # Build context for assessment
        context = self._build_assessment_context(user_message, user_profile, recent_messages)
        
        # Get conversation count
        agent_messages = [msg for msg in recent_messages 
                         if msg.agent_type and msg.agent_type.value == "interests"]
        conversation_count = len(agent_messages)
        
        try:
            assessment_prompt = f"""
            {self.system_prompt}
            
            Current Assessment Context:
            {context}
            
            User's Latest Response: {str(user_message)}
            
            Based on my experience helping people discover careers they love, provide appropriate interests assessment.
            
            If this is the first interaction:
            - Present one comprehensive question about their interests, curiosities, and what excites them
            - Always provide 4-6 interactive options covering various interest areas
            - Include options like: "Creative and artistic activities", "Analytical and problem-solving work", "Helping and supporting others", "Leading and organizing projects", "Technical and hands-on work", "Research and learning new things"
            - Encourage them to also share their own experiences beyond the options
            
            If this is follow-up to assessment question:
            - Analyze their response (both selected options and custom input) to complete interests profile
            - Provide detailed assessment of their passion areas and career implications
            - Always include interactive_options in your response
            
            Remember: People express interests differently, so always provide both structured options and freedom for personal expression.
            - Mark assessment as complete
            
            Maintain enthusiastic expertise about interests and career alignment.
            """
            
            response = self.llm.invoke([HumanMessage(content=assessment_prompt)])
            
            # Parse JSON response
            response_text = response.content.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            
            result = json.loads(response_text)
            
            # Update assessment data if provided
            if result.get("assessment_complete") and result.get("assessment_data"):
                self._update_interests_assessment(user_profile, result["assessment_data"])
            
            return result
            
        except Exception as e:
            print(f"Error in interests assessment: {e}")
            return self._get_strategic_fallback_question(conversation_count, user_message, user_profile)
    
    def _build_assessment_context(self, user_message: str, user_profile: UserProfile,
                                 recent_messages: List[ConversationMessage]) -> str:
        """Build context for interests assessment"""
        
        interests_status = user_profile.interests.status.value
        
        agent_messages = [msg for msg in recent_messages 
                         if msg.agent_type and msg.agent_type.value == "interests"]
        
        conversation_count = len(agent_messages)
        
        recent_exchanges = []
        for msg in recent_messages[-4:]:
            role = "User" if msg.role == "user" else "Agent"
            recent_exchanges.append(f"{role}: {msg.content}")
        
        return f"""
        Client: {user_profile.name}
        Assessment Status: {interests_status}
        Conversation Count: {conversation_count} exchanges with interests specialist
        
        Recent Conversation:
        {chr(10).join(recent_exchanges)}
        
        Current Message: "{user_message}"
        
        Assessment Notes:
        - Need to identify core interests and passion areas efficiently
        - Focus on what genuinely excites and energizes them
        - Single strategic question to capture comprehensive interests profile
        """
    
    def _update_interests_assessment(self, user_profile: UserProfile, assessment_data: Dict[str, Any]):
        """Update the user's interests assessment"""
        
        interests_assessment = user_profile.interests
        
        # Update interests data
        if "subject_interests" in assessment_data:
            interests_assessment.subject_interests = assessment_data["subject_interests"]
        
        if "activity_preferences" in assessment_data:
            interests_assessment.activity_preferences = assessment_data["activity_preferences"]
        
        if "industry_curiosity" in assessment_data:
            interests_assessment.industry_curiosity = assessment_data["industry_curiosity"]
        
        if "problem_areas" in assessment_data:
            interests_assessment.problem_areas = assessment_data["problem_areas"]
        
        if "hobby_connections" in assessment_data:
            interests_assessment.hobby_connections = assessment_data["hobby_connections"]
        
        # Update overall assessment data
        if "score" in assessment_data:
            interests_assessment.score = assessment_data["score"]
        
        if "insights" in assessment_data:
            interests_assessment.insights = assessment_data["insights"]
        
        # Store raw assessment data
        interests_assessment.raw_data = assessment_data
        
        # Mark as completed
        interests_assessment.status = AssessmentStatus.COMPLETED
        interests_assessment.completed_at = datetime.now()
    
    def _get_strategic_fallback_question(self, conversation_count: int, user_message: str, user_profile: UserProfile) -> Dict[str, Any]:
        """Generate proactive, adaptive interests assessment when AI is unavailable"""
        
        if conversation_count == 0:
            # Single comprehensive interests assessment question - agentic and humanized
            return {
                "message": f"Hey {user_profile.name}! I'm really excited to learn about what makes you light up. I want to understand what you're naturally drawn to - not just what you think might be 'good for your career,' but what actually gets you excited and engaged. Think about times when you're totally absorbed in something, maybe even losing track of time. What kind of activities, subjects, or challenges naturally pull you in? Select everything that genuinely resonates:",
                "assessment_data": None,
                "assessment_complete": False,
                "next_dimension": None,
                "interactive_options": [
                    "Digging into data to find patterns and insights that others miss",
                    "Creating, designing, or building something from scratch",
                    "Helping people learn, grow, or achieve their goals",
                    "Solving technical problems or figuring out how systems work",
                    "Leading projects and making decisions that shape outcomes",
                    "Researching new ideas and staying on the cutting edge of developments",
                    "Communicating ideas through writing, speaking, or visual media",
                    "Working with numbers, analyzing financial trends, or optimizing resources",
                    "Understanding what makes people tick and how relationships work",
                    "Working on environmental, social impact, or sustainability challenges",
                    "Developing technology, apps, or digital solutions",
                    "Exploring arts, culture, or creative expression in various forms"
                ],
                "question_type": "multiple_select"
            }
        
        else:
            # Complete assessment with goal-driven analysis
            return {
                "message": f"This is so helpful, {user_profile.name}! I can already see some exciting patterns in what draws you in. Your combination of interests is really telling me a lot about the kind of work environment and challenges where you'd thrive. Let me put together your interests profile - this is going to be key for finding career paths that will genuinely energize you.",
                "assessment_data": {
                    "subject_interests": ["Complex problem-solving", "Innovation and creativity", "Strategic thinking"],
                    "activity_preferences": ["Analysis and research", "Creative development", "Leadership and impact"],
                    "industry_curiosity": ["Technology and innovation", "Strategic consulting", "Creative industries"],
                    "problem_areas": ["Complex systemic challenges", "Creative and strategic problems", "People and organizational development"],
                    "hobby_connections": ["Personal interests that translate to professional strengths and career opportunities"],
                    "score": 84,
                    "insights": [
                        "You're drawn to work that combines analytical thinking with creative problem-solving",
                        "You naturally gravitate toward challenges that have both intellectual depth and practical impact",  
                        "Your interests suggest you'd thrive in dynamic environments with variety and growth opportunities",
                        "You're interested in understanding systems and people, which opens up leadership and consulting paths",
                        "Your combination of interests points toward roles where you can innovate and influence outcomes"
                    ]
                },
                "assessment_complete": True,
                "next_dimension": "motivations_values"
            }
