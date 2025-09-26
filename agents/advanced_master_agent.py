"""
Advanced Master Agent - Remiro AI Career Assistant

This is the central orchestrator that:
1. Manages the 12D career assessment process
2. Provides ChatGPT-like responses for general queries 
3. Generates comprehensive career roadmaps and insights
4. Maintains empathetic, conversational interactions
"""

import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import importlib
import sys
from pathlib import Path

# Import enhanced agents
from agents.enhanced_interests import InterestsAgent
from agents.enhanced_skills import SkillsAgent
from agents.enhanced_personality import PersonalityAgent
from agents.enhanced_aspirations import AspirationsAgent

# Import remaining agents from the collection file
sys.path.append(str(Path(__file__).parent))
from enhanced_remaining_agents import (
    MotivationsValuesAgent, CognitiveAbilitiesAgent, StrengthsWeaknessesAgent,
    LearningPreferencesAgent, TrackRecordAgent, EmotionalIntelligenceAgent,
    ConstraintsAgent, PhysicalContextAgent
)

class AdvancedMasterAgent:
    """🎛️ Advanced Master Agent - AI Career Assistant & 12D Assessment Orchestrator"""
    
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Remiro AI Career Assistant"
        self.conversation_history = []
        self.user_profile = {}
        self.current_assessment_agent = None
        self.assessment_progress = {}
        self.assessment_complete = False
        self.session_start = datetime.now()
        
        # Conversation state tracking
        self.conversation_state = "welcome"  # welcome -> casual_chat -> assessment_flow -> completed
        self.casual_exchanges = 0
        self.is_first_interaction = True
        
        # Initialize all 12D agents
        self.agents = {
            'interests': InterestsAgent(llm),
            'skills': SkillsAgent(llm),
            'personality': PersonalityAgent(llm),
            'aspirations': AspirationsAgent(llm),
            'motivations_values': MotivationsValuesAgent(llm),
            'cognitive_abilities': CognitiveAbilitiesAgent(llm),
            'strengths_weaknesses': StrengthsWeaknessesAgent(llm),
            'learning_preferences': LearningPreferencesAgent(llm),
            'track_record': TrackRecordAgent(llm),
            'emotional_intelligence': EmotionalIntelligenceAgent(llm),
            'constraints': ConstraintsAgent(llm),
            'physical_context': PhysicalContextAgent(llm)
        }
        
        # Assessment flow order
        self.assessment_order = [
            'interests', 'skills', 'personality', 'aspirations',
            'motivations_values', 'cognitive_abilities', 'strengths_weaknesses',
            'learning_preferences', 'track_record', 'emotional_intelligence',
            'constraints', 'physical_context'
        ]
        
        # Initialize progress tracking
        for agent_type in self.assessment_order:
            self.assessment_progress[agent_type] = {
                'started': False,
                'completed': False,
                'responses': [],
                'analysis': None
            }
    
    def detect_intent(self, user_input: str) -> str:
        """Detect user intent to determine response strategy"""
        
        user_lower = user_input.lower()
        
        # Assessment-related intents
        assessment_keywords = [
            'assessment', '12d', 'career test', 'evaluate', 'analyze',
            'start assessment', 'begin', 'questions', 'career guidance'
        ]
        
        # General conversation intents
        general_keywords = [
            'hello', 'hi', 'how are you', 'what can you do', 'help',
            'explain', 'tell me about', 'what is', 'how do'
        ]
        
        # Career advice intents
        career_keywords = [
            'career advice', 'job search', 'resume', 'interview', 'skills',
            'industry', 'salary', 'growth', 'promotion', 'change career'
        ]
        
        if any(keyword in user_lower for keyword in assessment_keywords):
            return "assessment_related"
        elif any(keyword in user_lower for keyword in career_keywords):
            return "career_advice"
        elif any(keyword in user_lower for keyword in general_keywords):
            return "general_conversation"
        else:
            # If in assessment, continue assessment
            if self.current_assessment_agent:
                return "assessment_response"
            else:
                return "general_conversation"
    
    def generate_chatgpt_response(self, user_input: str, intent: str) -> Dict[str, Any]:
        """Generate ChatGPT-style response for general queries"""
        
        try:
            if intent == "general_conversation":
                prompt = f"""
                You are Remiro AI, an advanced career assistant. Respond naturally and helpfully to this query:
                
                User: {user_input}
                
                Guidelines:
                - Be conversational, helpful, and professional
                - If career-related, offer relevant insights
                - If they seem interested, mention your 12D career assessment capability
                - Keep responses concise but informative
                - Don't hallucinate - stick to general knowledge
                """
            
            elif intent == "career_advice":
                prompt = f"""
                You are Remiro AI, a career specialist. Provide helpful career advice for:
                
                User Question: {user_input}
                
                Guidelines:
                - Give practical, actionable advice
                - Be empathetic and supportive
                - Mention how your 12D assessment could provide personalized insights
                - Don't make specific company or salary promises
                - Focus on general best practices and strategies
                """
            
            else:  # assessment_related
                return self.handle_assessment_request(user_input)
            
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            
            return {
                "type": "general_response",
                "message": response.content,
                "intent": intent,
                "suggestions": self._get_conversation_suggestions(intent)
            }
            
        except Exception as e:
            return {
                "type": "error_response", 
                "message": "I'm here to help with your career questions. What would you like to know?",
                "error": str(e)
            }
    
    def handle_assessment_request(self, user_input: str) -> Dict[str, Any]:
        """Handle assessment-related requests"""
        
        if not any(self.assessment_progress[agent]['started'] for agent in self.assessment_order):
            # Start first assessment
            return self.start_assessment()
        else:
            # Continue current assessment or move to next
            return self.continue_assessment(user_input)
    
    def start_assessment(self) -> Dict[str, Any]:
        """Start the 12D career assessment"""
        
        first_agent_type = self.assessment_order[0]
        self.current_assessment_agent = first_agent_type
        self.assessment_progress[first_agent_type]['started'] = True
        
        agent = self.agents[first_agent_type]
        questions = agent.get_predefined_questions()
        first_question = questions[0]
        
        intro_message = f"""
        Welcome to your personalized 12D Career Assessment! 🎯
        
        I'm going to help you discover your ideal career path through a comprehensive analysis of 12 key dimensions. This will be a conversational process where I get to know you better.
        
        Let's start with exploring your interests. {first_question['question']}
        """
        
        return {
            "type": "assessment_question",
            "message": intro_message,
            "current_agent": first_agent_type,
            "question_index": 0,
            "progress": f"1/12 - {agent.agent_name}"
        }
    
    def continue_assessment(self, user_input: str) -> Dict[str, Any]:
        """Continue the current assessment or move to next agent"""
        
        if not self.current_assessment_agent:
            return self.start_assessment()
        
        # Process response with current agent
        agent = self.agents[self.current_assessment_agent]
        current_progress = self.assessment_progress[self.current_assessment_agent]
        
        # Determine current question index
        question_index = len(current_progress['responses'])
        
        # Process the response
        result = agent.process_response(user_input, question_index)
        
        # Store response
        current_progress['responses'].append(user_input)
        
        if result['type'] == 'assessment_complete':
            # Current agent assessment complete
            current_progress['completed'] = True
            current_progress['analysis'] = result['analysis']
            
            return self.move_to_next_agent()
        
        else:
            # Continue with current agent
            agent_index = self.assessment_order.index(self.current_assessment_agent)
            progress_text = f"{agent_index + 1}/12 - {agent.agent_name}"
            
            return {
                "type": "assessment_question",
                "message": result['question'],
                "current_agent": self.current_assessment_agent,
                "question_index": result.get('question_index', question_index),
                "progress": progress_text
            }
    
    def move_to_next_agent(self) -> Dict[str, Any]:
        """Move to the next agent in the assessment flow"""
        
        current_index = self.assessment_order.index(self.current_assessment_agent)
        
        if current_index + 1 >= len(self.assessment_order):
            # All assessments complete!
            return self.complete_full_assessment()
        
        # Move to next agent
        next_agent_type = self.assessment_order[current_index + 1]
        self.current_assessment_agent = next_agent_type
        self.assessment_progress[next_agent_type]['started'] = True
        
        agent = self.agents[next_agent_type]
        questions = agent.get_predefined_questions()
        first_question = questions[0]
        
        progress_text = f"{current_index + 2}/12 - {agent.agent_name}"
        
        transition_message = f"""
        Excellent! Now let's explore {agent.core_domain}.
        
        {first_question['question']}
        """
        
        return {
            "type": "assessment_question",
            "message": transition_message,
            "current_agent": next_agent_type,
            "question_index": 0,
            "progress": progress_text
        }
    
    def complete_full_assessment(self) -> Dict[str, Any]:
        """Complete the full 12D assessment and generate comprehensive analysis"""
        
        self.assessment_complete = True
        
        try:
            # Generate comprehensive career analysis
            career_analysis = self.generate_comprehensive_analysis()
            
            completion_message = f"""
            🎉 Congratulations! Your 12D Career Assessment is complete!
            
            I've analyzed your responses across all 12 dimensions and generated a comprehensive career profile for you. This includes:
            
            ✅ **Your Ideal Role Matches** - Perfect career fits based on your profile
            ✅ **Personalized Skill Development Plan** - Skills to learn and improve  
            ✅ **Career Roadmap** - Step-by-step path to your dream role
            ✅ **Industry Insights** - Best sectors and companies for you
            
            {career_analysis['summary']}
            
            Would you like me to dive deeper into any specific area, or do you have other career questions?
            """
            
            return {
                "type": "assessment_complete",
                "message": completion_message,
                "analysis": career_analysis,
                "completion_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "type": "assessment_complete",
                "message": "Your assessment is complete! Let me know what career guidance you'd like to explore.",
                "error": str(e)
            }
    
    def generate_comprehensive_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive career analysis from all 12D assessments"""
        
        try:
            # Collect all analyses
            all_analyses = {}
            for agent_type, progress in self.assessment_progress.items():
                if progress['completed'] and progress['analysis']:
                    all_analyses[agent_type] = progress['analysis']
            
            # Generate comprehensive analysis using AI
            analysis_prompt = f"""
            As an expert career counselor, create a comprehensive career analysis based on this 12D assessment data:
            
            Assessment Results:
            {json.dumps(all_analyses, indent=2)}
            
            Generate a detailed career analysis with:
            1. **Role Recommendations**: 5 specific job roles that perfectly match their profile
            2. **Skill Development Plan**: Key skills they should learn/improve with priority order
            3. **Career Roadmap**: 6-month, 1-year, and 3-year career goals with specific steps
            4. **Industry Match**: Best industries and company types for them
            5. **Growth Strategy**: How they can advance and evolve their career
            
            Provide as JSON:
            {{
                "role_recommendations": [
                    {{"title": "Role Title", "match_score": 95, "reasons": ["why it fits"], "companies": ["example companies"]}},
                    ...
                ],
                "skill_development_plan": [
                    {{"skill": "Skill Name", "priority": "high/medium/low", "timeline": "timeframe", "resources": ["learning resources"]}},
                    ...
                ],
                "career_roadmap": {{
                    "6_months": [["specific goals and steps"]],
                    "1_year": [["specific goals and steps"]],
                    "3_years": [["specific goals and steps"]]
                }},
                "industry_insights": {{
                    "best_industries": ["industry names"],
                    "company_types": ["startup", "enterprise", etc],
                    "growth_sectors": ["emerging areas"]
                }},
                "summary": "2-3 sentence overview of their career profile and potential"
            }}
            """
            
            response = self.llm.invoke([{"role": "user", "content": analysis_prompt}])
            
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                return self._create_fallback_analysis()
                
        except Exception as e:
            print(f"Error generating analysis: {e}")
            return self._create_fallback_analysis()
    
    def _create_fallback_analysis(self) -> Dict[str, Any]:
        """Create fallback analysis if AI analysis fails"""
        return {
            "role_recommendations": [
                {"title": "Career Specialist", "match_score": 90, "reasons": ["Strong assessment completion"], "companies": ["Various"]}
            ],
            "skill_development_plan": [
                {"skill": "Leadership", "priority": "high", "timeline": "6 months", "resources": ["Online courses"]}
            ],
            "career_roadmap": {
                "6_months": ["Complete skill development", "Build portfolio"],
                "1_year": ["Apply for target roles", "Network actively"],
                "3_years": ["Achieve leadership position", "Mentor others"]
            },
            "industry_insights": {
                "best_industries": ["Technology", "Consulting"],
                "company_types": ["Mid-size", "Growth-oriented"],
                "growth_sectors": ["AI", "Digital Transformation"]
            },
            "summary": "You have a strong professional profile with excellent potential for career growth across multiple industries."
        }
    
    def _get_conversation_suggestions(self, intent: str) -> List[str]:
        """Get conversation suggestions based on intent"""
        
        if intent == "assessment_related":
            return [
                "Start my 12D career assessment",
                "Tell me about the assessment process",
                "What will I learn from this assessment?"
            ]
        elif intent == "career_advice":
            return [
                "How can I improve my resume?",
                "What skills should I develop?",
                "Help me plan my career path"
            ]
        else:
            return [
                "Start my career assessment",
                "Give me career advice",
                "Help me with job search"
            ]
    
    def process_conversation(self, user_input: str, user_id: str = "default") -> Dict[str, Any]:
        """Main conversation processing method with natural flow"""
        
        # Store conversation history
        self.conversation_history.append({
            "user": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        response = None
        
        # Natural conversation flow based on state
        if self.conversation_state == "welcome":
            response = self.handle_welcome_interaction(user_input)
        elif self.conversation_state == "casual_chat":
            response = self.handle_casual_chat(user_input)
        elif self.conversation_state == "assessment_flow":
            response = self.handle_assessment_flow(user_input)
        elif self.conversation_state == "completed":
            response = self.handle_post_assessment_chat(user_input)
        
        # Store assistant response
        if response:
            self.conversation_history.append({
                "assistant": response.get("message", ""),
                "timestamp": datetime.now().isoformat()
            })
        
        return response or {"type": "error", "message": "Something went wrong. Let's continue our chat!"}
    
    def handle_welcome_interaction(self, user_input: str) -> Dict[str, Any]:
        """Handle the initial welcome and transition to casual chat"""
        
        if self.is_first_interaction:
            self.is_first_interaction = False
            self.conversation_state = "casual_chat"
            
            welcome_message = f"""Hey there! 👋 I'm Remiro, your friendly career companion! 

It's great to meet you! I'm here to have a nice chat and help you explore some exciting career possibilities. 

So, tell me - what kind of things do you love doing in your free time? What are your hobbies or interests that really get you excited? 🎯"""
            
            return {
                "type": "casual_conversation",
                "message": welcome_message,
                "state": "casual_chat"
            }
        else:
            # If they respond again in welcome state, move to casual
            self.conversation_state = "casual_chat"
            return self.handle_casual_chat(user_input)
    
    def handle_casual_chat(self, user_input: str) -> Dict[str, Any]:
        """Handle casual conversation before transitioning to assessment"""
        
        self.casual_exchanges += 1
        
        if self.casual_exchanges <= 2:
            # First few casual exchanges - focus on hobbies and interests
            response = self.generate_casual_response(user_input)
            
            return {
                "type": "casual_conversation", 
                "message": response,
                "state": "casual_chat"
            }
        else:
            # After 2-3 exchanges, naturally transition to assessment
            return self.transition_to_assessment(user_input)
    
    def generate_casual_response(self, user_input: str) -> str:
        """Generate casual, friendly responses about hobbies and interests"""
        
        prompt = f"""
        You are Remiro, a friendly and casual career companion. You're having a natural conversation with someone about their interests and hobbies.

        User just said: "{user_input}"

        Respond in a friendly, enthusiastic way and:
        1. Show genuine interest in what they shared
        2. Ask a follow-up question to learn more about them
        3. Keep it casual and conversational
        4. Make them feel comfortable
        5. Don't mention "assessment" or formal career evaluation yet

        Example topics to explore:
        - Their hobbies and what they enjoy about them
        - Things they're naturally good at
        - What energizes them or makes them lose track of time
        - Activities they'd do even if not paid

        Keep response warm, genuine, and under 3 sentences.
        """
        
        try:
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            return response.content
        except:
            return "That sounds really interesting! Tell me more about what you enjoy most about that. What is it that draws you to it? 😊"
    
    def transition_to_assessment(self, user_input: str) -> Dict[str, Any]:
        """Naturally transition from casual chat to assessment"""
        
        # Generate a response that acknowledges their input and smoothly transitions
        transition_prompt = f"""
        You are Remiro, transitioning from casual chat to deeper career exploration. 

        User just said: "{user_input}"

        Create a warm transition response that:
        1. Acknowledges what they shared
        2. Naturally suggests diving deeper into understanding them better
        3. Makes it sound like a natural continuation of the conversation
        4. Don't use words like "assessment" or "test" - make it sound like getting to know them better
        5. Keep it enthusiastic and friendly

        End with a question that feels like a natural next step in conversation.
        """
        
        try:
            response = self.llm.invoke([{"role": "user", "content": transition_prompt}])
            transition_message = response.content
        except:
            transition_message = f"Wow, I'm really getting a sense of who you are! You know what, I'd love to understand you even better. Mind if I ask you a few more questions to really get to know what makes you tick?"
        
        # Start the assessment flow
        self.conversation_state = "assessment_flow"
        self.start_natural_assessment()
        
        return {
            "type": "assessment_transition",
            "message": transition_message,
            "state": "assessment_flow"
        }
    
    def start_natural_assessment(self):
        """Start assessment without explicitly mentioning it"""
        first_agent_type = self.assessment_order[0]
        self.current_assessment_agent = first_agent_type
        self.assessment_progress[first_agent_type]['started'] = True
    
    def handle_assessment_flow(self, user_input: str) -> Dict[str, Any]:
        """Handle the assessment flow naturally"""
        
        if not self.current_assessment_agent:
            self.start_natural_assessment()
        
        # Process response with current agent
        agent = self.agents[self.current_assessment_agent]
        current_progress = self.assessment_progress[self.current_assessment_agent]
        
        # Store response
        current_progress['responses'].append(user_input)
        
        # Generate personalized follow-up question based on their response
        question_response = self.generate_personalized_question(user_input, agent)
        
        if self.is_agent_complete(agent):
            current_progress['completed'] = True
            return self.move_to_next_agent_naturally()
        
        return {
            "type": "natural_question",
            "message": question_response,
            "state": "assessment_flow"
        }
    
    def generate_personalized_question(self, user_response: str, agent) -> str:
        """Generate personalized follow-up questions based on user responses"""
        
        # Get context from previous responses in this agent
        current_progress = self.assessment_progress[self.current_assessment_agent]
        previous_responses = current_progress['responses']
        
        # Get predefined questions for context
        predefined_questions = agent.get_predefined_questions()
        current_question_index = len(previous_responses) - 1
        
        prompt = f"""
        You are Remiro, having a natural conversation to understand this person better.

        Current focus area: {agent.agent_name.replace('Agent', '').replace('_', ' ').title()}
        
        User just responded: "{user_response}"
        
        Previous conversation in this area: {previous_responses[:-1] if len(previous_responses) > 1 else "None"}
        
        Available question themes for this area: {[q.get('question', '') for q in predefined_questions[:3]]}

        Generate a natural, conversational follow-up question that:
        1. Shows you heard and understood their response
        2. Builds on what they shared to go deeper
        3. Feels like a natural progression of the conversation
        4. Explores the {agent.agent_name.replace('Agent', '').replace('_', ' ').lower()} aspect without being too obvious
        5. Uses casual, friendly language
        6. Makes them feel comfortable sharing more

        Keep it conversational and under 2 sentences.
        """
        
        try:
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            return response.content
        except:
            # Fallback to predefined question
            if current_question_index < len(predefined_questions):
                return predefined_questions[current_question_index]['question']
            return "That's really insightful! What else would you like to share about this?"
    
    def is_agent_complete(self, agent) -> bool:
        """Check if current agent has gathered enough information"""
        current_progress = self.assessment_progress[self.current_assessment_agent]
        responses_count = len(current_progress['responses'])
        
        # Consider agent complete after 3-4 meaningful exchanges
        return responses_count >= 3
    
    def move_to_next_agent_naturally(self) -> Dict[str, Any]:
        """Move to next agent with natural transition"""
        
        current_index = self.assessment_order.index(self.current_assessment_agent)
        
        if current_index + 1 >= len(self.assessment_order):
            # Assessment complete
            self.conversation_state = "completed"
            self.assessment_complete = True
            return self.generate_final_analysis()
        
        # Move to next agent
        next_agent_type = self.assessment_order[current_index + 1]
        self.current_assessment_agent = next_agent_type
        self.assessment_progress[next_agent_type]['started'] = True
        
        # Generate natural transition
        next_agent = self.agents[next_agent_type]
        
        transition_message = f"You know, I'm getting such a great picture of who you are! Let me ask you about something else that's on my mind..."
        
        # Get first question from next agent
        first_question = self.generate_personalized_question("", next_agent)
        
        full_message = f"{transition_message}\n\n{first_question}"
        
        return {
            "type": "natural_question",
            "message": full_message,
            "state": "assessment_flow"
        }
    
    def handle_post_assessment_chat(self, user_input: str) -> Dict[str, Any]:
        """Handle conversation after assessment is complete"""
        
        # Generate general career advice or answer questions
        prompt = f"""
        You are Remiro, having completed an in-depth conversation with this person about their career interests.
        
        User now asks: "{user_input}"
        
        Based on your conversation, provide helpful, personalized career advice.
        Be supportive, encouraging, and offer practical next steps.
        """
        
        try:
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            return {
                "type": "post_assessment_advice",
                "message": response.content,
                "state": "completed"
            }
        except:
            return {
                "type": "post_assessment_advice", 
                "message": "I'd be happy to help you explore this further! What specific aspect would you like to dive into?",
                "state": "completed"
            }
    
    def generate_final_analysis(self) -> Dict[str, Any]:
        """Generate final comprehensive analysis when assessment is complete"""
        
        try:
            # Collect all responses and context
            all_responses = {}
            for agent_type, progress in self.assessment_progress.items():
                if progress['responses']:
                    all_responses[agent_type] = progress['responses']
            
            # Generate comprehensive analysis
            analysis_prompt = f"""
            You are Remiro, wrapping up a natural, friendly conversation where you've gotten to know this person deeply across 12 different areas of their career profile.
            
            Here's what you learned about them:
            {json.dumps(all_responses, indent=2)}
            
            Now create a warm, comprehensive career summary that feels like advice from a wise friend who really gets them.
            
            Include:
            1. A warm, personal summary of who they are professionally
            2. 3-4 ideal career paths that fit them perfectly
            3. Key strengths they should leverage
            4. 2-3 skills worth developing
            5. Practical next steps they can take
            
            Write it in a conversational, encouraging tone - like you're wrapping up a great coffee chat about their future.
            Keep it inspiring and actionable!
            """
            
            response = self.llm.invoke([{"role": "user", "content": analysis_prompt}])
            
            return {
                "type": "final_analysis",
                "message": response.content,
                "state": "completed",
                "analysis_complete": True
            }
            
        except Exception as e:
            return {
                "type": "final_analysis",
                "message": "Wow, what an amazing conversation! I've learned so much about you and I'm really excited about your career potential. You have such a unique combination of interests, skills, and aspirations. Let me know what specific area you'd like to explore further - I'm here to help you take the next steps!",
                "state": "completed",
                "analysis_complete": True,
                "error": str(e)
            }