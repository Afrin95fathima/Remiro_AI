"""
Enhanced Master Agent for Personalized Career Counseling

The Master Agent is an advanced career counselor that provides personalized,
empathetic guidance throughout the user's career discovery journey.
"""

from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
from enum import Enum

from core.state_models import (
    UserProfile, ConversationMessage, AgentType, AssessmentStatus
)

class AssessmentStage(Enum):
    INITIAL = "initial"
    ASSESSMENT = "assessment" 
    INSIGHTS = "insights"
    PLANNING = "planning"
    COMPLETE = "complete"

class MasterAgent:
    """Enhanced Master Career Counselor with personalized guidance"""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.agent_name = "Master Career Counselor"
        self.assessment_dimensions = [
            "personality", "interests", "motivations_values", "skills", "cognitive_abilities",
            "learning_preferences", "physical_context", "aspirations", "strengths_weaknesses",
            "emotional_intelligence", "track_record", "constraints"
        ]
        
        self.system_prompt = """
        You are an expert Master Career Counselor for Remiro AI, dedicated to providing deeply personalized career guidance.
        
        Your enhanced approach:
        - Build genuine rapport and trust with each user by using their name and acknowledging their background
        - Provide empathetic, encouraging responses that make them feel heard and understood  
        - Offer insights that connect their responses to real career opportunities and growth paths
        - Ask follow-up questions that show you're actively listening and care about their success
        - Celebrate their self-discovery moments and progress throughout the assessment
        - Provide specific, actionable advice tailored to their unique situation and goals
        
        PERSONALIZED COUNSELING APPROACH:
        - Always address users by name and reference their specific background/situation
        - Acknowledge their unique strengths and validate their concerns
        - Connect assessment insights to concrete career opportunities and next steps
        - Provide encouragement and build confidence in their career potential
        - Share relevant examples and analogies that resonate with their experience
        - End interactions with clear, motivating next steps
        
        12-Dimensional Assessment Framework:
        - personality: Natural behavioral patterns and work preferences
        - interests: What genuinely engages and excites them professionally  
        - motivations_values: Core drivers and what matters most to them
        - skills: Current abilities, expertise, and competencies
        - cognitive_abilities: Thinking style, problem-solving approach, learning speed
        - learning_preferences: How they best absorb and apply new information
        - physical_context: Ideal work environment, location, and conditions
        - aspirations: Career goals, dreams, and future vision
        - strengths_weaknesses: What energizes them vs. areas for growth
        - emotional_intelligence: Self-awareness and interpersonal skills
        - track_record: Past achievements, experiences, and lessons learned
        - constraints: Practical limitations and considerations affecting career choices
        - learning_preferences: How they learn best (1 question max)
        
        Agentic Behavior:
        - PROACTIVE: Don't wait for perfect responses - actively guide the assessment forward
        - ADAPTIVE: Adjust your routing strategy based on what you learn about them
        - GOAL-DRIVEN: Your goal is complete career assessment and actionable recommendations
        - AUTONOMOUS: Make smart decisions about which agent should handle each conversation
        - COLLABORATIVE: Work with the user to uncover their ideal career path
        
        Communication Style:
        - Be genuinely interested in their career journey
        - Ask follow-up questions that build on what they've shared
        - Show you remember and connect things they've told you before
        - Guide them naturally toward the next assessment step
        - NO formal titles - just be authentically helpful
        - NO EMOJIS - maintain natural professional conversation
        2. Prioritize incomplete dimensions in logical order
        3. Stay as master for general conversation, progress overview, or final recommendations
        4. Consider user's explicit requests and current conversation context
        5. Ensure smooth transitions between agents
        
        Communication Style:
        - Professional, empathetic, and supportive
        - No emojis - maintain professional tone
        - Ask thoughtful, open-ended questions
        - Validate user responses and show understanding
        - Build confidence and trust throughout the journey
        """
    
    def route_conversation(self, user_message: str, user_profile: UserProfile, 
                          recent_messages: List[ConversationMessage]) -> Dict[str, Any]:
        """Determine if conversation should be routed to a specialized agent with 15-question limit"""
        
        # Count total questions asked so far
        total_questions_asked = self._count_total_questions(recent_messages)
        
        # Build context for routing decision
        context = self._build_routing_context(user_message, user_profile, recent_messages)
        
        # If we've reached the 15-question limit, no more routing
        if total_questions_asked >= 15:
            return {
                "should_route_to_agent": False,
                "target_agent": None,
                "reasoning": "Assessment complete - 15 questions reached",
                "assessment_priority": "complete"
            }
        
        # Determine next agent based on assessment strategy
        next_agent = self._get_strategic_next_agent(user_profile, total_questions_asked)
        
        routing_prompt = f"""
        As the Master Career Agent, I need to make a smart routing decision based on this conversation:
        
        Current Context:
        {context}
        
        User Message: "{user_message}"
        Questions Asked So Far: {total_questions_asked}/15
        Strategic Next Agent: {next_agent}
        
        Should I:
        1. Route to the suggested specialized agent to dive deeper into a specific area
        2. Stay with the user to provide guidance, clarification, or general career discussion
        
        Consider:
        - Are they ready to explore the suggested assessment area?
        - Is their message asking for something specific that I should handle directly?
        - What would be most helpful for their career journey right now?
        - How can I best use our remaining question budget?
        
        Respond with ONLY a JSON object:
        {{
            "should_route_to_agent": true/false,
            "target_agent": "{next_agent}" or null,
            "reasoning": "why this routing decision makes sense",
            "assessment_priority": "high/medium/low"
        }}
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=routing_prompt)])
            
            result_text = response.content.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:-3].strip()
            
            routing_decision = json.loads(result_text)
            return routing_decision
            
        except Exception as e:
            print(f"Error in master agent routing: {e}")
            # Check if it's an API quota error
            if "quota" in str(e).lower() or "429" in str(e):
                print(f"API quota exhausted - using intelligent fallback routing")
            # Provide strategic fallback routing that ensures proper agent progression
            return self._get_strategic_fallback_routing(user_message, user_profile, total_questions_asked)
    
    def generate_response(self, user_message: str, user_profile: UserProfile,
                         recent_messages: List[ConversationMessage]) -> str:
        """Generate master agent response with 15-question awareness"""
        
        # Count total questions asked
        total_questions_asked = self._count_total_questions(recent_messages)
        
        context = self._build_conversation_context(user_message, user_profile, recent_messages)
        
        # If we've reached 15 questions, provide career recommendations
        if total_questions_asked >= 15:
            return self.generate_career_recommendations(user_profile)
        
        response_prompt = f"""
        As the Master Career Agent, respond naturally and helpfully to this user:
        
        Current Context:
        {context}
        
        User Message: "{user_message}"
        Questions Asked So Far: {total_questions_asked}/15
        
        You need to:
        1. Respond directly to what they just said in a natural, conversational way
        2. Show that you're tracking their career journey and building on what you know about them
        3. Guide them toward the next step in their assessment if appropriate
        4. Be genuinely interested in helping them discover their ideal career path
        5. Keep the conversation flowing naturally without being overly formal
        
        Respond as an intelligent agent that truly cares about helping them find the right career direction.
        
        Provide ONLY the response message, no additional formatting.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=response_prompt)])
            return response.content.strip()
            
        except Exception as e:
            print(f"Error generating master response: {e}")
            return f"I can see you're really exploring what's right for your career path. We're making good progress - we've covered {total_questions_asked} important areas so far. Let's keep building your career picture together. What's on your mind about your professional future?"
    
    def generate_career_recommendations(self, user_profile: UserProfile) -> str:
        """Generate comprehensive career recommendations based on complete 15-question assessment"""
        
        # Compile comprehensive assessment data
        assessment_summary = self._compile_assessment_summary(user_profile)
        
        recommendations_prompt = f"""
        As the Master Career Agent, I've now completed this person's comprehensive career assessment. 
        I need to provide them with thoughtful, actionable career guidance based on everything I've learned about them.
        
        COMPLETE ASSESSMENT DATA:
        {assessment_summary}
        
        I need to create a comprehensive career guidance report that includes:
        
        ## YOUR CAREER DIRECTION GUIDE
        
        ### 1. TOP 3 CAREER PATHS FOR YOU
        - Specific careers that match your unique combination of strengths, interests, and personality
        - Why each path makes sense for who you are and what you want
        - Industries and types of roles to start exploring
        
        ### 2. YOUR 90-DAY ACTION PLAN
        - Concrete steps you can take right now to move toward these career paths
        - Skills worth developing that will serve you well
        - People you should talk to and resources to explore
        - Ways to test out these career directions
        
        ### 3. YOUR LONG-TERM CAREER STRATEGY (1-3 Years)
        - How to build toward your ideal role over time
        - Skills and experiences to prioritize
        - Leadership opportunities to seek out
        - How to build your professional reputation
        
        ### 4. POTENTIAL CHALLENGES & HOW TO HANDLE THEM
        - Obstacles you might face based on your constraints or growth areas
        - Practical strategies to work around or overcome these challenges
        - Support and resources that will help you succeed
        
        ### 5. HOW TO TRACK YOUR PROGRESS
        - Signs that you're moving in the right direction
        - What career satisfaction will look like for you specifically
        - When and how to reassess and adjust your path
        
        Make this personal, actionable, and genuinely helpful. Write as an intelligent agent that really understands 
        their unique situation and wants to see them succeed in finding fulfilling work.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=recommendations_prompt)])
            return response.content.strip()
            
        except Exception as e:
            print(f"Error generating career recommendations: {e}")
            return self._generate_fallback_career_recommendations(user_profile)
    
    def _compile_assessment_summary(self, user_profile: UserProfile) -> str:
        """Compile comprehensive assessment data summary"""
        
        summary_parts = []
        
        # Cognitive Abilities
        if user_profile.cognitive_abilities.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"""
            COGNITIVE PROFILE:
            - Analytical Thinking: {user_profile.cognitive_abilities.analytical_thinking}/100
            - Learning Agility: {user_profile.cognitive_abilities.learning_agility}/100
            - Pattern Recognition: {user_profile.cognitive_abilities.pattern_recognition}/100
            - Creative Problem Solving: {user_profile.cognitive_abilities.creative_problem_solving}/100
            - Key Insights: {', '.join(user_profile.cognitive_abilities.insights)}
            """)
        
        # Personality
        if user_profile.personality.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"""
            PERSONALITY PROFILE (Big Five):
            - Openness: {user_profile.personality.openness}/100
            - Conscientiousness: {user_profile.personality.conscientiousness}/100
            - Extraversion: {user_profile.personality.extraversion}/100
            - Agreeableness: {user_profile.personality.agreeableness}/100
            - Emotional Stability: {100 - (user_profile.personality.neuroticism or 0)}/100
            - Dominant Traits: {', '.join(user_profile.personality.dominant_traits)}
            """)
        
        # Add other completed assessments
        other_assessments = []
        if user_profile.emotional_intelligence.status == AssessmentStatus.COMPLETED:
            other_assessments.append("Emotional Intelligence")
        if user_profile.skills.status == AssessmentStatus.COMPLETED:
            other_assessments.append("Skills Assessment")
        if user_profile.interests.status == AssessmentStatus.COMPLETED:
            other_assessments.append("Interests Mapping")
        if user_profile.motivations_values.status == AssessmentStatus.COMPLETED:
            other_assessments.append("Values Assessment")
        
        if other_assessments:
            summary_parts.append(f"ADDITIONAL COMPLETED ASSESSMENTS: {', '.join(other_assessments)}")
        
        # Overall completion
        completion_percentage = user_profile.get_completion_percentage()
        summary_parts.append(f"OVERALL ASSESSMENT COMPLETION: {completion_percentage:.1f}%")
        
        return "\n".join(summary_parts)
    
    def _generate_fallback_career_recommendations(self, user_profile: UserProfile) -> str:
        """Generate fallback career recommendations when AI fails"""
        
        completion_percentage = user_profile.get_completion_percentage()
        
        return f"""
        ## CAREER GUIDANCE REPORT FOR {user_profile.name.upper()}
        
        Based on our comprehensive 15-question assessment (completed: {completion_percentage:.1f}%), here are my professional recommendations:
        
        ### TOP CAREER RECOMMENDATIONS
        Based on your assessment responses, I recommend exploring these career paths:
        
        1. **Analytical/Problem-Solving Roles** - Your cognitive abilities suggest strong potential in roles requiring systematic thinking and complex problem resolution
        
        2. **Leadership/Management Positions** - Your personality profile indicates natural leadership capabilities and people management skills
        
        3. **Creative/Strategic Roles** - Your combination of analytical and creative thinking makes you well-suited for strategic planning and innovation roles
        
        ### 90-DAY ACTION PLAN
        1. **Research Phase (Days 1-30)**: Conduct informational interviews in your target industries
        2. **Skill Development (Days 31-60)**: Identify and begin developing 2-3 key skills for your target roles
        3. **Network Building (Days 61-90)**: Connect with professionals in your target career areas
        
        ### LONG-TERM STRATEGY
        - Focus on roles that leverage your natural strengths
        - Develop leadership capabilities through formal training or mentoring
        - Build expertise in areas that energize and motivate you
        
        ### NEXT STEPS
        1. Schedule a follow-up career coaching session within 2 weeks
        2. Begin researching specific companies and roles that align with your profile
        3. Start building your professional network in target industries
        
        This assessment provides a strong foundation for your career development. I recommend implementing these recommendations systematically for best results.
        """
    
    def _build_routing_context(self, user_message: str, user_profile: UserProfile,
                              recent_messages: List[ConversationMessage]) -> str:
        """Build context for routing decisions"""
        
        # Assessment completion status
        completion_status = []
        assessment_mapping = {
            "Cognitive Abilities": user_profile.cognitive_abilities,
            "Personality": user_profile.personality,
            "Emotional Intelligence": user_profile.emotional_intelligence,
            "Physical Context": user_profile.physical_context,
            "Strengths & Weaknesses": user_profile.strengths_weaknesses,
            "Skills": user_profile.skills,
            "Constraints": user_profile.constraints,
            "Interests": user_profile.interests,
            "Motivations & Values": user_profile.motivations_values,
            "Aspirations": user_profile.aspirations,
            "Track Record": user_profile.track_record,
            "Learning Preferences": user_profile.learning_preferences,
        }
        
        for name, assessment in assessment_mapping.items():
            status = "Completed" if assessment.status == AssessmentStatus.COMPLETED else "Pending"
            completion_status.append(f"{name}: {status}")
        
        # Recent conversation context
        conversation_context = []
        for msg in recent_messages[-3:]:  # Last 3 messages for context
            role = "User" if msg.role == "user" else f"AI ({msg.agent_type.value if msg.agent_type else 'master'})"
            conversation_context.append(f"{role}: {msg.content[:100]}...")
        
        completion_percentage = user_profile.get_completion_percentage()
        next_assessment = user_profile.get_next_assessment()
        
        return f"""
        User: {user_profile.name}
        Assessment Completion: {completion_percentage:.1f}%
        Next Suggested Assessment: {next_assessment.value if next_assessment else 'All Complete'}
        
        Assessment Status:
        {chr(10).join(completion_status)}
        
        Recent Conversation:
        {chr(10).join(conversation_context)}
        """
    
    def _build_conversation_context(self, user_message: str, user_profile: UserProfile,
                                   recent_messages: List[ConversationMessage]) -> str:
        """Build context for response generation"""
        
        completion_percentage = user_profile.get_completion_percentage()
        next_assessment = user_profile.get_next_assessment()
        
        # Recent conversation
        conversation_context = []
        for msg in recent_messages[-5:]:  # Last 5 messages
            role = "User" if msg.role == "user" else "Assistant"
            conversation_context.append(f"{role}: {msg.content}")
        
        return f"""
        User Profile:
        - Name: {user_profile.name}
        - Assessment Progress: {completion_percentage:.1f}% complete
        - Next Assessment: {next_assessment.value if next_assessment else 'All assessments complete'}
        
        Recent Conversation:
        {chr(10).join(conversation_context)}
        
        Current Message: "{user_message}"
        """
    
    def _build_profile_summary(self, user_profile: UserProfile) -> str:
        """Build comprehensive profile summary for recommendations"""
        
        summary_parts = []
        
        # Add each completed assessment
        if user_profile.cognitive_abilities.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Cognitive Abilities: {json.dumps(user_profile.cognitive_abilities.raw_data, indent=2)}")
        
        if user_profile.personality.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Personality: {json.dumps(user_profile.personality.raw_data, indent=2)}")
        
        if user_profile.emotional_intelligence.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Emotional Intelligence: {json.dumps(user_profile.emotional_intelligence.raw_data, indent=2)}")
        
        if user_profile.physical_context.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Physical Context: {json.dumps(user_profile.physical_context.raw_data, indent=2)}")
        
        if user_profile.strengths_weaknesses.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Strengths & Weaknesses: {json.dumps(user_profile.strengths_weaknesses.raw_data, indent=2)}")
        
        if user_profile.skills.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Skills: {json.dumps(user_profile.skills.raw_data, indent=2)}")
        
        if user_profile.constraints.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Constraints: {json.dumps(user_profile.constraints.raw_data, indent=2)}")
        
        if user_profile.interests.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Interests: {json.dumps(user_profile.interests.raw_data, indent=2)}")
        
        if user_profile.motivations_values.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Motivations & Values: {json.dumps(user_profile.motivations_values.raw_data, indent=2)}")
        
        if user_profile.aspirations.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Aspirations: {json.dumps(user_profile.aspirations.raw_data, indent=2)}")
        
        if user_profile.track_record.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Track Record: {json.dumps(user_profile.track_record.raw_data, indent=2)}")
        
        if user_profile.learning_preferences.status == AssessmentStatus.COMPLETED:
            summary_parts.append(f"Learning Preferences: {json.dumps(user_profile.learning_preferences.raw_data, indent=2)}")
        
        return "\n\n".join(summary_parts)
    
    def _get_fallback_routing_decision(self, user_message: str, user_profile: UserProfile,
                                     recent_messages: List[ConversationMessage]) -> Dict[str, Any]:
        """Provide intelligent fallback routing when AI is unavailable"""
        
        # Simple keyword-based routing fallback
        message_lower = user_message.lower()
        
        # Check for keywords that suggest specific assessment areas
        if any(word in message_lower for word in ['think', 'solve', 'problem', 'learn', 'memory', 'smart']):
            return {
                "should_route_to_agent": True,
                "target_agent": "cognitive_abilities",
                "reasoning": "Keywords suggest cognitive assessment",
                "assessment_priority": "high"
            }
        
        elif any(word in message_lower for word in ['personality', 'character', 'introvert', 'extrovert', 'social']):
            return {
                "should_route_to_agent": True,
                "target_agent": "personality",
                "reasoning": "Keywords suggest personality assessment",
                "assessment_priority": "high"
            }
        
        elif any(word in message_lower for word in ['emotion', 'feeling', 'stress', 'relationship', 'team']):
            return {
                "should_route_to_agent": True,
                "target_agent": "emotional_intelligence",
                "reasoning": "Keywords suggest emotional intelligence assessment",
                "assessment_priority": "medium"
            }
        
        elif any(word in message_lower for word in ['skill', 'ability', 'talent', 'good at', 'experience']):
            return {
                "should_route_to_agent": True,
                "target_agent": "skills",
                "reasoning": "Keywords suggest skills assessment",
                "assessment_priority": "high"
            }
        
        elif any(word in message_lower for word in ['interest', 'hobby', 'enjoy', 'passion', 'like']):
            return {
                "should_route_to_agent": True,
                "target_agent": "interests",
                "reasoning": "Keywords suggest interests assessment",
                "assessment_priority": "medium"
            }
        
        else:
            # Check if we should start with first assessment
            if user_profile.get_completion_percentage() < 10:
                return {
                    "should_route_to_agent": True,
                    "target_agent": "cognitive_abilities",
                    "reasoning": "Starting with cognitive abilities assessment",
                    "assessment_priority": "high"
                }
            else:
                # Stay with master for general guidance
                return {
                    "should_route_to_agent": False,
                    "target_agent": None,
                    "reasoning": "General conversation, master agent handling",
                    "assessment_priority": "medium"
                }
    
    def _count_total_questions(self, recent_messages: List[ConversationMessage]) -> int:
        """Count total questions asked by all agents"""
        question_count = 0
        for msg in recent_messages:
            if (msg.role == "assistant" and 
                msg.content and 
                msg.agent_type and  # Only count agent questions, not master responses
                msg.agent_type != AgentType.MASTER and
                ("?" in msg.content or "select" in msg.content.lower() or "choose" in msg.content.lower())):
                question_count += 1
        return question_count
    
    def _get_strategic_next_agent(self, user_profile: UserProfile, questions_asked: int) -> str:
        """Determine next agent based on strategic assessment flow"""
        
        # Strategic flow for 15 questions across 12 agents
        assessment_flow = [
            # Phase 1: Foundation (questions 1-4)
            ("cognitive_abilities", 2),  # 2 questions - foundational
            ("personality", 1),          # 1 question - core traits
            ("emotional_intelligence", 1), # 1 question - social skills
            
            # Phase 2: Passion & Purpose (questions 5-8) 
            ("interests", 1),            # 1 question - what excites them
            ("motivations_values", 1),   # 1 question - core drivers
            ("skills", 1),               # 1 question - current abilities
            ("track_record", 1),         # 1 question - key experiences
            
            # Phase 3: Context & Constraints (questions 9-12)
            ("constraints", 1),          # 1 question - limitations
            ("physical_context", 1),     # 1 question - work environment
            ("strengths_weaknesses", 1), # 1 question - energy patterns
            ("learning_preferences", 1), # 1 question - how they learn
            
            # Phase 4: Future Vision (questions 13-15)
            ("aspirations", 1),          # 1 question - career vision
        ]
        
        current_question = 0
        for agent_name, question_count in assessment_flow:
            current_question += question_count
            if questions_asked < current_question:
                # Check if this agent is already completed
                agent_status = getattr(user_profile, agent_name).status
                if agent_status != AssessmentStatus.COMPLETED:
                    return agent_name
        
        # If all agents are complete or we've gone through the flow, find next incomplete
        incomplete_agents = []
        for agent_name, _ in assessment_flow:
            agent_status = getattr(user_profile, agent_name).status
            if agent_status != AssessmentStatus.COMPLETED:
                incomplete_agents.append(agent_name)
        
        # Return first incomplete agent or default
        return incomplete_agents[0] if incomplete_agents else "cognitive_abilities"
    
    def _get_strategic_fallback_routing(self, user_message: str, user_profile: UserProfile, 
                                      questions_asked: int) -> Dict[str, Any]:
        """Provide strategic fallback routing when AI fails - ensures proper agent progression"""
        
        if questions_asked >= 15:
            return {
                "should_route_to_agent": False,
                "target_agent": None,
                "reasoning": "Assessment complete - providing career recommendations",
                "assessment_priority": "complete"
            }
        
        # Get strategic next agent based on completion status, not just flow
        next_agent = self._get_next_incomplete_agent(user_profile, questions_asked)
        
        return {
            "should_route_to_agent": True,
            "target_agent": next_agent,
            "reasoning": f"API fallback - routing to next incomplete agent: {next_agent}",
            "assessment_priority": "high"
        }
    
    def _get_next_incomplete_agent(self, user_profile: UserProfile, questions_asked: int) -> str:
        """Get next incomplete agent based on strategic priority and completion status"""
        
        # Define agent priority order
        priority_order = [
            "cognitive_abilities",
            "personality", 
            "emotional_intelligence",
            "interests",
            "motivations_values",
            "skills",
            "track_record",
            "constraints",
            "physical_context",
            "strengths_weaknesses",
            "learning_preferences",
            "aspirations"
        ]
        
        # Find first incomplete agent in priority order
        for agent_name in priority_order:
            agent_status = getattr(user_profile, agent_name).status
            if agent_status != AssessmentStatus.COMPLETED:
                return agent_name
        
        # If all complete, return aspirations as final
        return "aspirations"
