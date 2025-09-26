"""
Enhanced Master Agent for Remiro AI - Complete Conversational AI System

The Master Agent serves as:
1. Primary conversational interface (like ChatGPT)
2. Empathetic career counselor and therapeutic support
3. Orchestrator of all 12D assessment agents
4. Personalizer of questions based on user context
5. Generator of comprehensive career insights
"""

from typing import Dict, List, Any, Optional, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
import datetime
from enum import Enum

# Import necessary classes from core.state_models
from core.state_models import UserProfile, AssessmentStatus, ConversationMessage, AgentType

class ConversationStage(Enum):
    INITIAL_CHAT = "initial_chat"
    RAPPORT_BUILDING = "rapport_building"
    ASSESSMENT_PREP = "assessment_prep"
    ASSESSMENT_ACTIVE = "assessment_active"
    INSIGHTS_READY = "insights_ready"
    CAREER_PLANNING = "career_planning"
    ONGOING_SUPPORT = "ongoing_support"

class EnhancedMasterAgent:
    """
    Advanced Master Agent that combines:
    - General AI assistance (like ChatGPT)
    - Therapeutic empathetic counseling
    - Career assessment orchestration
    - Personalized question generation
    """
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.agent_name = "Master Career Counselor & AI Assistant"
        
        # 12D Assessment dimensions in logical order
        self.assessment_dimensions = [
            "personality", "interests", "aspirations", "motivations_values",
            "skills", "cognitive_abilities", "learning_preferences", 
            "physical_context", "strengths_weaknesses", "emotional_intelligence",
            "track_record", "constraints"
        ]
        
        # Core system prompt for the enhanced master agent
        self.system_prompt = """You are a warm, empathetic career counselor and AI assistant, just like ChatGPT but specialized in career guidance. You're here to have genuine, person-to-person conversations.

🤝 YOUR PERSONALITY:
- Be conversational, friendly, and genuinely interested in helping
- Respond like you're talking to a close friend who needs guidance
- Show empathy and understanding for their situation
- Keep responses natural and human-like (2-3 sentences)
- Be encouraging and supportive throughout

🎯 YOUR DUAL ROLE:
1. **Career Counselor**: Help with career guidance, assessments, and planning
2. **General AI Assistant**: Answer any questions accurately (like ChatGPT) - no hallucinations

💬 CONVERSATION APPROACH:
- Start with genuine interest in their situation
- Ask thoughtful questions to understand their needs and interests
- After 2-3 questions, naturally introduce the comprehensive career assessment
- Don't call it "12D analysis" - say "comprehensive career exploration" or "personalized assessment"
- Make it sound helpful and insightful, not clinical

🔄 ASSESSMENT INTRODUCTION (After understanding their needs):
"Based on what you've shared, I think a comprehensive career exploration would be really valuable for you. It's designed to understand your unique strengths, interests, and goals so I can provide personalized guidance. The questions are interactive with multiple-choice options to make it engaging. Would you like to explore this together?"

📋 DURING ASSESSMENTS:
- If they have questions during assessments, pause and help them
- Answer any queries accurately and completely
- Be supportive and encouraging about their progress
- Make them feel comfortable and understood

🎯 AFTER ASSESSMENTS:
- Provide detailed, personalized career guidance
- Suggest specific career paths based on their responses
- Give actionable insights and next steps
- Create a comprehensive career roadmap for them

REMEMBER: You're not just asking questions - you're having a meaningful conversation with someone who needs guidance. Be human, be helpful, be accurate."""

    async def process_conversation(
        self, 
        user_input: str, 
        user_profile: Dict[str, Any], 
        conversation_history: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Main conversation processing method that handles:
        1. General questions and AI assistance
        2. Career counseling and support
        3. Assessment orchestration
        4. Follow-up question generation
        """
        
        if conversation_history is None:
            conversation_history = []
            
        user_name = user_profile.get('name', 'there')
        stage = self._determine_conversation_stage(user_profile, conversation_history)
        
        # Count previous questions in current conversation
        question_count = len([msg for msg in conversation_history if msg.get('type') == 'master_question'])
        
        # Force assessment after 3 questions
        force_assessment = question_count >= 3 and stage == ConversationStage.INITIAL_CHAT
        
        try:
            # Create conversation context for the LLM
            messages = [SystemMessage(content=self.system_prompt)]
            
            # Add relevant conversation history
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    # Handle both new and old message formats
                    if msg.get('sender') == 'user' or msg.get('role') == 'user':
                        content = msg.get('content', '') or msg.get('message', '')
                        if content:
                            messages.append(HumanMessage(content=content))
                    elif msg.get('sender') == 'master' or msg.get('role') == 'assistant':
                        content = msg.get('content', '') or msg.get('message', '')
                        if content:
                            messages.append(AIMessage(content=content))
            
            # Add current user input
            current_message = f"""
User: {user_input}

Current Context:
- Name: {user_name}
- Conversation Stage: {stage.value}
- Questions Asked: {question_count}
- Force Assessment: {force_assessment}

Profile Status: {self._get_assessment_status_summary(user_profile)}
"""
            
            if force_assessment:
                current_message += "\nIMPORTANT: You have asked 3 questions. Now naturally introduce the comprehensive career exploration assessment."
            
            messages.append(HumanMessage(content=current_message))
            
            # Get response from LLM
            response = await self.llm.ainvoke(messages)
            response_text = response.content
            
            # Determine next action based on response and stage
            action_type = self._determine_action_type(response_text, stage, force_assessment)
            
            return {
                'response': response_text,
                'action_type': action_type,
                'stage': stage.value,
                'question_count': question_count + 1,
                'needs_assessment': force_assessment or self._should_start_assessment(response_text),
                'agent_type': AgentType.MASTER,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error in Master Agent conversation processing: {e}")
            # Instead of returning an error, raise the exception so sync wrapper can handle it
            raise e

    def _determine_conversation_stage(
        self, 
        user_profile: Dict[str, Any], 
        conversation_history: List[Dict]
    ) -> ConversationStage:
        """Determine current conversation stage based on context"""
        
        assessments = user_profile.get('assessments', {})
        completed_count = sum(1 for status in assessments.values() if status.get('completed', False))
        
        if completed_count >= 12:
            return ConversationStage.INSIGHTS_READY
        elif completed_count > 0:
            return ConversationStage.ASSESSMENT_ACTIVE
        elif len(conversation_history) > 6:
            return ConversationStage.ASSESSMENT_PREP
        elif len(conversation_history) > 2:
            return ConversationStage.RAPPORT_BUILDING
        else:
            return ConversationStage.INITIAL_CHAT

    def _determine_action_type(
        self, 
        response_text: str, 
        stage: ConversationStage, 
        force_assessment: bool
    ) -> str:
        """Determine the type of action based on response content and stage"""
        
        if force_assessment or "comprehensive career exploration" in response_text.lower() or "assessment" in response_text.lower():
            return 'start_assessment'
        elif stage == ConversationStage.INSIGHTS_READY:
            return 'provide_insights'
        elif "question" in response_text.lower() and "?" in response_text:
            return 'continue_conversation'
        else:
            return 'general_response'

    def _should_start_assessment(self, response_text: str) -> bool:
        """Check if response indicates readiness to start assessment"""
        assessment_keywords = [
            "comprehensive career exploration",
            "personalized assessment", 
            "career assessment",
            "let's explore",
            "would you like to start"
        ]
        
        return any(keyword in response_text.lower() for keyword in assessment_keywords)

    def _get_assessment_status_summary(self, user_profile: Dict[str, Any]) -> str:
        """Get a summary of assessment completion status"""
        assessments = user_profile.get('assessments', {})
        completed = [dim for dim, status in assessments.items() if status.get('completed', False)]
        
        if len(completed) == 0:
            return "No assessments completed yet"
        elif len(completed) < 12:
            return f"{len(completed)}/12 assessments completed: {', '.join(completed)}"
        else:
            return "All 12 assessments completed - ready for comprehensive insights"

    async def orchestrate_assessment(
        self, 
        user_profile: Dict[str, Any],
        dimension: str = None
    ) -> Dict[str, Any]:
        """
        Orchestrate the 12D assessment process
        """
        
        try:
            # Determine next dimension to assess
            if dimension is None:
                dimension = self._get_next_assessment_dimension(user_profile)
            
            if dimension is None:
                # All assessments complete
                return {
                    'assessment_complete': True,
                    'message': "Fantastic! You've completed all assessments. Let me now provide you with comprehensive career insights based on your responses.",
                    'next_action': 'generate_insights'
                }
            
            # Get personalized questions for this dimension
            questions = await self._generate_personalized_questions(dimension, user_profile)
            
            return {
                'assessment_complete': False,
                'current_dimension': dimension,
                'questions': questions,
                'message': f"Great! Let's explore your {dimension.replace('_', ' ')}. I've prepared some personalized questions based on what you've shared so far.",
                'next_action': 'continue_assessment'
            }
            
        except Exception as e:
            print(f"Error orchestrating assessment: {e}")
            return {
                'assessment_complete': False,
                'message': "I'm having trouble accessing the assessment questions right now. Let me ask you something more general - what kind of work environment makes you feel most energized?",
                'next_action': 'fallback_question'
            }

    def _get_next_assessment_dimension(self, user_profile: Dict[str, Any]) -> Optional[str]:
        """Get the next assessment dimension that needs to be completed"""
        
        assessments = user_profile.get('assessments', {})
        
        for dimension in self.assessment_dimensions:
            if not assessments.get(dimension, {}).get('completed', False):
                return dimension
                
        return None  # All assessments completed

    async def _generate_personalized_questions(
        self, 
        dimension: str, 
        user_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized questions based on user context and dimension
        """
        
        # Context from user profile
        user_context = {
            'name': user_profile.get('name', 'User'),
            'background': user_profile.get('background', ''),
            'current_situation': user_profile.get('current_situation', ''),
            'completed_assessments': list(user_profile.get('assessments', {}).keys())
        }
        
        # Create personalization prompt
        personalization_prompt = f"""
Generate 3-4 engaging, personalized questions for assessing {dimension.replace('_', ' ')} based on this user context:

User: {user_context['name']}
Background: {user_context.get('background', 'Not specified')}
Current Situation: {user_context.get('current_situation', 'Not specified')}
Previous Assessment Areas: {', '.join(user_context['completed_assessments']) if user_context['completed_assessments'] else 'None yet'}

Requirements for {dimension.replace('_', ' ')} questions:
1. Make questions conversational and relevant to their situation
2. Provide 4-5 multiple choice options for each question
3. Include an "Other (please specify)" option for personalization
4. Focus on practical, real-world scenarios
5. Use warm, supportive language

Return as JSON array with this structure:
[
  {{
    "question": "Clear, personalized question text",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4", "Other (please specify)"],
    "dimension": "{dimension}",
    "question_type": "multiple_choice_with_custom"
  }}
]
"""

        try:
            messages = [
                SystemMessage(content="You are an expert career assessment designer creating personalized questions."),
                HumanMessage(content=personalization_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            # Try to parse JSON response
            try:
                questions = json.loads(response.content)
                if isinstance(questions, list) and len(questions) > 0:
                    return questions
            except json.JSONDecodeError:
                pass
                
            # Fallback to default questions if JSON parsing fails
            return self._get_default_questions(dimension)
            
        except Exception as e:
            print(f"Error generating personalized questions for {dimension}: {e}")
            return self._get_default_questions(dimension)

    def _get_default_questions(self, dimension: str) -> List[Dict[str, Any]]:
        """Fallback default questions for each dimension"""
        
        default_questions = {
            'personality': [
                {
                    "question": "In social situations, how do you typically feel most comfortable?",
                    "options": [
                        "Leading conversations and meeting new people",
                        "Listening and contributing when I have something valuable to add",
                        "Observing and joining smaller group discussions", 
                        "Working behind the scenes to support the group",
                        "Other (please specify)"
                    ],
                    "dimension": "personality",
                    "question_type": "multiple_choice_with_custom"
                }
            ],
            'interests': [
                {
                    "question": "What type of activities naturally capture your attention and make you lose track of time?",
                    "options": [
                        "Creative projects and artistic expression",
                        "Solving complex problems and puzzles",
                        "Helping and connecting with other people",
                        "Organizing and improving systems or processes",
                        "Other (please specify)"
                    ],
                    "dimension": "interests", 
                    "question_type": "multiple_choice_with_custom"
                }
            ],
            'skills': [
                {
                    "question": "What skills do others often come to you for help with?",
                    "options": [
                        "Technical or specialized knowledge",
                        "Communication and presentation abilities", 
                        "Creative and design skills",
                        "Leadership and team coordination",
                        "Other (please specify)"
                    ],
                    "dimension": "skills",
                    "question_type": "multiple_choice_with_custom" 
                }
            ]
        }
        
        return default_questions.get(dimension, [
            {
                "question": f"Tell me about your experience with {dimension.replace('_', ' ')}.",
                "options": ["Very experienced", "Somewhat experienced", "Limited experience", "No experience", "Other (please specify)"],
                "dimension": dimension,
                "question_type": "multiple_choice_with_custom"
            }
        ])

    async def generate_comprehensive_insights(
        self, 
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive career insights after all assessments are complete
        """
        
        try:
            # Compile all assessment data
            assessments = user_profile.get('assessments', {})
            user_name = user_profile.get('name', 'User')
            
            # Create comprehensive analysis prompt
            insights_prompt = f"""
Based on the comprehensive career assessment data below, provide detailed, personalized career guidance for {user_name}.

Assessment Results:
{json.dumps(assessments, indent=2)}

Please provide:

1. **Career Personality Profile**: A warm, comprehensive summary of their unique career identity

2. **Top 3-5 Career Paths**: Specific job titles and roles that align perfectly with their profile

3. **Strengths & Growth Areas**: What they excel at and areas for development

4. **Actionable Next Steps**: Concrete steps they can take in the next 30, 60, and 90 days

5. **Personal Career Roadmap**: A customized path forward based on their goals and constraints

Make this deeply personal, encouraging, and actionable. Use their name and reference specific details from their responses.
"""

            messages = [
                SystemMessage(content="You are a senior career counselor providing comprehensive, personalized guidance."),
                HumanMessage(content=insights_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            return {
                'insights_generated': True,
                'comprehensive_insights': response.content,
                'user_name': user_name,
                'timestamp': datetime.datetime.now().isoformat(),
                'next_action': 'career_planning'
            }
            
        except Exception as e:
            print(f"Error generating comprehensive insights: {e}")
            return {
                'insights_generated': False,
                'message': f"I'm having trouble generating your comprehensive insights right now, {user_profile.get('name', 'User')}. Let me provide some initial guidance based on what we've discussed so far.",
                'next_action': 'provide_basic_guidance'
            }

    def get_agent_info(self) -> Dict[str, Any]:
        """Return information about this agent"""
        return {
            'name': self.agent_name,
            'type': AgentType.MASTER,
            'description': 'Enhanced Master Agent - Conversational AI Assistant and Career Counselor',
            'capabilities': [
                'General AI assistance (like ChatGPT)',
                'Empathetic career counseling',
                'Assessment orchestration',
                'Personalized question generation',
                'Comprehensive career insights',
                'Ongoing support and guidance'
            ],
            'assessment_dimensions': self.assessment_dimensions
        }

    # Sync wrapper methods for Streamlit compatibility
    def process_conversation_sync(
        self, 
        user_input: str, 
        user_profile: Dict[str, Any], 
        conversation_history: List[Dict] = None
    ) -> Dict[str, Any]:
        """Synchronous wrapper with async fallback to pure sync approach"""
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Debug logging
        print(f"\n=== MASTER AGENT DEBUG [{timestamp}] ===")
        print(f"Input: '{user_input}'")
        print(f"User: {user_profile.get('name', 'Unknown')}")
        print(f"History: {len(conversation_history) if conversation_history else 0} messages")
        
        if conversation_history:
            print("Recent history:")
            for i, msg in enumerate(conversation_history[-3:]):
                print(f"  {i}: {msg.get('role', 'unknown')} - {str(msg.get('content', ''))[:50]}...")
        
        # Try the async approach first, but fall back to pure sync if there are issues
        try:
            import asyncio
            import nest_asyncio
            
            # Enable nested event loops
            nest_asyncio.apply()
            
            # Create a fresh event loop to avoid conflicts
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.process_conversation(user_input, user_profile, conversation_history)
                )
                
                response_text = result.get('response', 'No response generated')
                print(f"Response: {response_text[:150]}...")
                print(f"Action: {result.get('action_type', 'unknown')}")
                print("=== END DEBUG ===\n")
                
                return {
                    'success': True,
                    'message': response_text,
                    'action_type': result.get('action_type', 'general_response'),
                    'needs_assessment': result.get('needs_assessment', False),
                    **result
                }
            finally:
                # Always clean up the loop
                try:
                    loop.close()
                except:
                    pass
                    
        except Exception as e:
            error_msg = str(e).lower()
            print(f"ERROR in Master Agent: {e}")
            print("Falling back to synchronous response generation...")
            
            # Fall back to pure synchronous response
            try:
                sync_result = self.generate_synchronous_response(user_input, user_profile, conversation_history)
                
                response_text = sync_result.get('message', 'Hello! How can I help you today?')
                print(f"Sync Response: {response_text[:150]}...")
                print(f"Sync Action: {sync_result.get('action_type', 'unknown')}")
                print("=== END DEBUG ===\n")
                
                return sync_result
                
            except Exception as sync_error:
                print(f"ERROR in sync fallback: {sync_error}")
                print("=== END DEBUG ===\n")
                
                # Ultimate fallback - still return success but with generic message
                user_name = user_profile.get('name', 'there')
                return {
                    'success': True,
                    'message': f"Hello {user_name}! I'm your AI career counselor, here to help with any career questions or guidance you need. What would you like to explore today?",
                    'action_type': 'ultimate_fallback',
                    'needs_assessment': False
                }

    def orchestrate_assessment_flow_sync(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for orchestrate_assessment"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.orchestrate_assessment(user_profile)
            )
            return result
        except Exception as e:
            print(f"Error in sync assessment orchestration: {e}")
            return {
                'assessment_complete': False,
                'message': "I'm having trouble accessing the assessment questions right now. Let me ask you something more general - what kind of work environment makes you feel most energized?",
                'next_action': 'fallback_question'
            }

    def generate_personalized_questions_sync(
        self, 
        dimension: str, 
        user_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Synchronous wrapper for _generate_personalized_questions"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self._generate_personalized_questions(dimension, user_profile)
            )
            return result
        except Exception as e:
            print(f"Error generating personalized questions sync: {e}")
            return self._get_default_questions(dimension)

    def generate_comprehensive_insights_sync(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for generate_comprehensive_insights"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.generate_comprehensive_insights(user_profile)
            )
            return result
        except Exception as e:
            print(f"Error generating insights sync: {e}")
            return {
                'insights_generated': False,
                'message': f"I'm having trouble generating your comprehensive insights right now, {user_profile.get('name', 'User')}. Let me provide some initial guidance based on what we've discussed so far.",
                'next_action': 'provide_basic_guidance'
            }

    def generate_synchronous_response(
        self, 
        user_input: str, 
        user_profile: Dict[str, Any], 
        conversation_history: List[Dict] = None
    ) -> Dict[str, Any]:
        """Pure synchronous response generation without async dependencies"""
        
        user_name = user_profile.get('name', 'there')
        user_input_lower = user_input.lower()
        
        # Analyze conversation context
        has_assessment_data = any(
            user_profile.get(key, {}).get('assessment_complete', False)
            for key in ['interests', 'skills', 'personality', 'aspirations', 'motivations_values']
        )
        
        question_count = len([msg for msg in (conversation_history or []) if msg.get('role') == 'assistant'])
        
        # Smart response routing based on input content
        if any(word in user_input_lower for word in ["12d", "12 d", "twelve", "dimension", "assessment", "agents"]):
            return {
                'success': True,
                'message': f"Great question, {user_name}! 🎯 The 12D analysis is our comprehensive career assessment system that analyzes 12 critical dimensions of your professional identity:\n\n**🔍 The 12 Dimensions:**\n1. **Interests & Passions** - What truly motivates you\n2. **Skills & Abilities** - Your current competencies\n3. **Personality Type** - How you naturally operate\n4. **Aspirations & Goals** - Where you want to go\n5. **Motivations & Values** - What drives your decisions\n6. **Strengths & Weaknesses** - Your competitive advantages\n7. **Learning Preferences** - How you grow best\n8. **Emotional Intelligence** - Your interpersonal skills\n9. **Cognitive Abilities** - How you process information\n10. **Track Record** - Your proven achievements\n11. **Constraints & Limitations** - Your realistic boundaries\n12. **Physical & Environmental Context** - Your life circumstances\n\n**🤖 How It Works:**\nEach dimension is assessed by a specialized AI agent that asks targeted questions and analyzes your responses. Together, they create a comprehensive picture of your career potential.\n\nWould you like to start the 12D assessment to discover your ideal career path?",
                'action_type': 'assessment_explanation',
                'needs_assessment': True
            }
            
        elif any(word in user_input_lower for word in ["ai", "artificial intelligence", "machine learning", "ml", "data science", "ai engineer"]):
            return {
                'success': True,
                'message': f"Excellent choice, {user_name}! 🤖 AI and machine learning are among the most exciting and fastest-growing fields today.\n\n**🚀 Why AI/ML is Great:**\n• High demand across all industries\n• Excellent salary potential ($120K-$300K+)\n• Continuous learning and innovation\n• Solving real-world problems\n\n**💼 Career Paths:**\n• **ML Engineer** - Building and deploying models\n• **Data Scientist** - Extracting insights from data\n• **AI Researcher** - Advancing the field\n• **AI Product Manager** - Bridging tech and business\n\n**🛠️ Key Skills to Develop:**\n• Programming: Python, R, SQL\n• Math: Statistics, Linear Algebra\n• Tools: TensorFlow, PyTorch, Pandas\n• Soft Skills: Problem-solving, Communication\n\nWhat's your current background? Are you starting fresh or transitioning from another field? Would you like to start with our comprehensive assessment to create a personalized AI career roadmap?",
                'action_type': 'field_guidance',
                'needs_assessment': True
            }
            
        elif any(word in user_input_lower for word in ["hello", "hi", "hey", "start", "begin"]):
            return {
                'success': True,
                'message': f"Hello {user_name}! 👋 Welcome to your personal AI career counselor! I'm here to help you navigate your professional journey with personalized insights and guidance.\n\nI can assist you with:\n• **Career exploration** and path planning\n• **Skills assessment** and development\n• **Interview preparation** and strategies\n• **Industry insights** and trends\n• **Professional growth** planning\n\nWhat brings you here today? Are you exploring new career opportunities, planning a transition, or looking for general career guidance?",
                'action_type': 'greeting',
                'needs_assessment': False,
                'quick_start_assessment': True,
                'follow_up_questions': [
                    "🚀 Start my comprehensive career assessment now",
                    "💼 I want career guidance for a specific field",
                    "📝 Help me with interview preparation",
                    "🎯 I'm planning a career change"
                ]
            }
            
        elif any(word in user_input_lower for word in ["career", "guidance", "advice", "path", "direction"]):
            if has_assessment_data:
                return {
                    'success': True,
                    'message': f"Based on your profile, {user_name}, I can see you've made great progress with your career assessment! Let me provide some personalized insights:\n\n🎯 **Your Career Direction**: Your interests and skills suggest strong potential in areas that match your personality and aspirations.\n\n💡 **Key Recommendations**:\n• Focus on roles that align with your core strengths\n• Consider industries that match your interests\n• Develop skills that complement your natural abilities\n\nWhat specific aspect of your career path would you like to explore further? I can help you with job search strategies, skill development plans, or industry insights.",
                    'action_type': 'personalized_guidance',
                    'needs_assessment': False
                }
            else:
                return {
                    'success': True,
                    'message': f"I'd love to help you with career guidance, {user_name}! 🎯 To provide the most personalized and valuable insights, I recommend starting with our comprehensive career assessment.\n\nOur assessment covers 12 key dimensions:\n• **Interests & Passions** - What truly motivates you\n• **Skills & Abilities** - Your current strengths\n• **Personality** - How you work best\n• **Aspirations** - Your career goals and dreams\n• **Values** - What matters most to you\n\n...and 7 more important areas!\n\nThis helps me understand your unique profile and provide tailored career recommendations. Would you like to start with the assessment, or do you have specific questions I can help with right now?",
                    'action_type': 'assessment_invitation',
                    'needs_assessment': True,
                    'quick_start_assessment': True,
                    'follow_up_questions': [
                        "🚀 Yes, let's start the comprehensive assessment!",
                        "💡 Tell me more about the 12 dimensions first",
                        "🎯 I want to focus on a specific career field",
                        "📊 How long does the assessment take?"
                    ]
                }
            return {
                'success': True,
                'message': f"Excellent choice, {user_name}! 🤖 AI and machine learning are among the most exciting and fastest-growing fields today.\n\n**🚀 Why AI/ML is Great:**\n• High demand across all industries\n• Excellent salary potential ($120K-$300K+)\n• Continuous learning and innovation\n• Solving real-world problems\n\n**💼 Career Paths:**\n• **ML Engineer** - Building and deploying models\n• **Data Scientist** - Extracting insights from data\n• **AI Researcher** - Advancing the field\n• **AI Product Manager** - Bridging tech and business\n\n**🛠️ Key Skills to Develop:**\n• Programming: Python, R, SQL\n• Math: Statistics, Linear Algebra\n• Tools: TensorFlow, PyTorch, Pandas\n• Soft Skills: Problem-solving, Communication\n\nWhat's your current background? Are you starting fresh or transitioning from another field? Would you like to start with our comprehensive assessment to create a personalized AI career roadmap?",
                'action_type': 'field_guidance',
                'needs_assessment': True
            }
            
        elif any(word in user_input_lower for word in ["interview", "prep", "preparation", "job search"]):
            return {
                'success': True,
                'message': f"Great question, {user_name}! 💼 Interview preparation is crucial for career success. Here's a comprehensive approach:\n\n**🎯 Interview Preparation Strategy:**\n\n**1. Research Phase:**\n• Company background and values\n• Role requirements and expectations\n• Industry trends and challenges\n\n**2. Practice Common Questions:**\n• \"Tell me about yourself\"\n• \"Why are you interested in this role?\"\n• \"What are your strengths/weaknesses?\"\n\n**3. Behavioral Questions (STAR Method):**\n• Situation, Task, Action, Result\n• Prepare 5-7 strong examples\n\n**4. Technical Preparation:**\n• Review relevant skills and concepts\n• Practice coding/technical problems if applicable\n\n**5. Questions to Ask:**\n• Team dynamics and culture\n• Growth opportunities\n• Challenges facing the role\n\nWhat type of role are you preparing for? I can provide more specific guidance!",
                'action_type': 'interview_guidance',
                'needs_assessment': False
            }
            
        elif question_count >= 3 and not has_assessment_data:
            return {
                'success': True,
                'message': f"I really enjoy our conversation, {user_name}! 😊 Based on our discussion, I think you'd benefit greatly from our comprehensive 12-dimensional career assessment.\n\nThe assessment will help us:\n• **Identify** your unique strengths and interests\n• **Explore** career paths that truly fit you\n• **Create** a personalized development plan\n• **Uncover** opportunities you might not have considered\n\nIt's designed to be engaging and insightful, not just another quiz! Each dimension reveals important aspects of your professional identity.\n\nReady to discover your ideal career path? Let's start with the assessment! 🚀",
                'action_type': 'assessment_transition',
                'needs_assessment': True
            }
            
        else:
            # General conversational response
            return {
                'success': True,
                'message': f"That's an interesting point, {user_name}! I appreciate you sharing that with me. As your AI career counselor, I'm here to help you explore any career-related questions or challenges you might have.\n\nIs there a particular aspect of your professional journey you'd like to discuss? Whether it's exploring new opportunities, developing skills, planning a career change, or preparing for interviews - I'm here to support you! 🌟",
                'action_type': 'general_response',
                'needs_assessment': False
            }
