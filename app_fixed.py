"""
Enhanced Remiro AI - Personalized Career Counseling System
A comprehensive 12-dimensional career assessment and planning platform
Now featuring conversational Master Agent interface
"""

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
import time
import random
import os
from pathlib import Path

# Core imports
from core.user_manager import UserManager

# Import the new Enhanced Master Agent
from agents.master_agent import EnhancedMasterAgent

# Tool imports
try:
    from tools.resume_builder import ResumeBuilder
    from tools.mock_interview import MockInterviewAI
    from tools.job_matcher_analyzer import JobMatcherSkillAnalyzer
    from tools.linkedin_enhancer import LinkedInEnhancer
    from tools.application_tracker import ApplicationTracker
except ImportError as e:
    st.error(f"Failed to import career tools: {e}")
    # Define placeholder classes
    class ResumeBuilder:
        def __init__(self, llm): pass
        def display_resume_builder(self, profile): st.info("Resume Builder tool loading...")
    
    class MockInterviewAI:
        def __init__(self, llm): pass  
        def display_mock_interview(self, profile): st.info("Mock Interview AI tool loading...")
    
    class JobMatcherSkillAnalyzer:
        def __init__(self, llm): pass
        def display_job_matcher_analyzer(self, profile): st.info("Job Matcher tool loading...")
    
    class LinkedInEnhancer:
        def __init__(self, llm): pass
        def display_linkedin_enhancer(self, profile): st.info("LinkedIn Enhancer tool loading...")
        
    class ApplicationTracker:
        def __init__(self, llm): pass
        def display_application_tracker(self, profile): st.info("Application Tracker tool loading...")

# LLM Configuration
from langchain_google_genai import ChatGoogleGenerativeAI

@st.cache_resource
def get_llm():
    """Initialize and cache the LLM"""
    # Try to get API key from multiple sources
    api_key = (
        os.getenv("GOOGLE_API_KEY") or 
        os.environ.get("GOOGLE_API_KEY") or
        st.secrets.get("GOOGLE_API_KEY", None)
    )
    
    # Clean up potential quotes from the API key
    if api_key:
        api_key = api_key.strip().strip('"').strip("'")
    
    # Debug: show what we found (mask the key for security)
    if api_key and len(api_key) > 10:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "Found"
        st.success(f"✅ Google API Key loaded: {masked_key}")
    else:
        st.error("⚠️ Please set your GOOGLE_API_KEY environment variable")
        st.info("You can get a free API key from: https://makersuite.google.com/app/apikey")
        
        # Show current environment for debugging
        st.write("**Environment Check:**")
        st.write(f"- Working Directory: {os.getcwd()}")
        st.write(f"- .env file exists: {Path('.env').exists()}")
        
        # Try to read .env file directly
        if Path('.env').exists():
            try:
                with open('.env', 'r') as f:
                    env_content = f.read()
                    if 'GOOGLE_API_KEY' in env_content:
                        st.info("✅ GOOGLE_API_KEY found in .env file")
                        # Show a few characters to debug
                        lines = env_content.split('\n')
                        for line in lines:
                            if line.startswith('GOOGLE_API_KEY'):
                                st.code(f"Found: {line[:20]}...")
                    else:
                        st.warning("❌ GOOGLE_API_KEY not found in .env file")
            except Exception as e:
                st.error(f"Error reading .env file: {e}")
        
        st.stop()
    
    try:
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Using the latest Gemini 2.0 Flash experimental model
            google_api_key=api_key,
            temperature=0.7,
            max_retries=3,
            request_timeout=60
        )
    except Exception as e:
        st.error(f"Error initializing Google Gemini: {str(e)}")
        st.info("Please check your API key is valid and has access to Gemini models")
        st.stop()

# Enhanced Agent Classes with Multiple Choice Questions
class EnhancedAgent:
    """Enhanced base agent with multiple choice questions and checkbox selections"""
    
    def __init__(self, llm, agent_name: str, assessment_type: str):
        self.llm = llm
        self.agent_name = agent_name
        self.assessment_type = assessment_type
        self.question_index = 0
        self.user_responses = []
        self.questions_data = self._get_questions_for_type()
    
    def _get_questions_for_type(self):
        """Get structured questions for each assessment type"""
        questions_map = {
            "personality": {
                "intro": "Let's explore your natural work style and personality preferences.",
                "questions": [
                    {
                        "question": "How do you prefer to work on projects?",
                        "options": [
                            "Leading and directing a team",
                            "Collaborating closely with others",
                            "Working independently with minimal supervision",
                            "Switching between team and solo work",
                            "Contributing as a supportive team member"
                        ]
                    },
                    {
                        "question": "What energizes you most at work?",
                        "options": [
                            "Solving complex problems",
                            "Building relationships with people",
                            "Creating new ideas and innovations",
                            "Helping others succeed",
                            "Achieving measurable goals",
                            "Learning new skills and knowledge"
                        ]
                    },
                    {
                        "question": "How do you handle workplace stress?",
                        "options": [
                            "Take charge and create solutions",
                            "Seek support from colleagues",
                            "Take time to reflect and plan",
                            "Focus on what I can control",
                            "Use humor to lighten the mood",
                            "Break tasks into smaller steps"
                        ]
                    }
                ]
            },
            "interests": {
                "intro": "Let's discover what truly captivates and motivates you.",
                "questions": [
                    {
                        "question": "Which activities make you lose track of time?",
                        "options": [
                            "Analyzing data and finding patterns",
                            "Creating or designing something new",
                            "Helping people solve problems",
                            "Learning about new technologies",
                            "Building or fixing things",
                            "Teaching or mentoring others",
                            "Planning and organizing events"
                        ]
                    },
                    {
                        "question": "What topics do you find most fascinating?",
                        "options": [
                            "Science and technology",
                            "Arts and creative expression",
                            "Business and entrepreneurship",
                            "Health and wellness",
                            "Environmental sustainability",
                            "Social issues and advocacy",
                            "History and culture",
                            "Psychology and human behavior"
                        ]
                    },
                    {
                        "question": "In your free time, you're most likely to:",
                        "options": [
                            "Read articles or watch documentaries",
                            "Work on creative projects",
                            "Volunteer for causes you care about",
                            "Exercise or play sports",
                            "Spend time with friends and family",
                            "Learn new skills online",
                            "Travel and explore new places"
                        ]
                    }
                ]
            },
            "aspirations": {
                "intro": "Let's explore your career dreams and future vision.",
                "questions": [
                    {
                        "question": "What kind of impact do you want to make in your career?",
                        "options": [
                            "Create innovative solutions to global problems",
                            "Help individuals improve their lives",
                            "Build successful businesses or organizations",
                            "Advance knowledge in your field",
                            "Inspire and lead others",
                            "Make a positive environmental impact",
                            "Preserve and share cultural knowledge"
                        ]
                    },
                    {
                        "question": "What does career success look like to you?",
                        "options": [
                            "Financial security and wealth",
                            "Recognition and respect from peers",
                            "Work-life balance and flexibility",
                            "Continuous learning and growth",
                            "Making a meaningful difference",
                            "Having creative freedom",
                            "Building lasting relationships",
                            "Achieving specific professional goals"
                        ]
                    },
                    {
                        "question": "In 10 years, you'd like to be known for:",
                        "options": [
                            "Expertise in your specialized field",
                            "Leadership and vision",
                            "Innovation and creativity",
                            "Helping others succeed",
                            "Building something significant",
                            "Making positive social change",
                            "Achieving work-life integration"
                        ]
                    }
                ]
            },
            "skills": {
                "intro": "Let's identify your superpowers and key capabilities.",
                "questions": [
                    {
                        "question": "Which skills do others often come to you for help with?",
                        "options": [
                            "Problem-solving and analysis",
                            "Communication and presentation",
                            "Project management and organization",
                            "Creative design and innovation",
                            "Technical skills and troubleshooting",
                            "Teaching and mentoring",
                            "Negotiation and persuasion",
                            "Research and information gathering"
                        ]
                    },
                    {
                        "question": "What types of tasks do you complete most confidently?",
                        "options": [
                            "Complex analytical work",
                            "Creative and artistic projects",
                            "People management and team coordination",
                            "Technical implementation and coding",
                            "Writing and content creation",
                            "Sales and business development",
                            "Planning and strategic thinking",
                            "Hands-on building and crafting"
                        ]
                    },
                    {
                        "question": "Which achievements are you most proud of?",
                        "options": [
                            "Solving difficult technical problems",
                            "Leading successful team projects",
                            "Creating something original",
                            "Improving processes or systems",
                            "Helping others learn and grow",
                            "Building strong relationships",
                            "Achieving challenging goals",
                            "Making positive changes in my community"
                        ]
                    }
                ]
            },
            "motivations_values": {
                "intro": "Let's discover what drives you and what values are most important to you.",
                "questions": [
                    {
                        "question": "What aspects of work give you the most satisfaction?",
                        "options": [
                            "Solving challenging problems",
                            "Helping others succeed",
                            "Creating something new",
                            "Achieving measurable results",
                            "Learning and growing",
                            "Working with great people",
                            "Making a positive impact",
                            "Having autonomy and flexibility"
                        ]
                    },
                    {
                        "question": "Which values are most important to you in your career?",
                        "options": [
                            "Integrity and honesty",
                            "Innovation and creativity",
                            "Collaboration and teamwork",
                            "Excellence and quality",
                            "Service to others",
                            "Personal growth",
                            "Work-life balance",
                            "Financial security",
                            "Recognition and achievement"
                        ]
                    },
                    {
                        "question": "What motivates you to do your best work?",
                        "options": [
                            "Personal satisfaction and pride",
                            "Recognition from others",
                            "Financial rewards",
                            "Making a difference",
                            "Learning new things",
                            "Competition and challenges",
                            "Helping my team succeed",
                            "Building something lasting"
                        ]
                    }
                ]
            },
            "cognitive_abilities": {
                "intro": "Let's explore how you think and solve problems.",
                "questions": [
                    {
                        "question": "When facing a complex problem, you typically:",
                        "options": [
                            "Break it down into smaller parts",
                            "Look for patterns and connections",
                            "Brainstorm multiple solutions",
                            "Research and gather information",
                            "Discuss it with others",
                            "Take time to think it through",
                            "Jump in and start experimenting"
                        ]
                    },
                    {
                        "question": "How do you prefer to process information?",
                        "options": [
                            "Visual diagrams and charts",
                            "Written documentation",
                            "Verbal discussions",
                            "Hands-on experimentation",
                            "Step-by-step procedures",
                            "Big picture concepts first",
                            "Real-world examples"
                        ]
                    },
                    {
                        "question": "What types of thinking come naturally to you?",
                        "options": [
                            "Logical and analytical thinking",
                            "Creative and innovative thinking",
                            "Strategic and long-term planning",
                            "Detail-oriented and systematic",
                            "Intuitive and gut-feeling based",
                            "Critical evaluation and questioning",
                            "Holistic and systems thinking"
                        ]
                    }
                ]
            },
            "learning_preferences": {
                "intro": "Let's understand how you learn and process information best.",
                "questions": [
                    {
                        "question": "How do you prefer to learn new skills?",
                        "options": [
                            "Hands-on practice and experimentation",
                            "Reading books and articles",
                            "Watching videos and demonstrations",
                            "Taking structured courses",
                            "Learning from a mentor",
                            "Group discussions and collaboration",
                            "Trial and error approach"
                        ]
                    },
                    {
                        "question": "What learning environment works best for you?",
                        "options": [
                            "Quiet space for focused study",
                            "Interactive group settings",
                            "Real-world work environments",
                            "Online and flexible timing",
                            "Structured classroom setting",
                            "One-on-one mentoring",
                            "Conference and workshop settings"
                        ]
                    },
                    {
                        "question": "How do you retain information best?",
                        "options": [
                            "Taking detailed notes",
                            "Creating visual mind maps",
                            "Teaching others what I learned",
                            "Practicing immediately",
                            "Connecting to existing knowledge",
                            "Regular review and repetition",
                            "Real-world application"
                        ]
                    }
                ]
            },
            "physical_context": {
                "intro": "Let's explore your ideal work environment and conditions.",
                "questions": [
                    {
                        "question": "What work environment helps you do your best work?",
                        "options": [
                            "Quiet, private office space",
                            "Open, collaborative workspace",
                            "Home office with flexibility",
                            "Outdoor or natural settings",
                            "High-energy, fast-paced environment",
                            "Calm, organized space",
                            "Varied locations and travel"
                        ]
                    },
                    {
                        "question": "What work schedule do you prefer?",
                        "options": [
                            "Traditional 9-5 schedule",
                            "Flexible hours with core times",
                            "Early morning start",
                            "Evening/night shift",
                            "Compressed work week",
                            "Project-based timing",
                            "Completely flexible schedule"
                        ]
                    },
                    {
                        "question": "What physical aspects are important for your productivity?",
                        "options": [
                            "Natural lighting and windows",
                            "Comfortable seating and ergonomics",
                            "Quiet environment with minimal distractions",
                            "Access to technology and tools",
                            "Space for movement and activity",
                            "Temperature control",
                            "Proximity to colleagues",
                            "Access to food and refreshments"
                        ]
                    }
                ]
            },
            "strengths_weaknesses": {
                "intro": "Let's honestly explore your professional strengths and growth areas.",
                "questions": [
                    {
                        "question": "What do you consider your greatest strengths?",
                        "options": [
                            "Strong analytical and problem-solving skills",
                            "Excellent communication abilities",
                            "Creative thinking and innovation",
                            "Leadership and team management",
                            "Attention to detail and accuracy",
                            "Adaptability and flexibility",
                            "Persistence and determination",
                            "Empathy and interpersonal skills"
                        ]
                    },
                    {
                        "question": "Which areas do you feel you could develop further?",
                        "options": [
                            "Public speaking and presentations",
                            "Technical skills and knowledge",
                            "Time management and organization",
                            "Networking and relationship building",
                            "Conflict resolution",
                            "Strategic thinking",
                            "Financial and business acumen",
                            "Cross-cultural communication"
                        ]
                    },
                    {
                        "question": "How do you typically work on self-improvement?",
                        "options": [
                            "Formal training and courses",
                            "Reading and self-study",
                            "Seeking feedback from others",
                            "Finding mentors and coaches",
                            "Practicing new skills regularly",
                            "Joining professional groups",
                            "Reflecting on experiences",
                            "Setting specific goals"
                        ]
                    }
                ]
            },
            "emotional_intelligence": {
                "intro": "Let's explore your interpersonal skills and emotional awareness.",
                "questions": [
                    {
                        "question": "How do you typically handle workplace relationships?",
                        "options": [
                            "Build strong personal connections",
                            "Maintain professional boundaries",
                            "Act as a mediator in conflicts",
                            "Provide support and encouragement",
                            "Focus on task completion",
                            "Adapt my style to different people",
                            "Listen actively and empathetically"
                        ]
                    },
                    {
                        "question": "How do you manage your emotions in challenging situations?",
                        "options": [
                            "Stay calm and composed",
                            "Take time to process before responding",
                            "Express feelings openly and honestly",
                            "Focus on finding solutions",
                            "Seek support from trusted colleagues",
                            "Use stress management techniques",
                            "Channel emotions into motivation"
                        ]
                    },
                    {
                        "question": "What's your approach to understanding others?",
                        "options": [
                            "Ask questions and listen carefully",
                            "Observe body language and non-verbals",
                            "Put myself in their shoes",
                            "Consider their background and perspective",
                            "Pay attention to their communication style",
                            "Notice patterns in their behavior",
                            "Create safe spaces for sharing"
                        ]
                    }
                ]
            },
            "track_record": {
                "intro": "Let's review your accomplishments and success patterns.",
                "questions": [
                    {
                        "question": "What achievements are you most proud of?",
                        "options": [
                            "Academic accomplishments and degrees",
                            "Professional promotions and recognition",
                            "Projects I led or contributed to",
                            "Problems I solved or innovations I created",
                            "People I helped or mentored",
                            "Skills I developed or mastered",
                            "Challenges I overcame",
                            "Positive changes I made in organizations"
                        ]
                    },
                    {
                        "question": "What patterns do you see in your successes?",
                        "options": [
                            "Strong preparation and planning",
                            "Persistence through difficulties",
                            "Collaboration and teamwork",
                            "Creative problem-solving",
                            "Attention to quality and detail",
                            "Building strong relationships",
                            "Continuous learning and improvement",
                            "Taking calculated risks"
                        ]
                    },
                    {
                        "question": "What have you learned about yourself from your experiences?",
                        "options": [
                            "I thrive under pressure",
                            "I'm naturally curious and love learning",
                            "I work best when helping others",
                            "I excel at seeing the big picture",
                            "I'm good at bringing people together",
                            "I enjoy solving complex problems",
                            "I'm resilient and bounce back from setbacks",
                            "I'm motivated by meaningful work"
                        ]
                    }
                ]
            },
            "constraints": {
                "intro": "Let's honestly discuss practical considerations that influence your career choices.",
                "questions": [
                    {
                        "question": "Which factors influence your career choices?",
                        "options": [
                            "Geographic location preferences",
                            "Family responsibilities and commitments",
                            "Financial needs and obligations",
                            "Work schedule and flexibility requirements",
                            "Health or physical considerations",
                            "Educational or skill requirements",
                            "Industry stability and job security",
                            "Company culture and values alignment"
                        ]
                    },
                    {
                        "question": "What are your non-negotiable requirements?",
                        "options": [
                            "Work-life balance",
                            "Competitive salary",
                            "Opportunities for advancement",
                            "Meaningful and purposeful work",
                            "Flexible work arrangements",
                            "Professional development opportunities",
                            "Supportive work environment",
                            "Job security and stability"
                        ]
                    },
                    {
                        "question": "How do you typically navigate career constraints?",
                        "options": [
                            "Find creative solutions and alternatives",
                            "Prioritize what's most important",
                            "Gradually work toward ideal situation",
                            "Seek advice and guidance from others",
                            "Make temporary compromises for long-term goals",
                            "Focus on what I can control",
                            "Adapt expectations to reality",
                            "Look for opportunities within limitations"
                        ]
                    }
                ]
            }
        }
        
        return questions_map.get(self.assessment_type, {
            "intro": "Let's explore this aspect of your career journey.",
            "questions": [
                {
                    "question": "Tell me about your preferences in this area:",
                    "options": ["Option 1", "Option 2", "Option 3"]
                }
            ]
        })
    
    async def process_interaction(self, user_input: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Process interaction with multiple choice questions"""
        try:
            user_name = user_profile.get('name', 'there')
            
            # If no input or starting fresh, show intro and first question
            if not user_input or self.question_index == 0:
                return self._get_first_question(user_name)
            
            # Process the selected options
            if isinstance(user_input, str) and user_input.strip():
                # Parse selected options (they come as comma-separated string)
                selected_options = [opt.strip() for opt in user_input.split(',') if opt.strip()]
                self.user_responses.append({
                    "question": self.questions_data["questions"][self.question_index - 1]["question"],
                    "selected_options": selected_options
                })
            
            # Check if we have more questions
            if self.question_index < len(self.questions_data["questions"]):
                return self._get_next_question(user_name)
            else:
                return await self._complete_assessment(user_name, user_profile)
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Hi {user_profile.get('name', 'there')}! Let's continue with your assessment.",
                "show_options": False
            }
    
    def _get_first_question(self, user_name: str) -> Dict[str, Any]:
        """Get the first question with options"""
        intro = self.questions_data["intro"]
        first_question = self.questions_data["questions"][0]
        
        self.question_index = 1
        
        return {
            "success": True,
            "message": f"Hi {user_name}! {intro}",
            "current_question": first_question,
            "question_number": 1,
            "total_questions": len(self.questions_data["questions"]),
            "show_options": True,
            "assessment_complete": False
        }
    
    def _get_next_question(self, user_name: str) -> Dict[str, Any]:
        """Get the next question with options"""
        current_question = self.questions_data["questions"][self.question_index]
        self.question_index += 1
        
        return {
            "success": True,
            "message": f"Great choices, {user_name}! Let's continue...",
            "current_question": current_question,
            "question_number": self.question_index,
            "total_questions": len(self.questions_data["questions"]),
            "show_options": True,
            "assessment_complete": False
        }
    
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
class MasterCareerAgent:
    """Master agent for orchestrating the career counseling process"""
    
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Master Career Counselor"
    
    def get_assessment_progress(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate assessment progress"""
        assessments = user_profile.get('assessments', {})
        all_dimensions = [
            'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
            'cognitive_abilities', 'learning_preferences', 'physical_context',
            'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
        ]
        
        completed = [dim for dim in all_dimensions if assessments.get(dim, {}).get('completed', False)]
        remaining = [dim for dim in all_dimensions if dim not in completed]
        
        return {
            "completed": completed,
            "remaining": remaining,
            "progress_percentage": round((len(completed) / len(all_dimensions)) * 100, 1),
            "total_dimensions": len(all_dimensions)
        }
    
    def get_next_options(self, user_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get next assessment options"""
        progress = self.get_assessment_progress(user_profile)
        
        options_map = {
            "personality": {"title": "🧠 Personality Assessment", "description": "Discover your natural work style and preferences"},
            "interests": {"title": "💡 Career Interests", "description": "Explore what truly engages and motivates you"},
            "aspirations": {"title": "🎯 Career Aspirations", "description": "Define your career goals and future vision"},
            "skills": {"title": "🛠️ Skills Assessment", "description": "Evaluate your current abilities and strengths"},
            "motivations_values": {"title": "⭐ Values & Motivations", "description": "Identify your core values and what drives you"},
            "cognitive_abilities": {"title": "🧩 Cognitive Abilities", "description": "Understand your thinking and problem-solving style"},
            "learning_preferences": {"title": "📚 Learning Preferences", "description": "Discover how you learn and process information best"},
            "physical_context": {"title": "🌍 Work Environment", "description": "Identify your ideal work setting and conditions"},
            "strengths_weaknesses": {"title": "💪 Strengths & Growth Areas", "description": "Honest assessment of abilities and development areas"},
            "emotional_intelligence": {"title": "❤️ Emotional Intelligence", "description": "Assess your interpersonal and emotional skills"},
            "track_record": {"title": "🏆 Track Record", "description": "Review your achievements and success patterns"},
            "constraints": {"title": "⚖️ Practical Considerations", "description": "Identify factors that influence your career choices"}
        }
        
        # Show all remaining options (no limit)
        remaining = progress["remaining"]
        options = []
        
        for dim in remaining:
            if dim in options_map:
                option_info = options_map[dim]
                options.append({
                    "agent": dim,
                    "title": option_info["title"],
                    "description": option_info["description"]
                })
        
        # Add insights option if some assessments completed
        if len(progress["completed"]) >= 3:
            options.append({
                "agent": "insights",
                "title": "📊 Get Career Insights",
                "description": "Review your progress and get preliminary insights"
            })
        
        # Add action plan option if 8+ assessments completed
        if len(progress["completed"]) >= 8:
            options.append({
                "agent": "action_plan",
                "title": "🎯 Generate Career Action Plan",
                "description": "Create your personalized career development roadmap"
            })
        
        return options
    
    async def generate_insights(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate career insights from completed assessments"""
        progress = self.get_assessment_progress(user_profile)
        assessments = user_profile.get('assessments', {})
        user_name = user_profile.get('name', 'User')
        
        completed_data = {k: v for k, v in assessments.items() if v.get('completed', False)}
        
        # Format assessment data for better analysis - Fix data access pattern
        formatted_data = []
        for dim, data in completed_data.items():
            # Check both possible data structures (data or assessment_data)
            assessment_info = data.get('data', {}) or data.get('assessment_data', {})
            if assessment_info:  # If we have assessment data
                formatted_data.append(f"{dim.upper()}: {assessment_info.get('summary', 'Assessment completed')}")
                if assessment_info.get('strengths'):
                    formatted_data.append(f"  Strengths: {', '.join(assessment_info['strengths'])}")
                if assessment_info.get('career_implications'):
                    formatted_data.append(f"  Career Implications: {', '.join(assessment_info['career_implications'])}")
                if assessment_info.get('themes'):
                    formatted_data.append(f"  Themes: {', '.join(assessment_info['themes'])}")
                if assessment_info.get('key_insights'):
                    formatted_data.append(f"  Key Insights: {', '.join(assessment_info['key_insights'])}")
        
        formatted_assessment_text = "\n".join(formatted_data) if formatted_data else "No assessment data found"
        
        # Debug check for empty data
        if not formatted_data:
            return {
                "success": False,
                "message": f"Hi {user_name}! I'm having trouble accessing your assessment data. Please try refreshing the page or retaking one of your assessments.",
                "debug_info": f"No formatted data from {len(completed_data)} completed assessments"
            }
        
        prompt = f"""As an expert Master Career Counselor, analyze {user_name}'s assessment data and provide career insights.

ASSESSMENT DATA:
{formatted_assessment_text}

USER: {user_name} ({len(progress['completed'])}/12 assessments completed)

Provide insights in this exact JSON format (no extra text or markdown):

{{
  "success": true,
  "message": "{user_name}, based on your {len(progress['completed'])} completed assessments, here are your key career insights...",
  "key_patterns": ["Pattern 1", "Pattern 2", "Pattern 3"],
  "career_directions": ["Direction 1", "Direction 2", "Direction 3"],
  "personalized_insights": ["Insight 1", "Insight 2", "Insight 3"],
  "next_priorities": ["Next step 1", "Next step 2"],
  "confidence_level": "Based on {len(progress['completed'])} assessments - confident insights"
}}"""

        try:
            response = await self.llm.ainvoke(prompt)
            response_content = response.content.strip()
            
            # Better debugging for empty responses
            if not response_content:
                return {
                    "success": False,
                    "message": f"Hi {user_name}! The AI is having trouble right now. Please try again in 30 seconds.",
                    "debug_info": "Empty response from model"
                }
            
            # Clean the response and parse JSON - improved cleaning
            cleaned_content = response_content
            
            # Remove common markdown artifacts
            cleaned_content = cleaned_content.replace("```json", "").replace("```", "").strip()
            
            # Remove any leading/trailing text that's not JSON
            start_brace = cleaned_content.find("{")
            end_brace = cleaned_content.rfind("}") + 1
            
            if start_brace != -1 and end_brace > start_brace:
                cleaned_content = cleaned_content[start_brace:end_brace]
            
            if not cleaned_content or cleaned_content == "{}":
                return {
                    "success": False,
                    "message": f"Hi {user_name}! The AI generated an empty response. Please try again in a moment.",
                    "debug_info": f"Empty or invalid JSON after cleaning. Original length: {len(response_content)}"
                }
            
            result = json.loads(cleaned_content)
            return {"success": True, **result}
            
        except json.JSONDecodeError as e:
            # Return specific JSON error with response preview
            return {
                "success": False, 
                "message": f"Hi {user_name}! I'm processing your {len(progress['completed'])} assessments but need a moment to organize the insights. Please try again.",
                "debug_info": f"JSON parse error: {str(e)}",
                "response_preview": response.content[:100] if 'response' in locals() else "No response captured"
            }
        except Exception as e:
            error_str = str(e)
            
            # Check for specific API errors
            if '429' in error_str or 'quota' in error_str.lower():
                return {
                    "success": False,
                    "error_type": "rate_limit",
                    "message": "AI service temporarily busy. Please wait 30-60 seconds and try again.",
                    "technical_details": error_str
                }
            elif 'timeout' in error_str.lower():
                return {
                    "success": False,
                    "error_type": "timeout",
                    "message": "Request timed out. Please try again.",
                    "technical_details": error_str
                }
            else:
                # Fallback response for any other errors
                return {
                    "success": False,
                    "message": f"Great progress so far, {user_name}! You've completed {len(progress['completed'])} assessments. Each one reveals valuable insights about your career potential. Continue with the remaining assessments for even deeper insights!",
                    "key_patterns": ["Self-aware and reflective", "Committed to growth"],
                    "career_directions": ["Multiple paths emerging - complete more assessments for specificity"],
                    "technical_error": error_str
                }
    
    async def generate_action_plan(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive career action plan"""
        assessments = user_profile.get('assessments', {})
        user_name = user_profile.get('name', 'User')
        background = user_profile.get('background', 'Professional')
        
        # Format all assessment data for comprehensive analysis - Fix data access pattern
        all_assessments_formatted = []
        for dim, data in assessments.items():
            if data.get('completed'):
                # Check both possible data structures (data or assessment_data)
                assessment_info = data.get('data', {}) or data.get('assessment_data', {})
                if assessment_info:
                    all_assessments_formatted.append(f"\n{dim.upper()}:")
                    all_assessments_formatted.append(f"  Summary: {assessment_info.get('summary', 'Assessment completed')}")
                    if assessment_info.get('strengths'):
                        all_assessments_formatted.append(f"  Strengths: {', '.join(assessment_info['strengths'])}")
                    if assessment_info.get('career_implications'):
                        all_assessments_formatted.append(f"  Career Implications: {', '.join(assessment_info['career_implications'])}")
                    if assessment_info.get('themes'):
                        all_assessments_formatted.append(f"  Themes: {', '.join(assessment_info['themes'])}")
                    if assessment_info.get('key_insights'):
                        all_assessments_formatted.append(f"  Key Insights: {', '.join(assessment_info['key_insights'])}")
        
        complete_profile_text = "\n".join(all_assessments_formatted) if all_assessments_formatted else "Assessment data not accessible"
        progress = self.get_assessment_progress(user_profile)
        
        # Debug check for empty assessment data
        if not all_assessments_formatted:
            completed_count = len([k for k, v in assessments.items() if v.get('completed')])
            return {
                "success": False,
                "message": f"Hi {user_name}! I'm having trouble accessing your detailed assessment data. Please refresh the page and try again.",
                "debug_info": f"No formatted assessment data from {completed_count} completed assessments"
            }
        
        prompt = f"""As a Master Career Counselor, create a personalized career action plan for {user_name}.

COMPLETE ASSESSMENT DATA:
{complete_profile_text}

USER: {user_name} ({len(progress['completed'])}/12 assessments completed)

Provide action plan in this exact JSON format (no extra text or markdown):

{{
  "success": true,
  "message": "{user_name}, congratulations on completing your assessment! Here's your personalized career action plan...",
  "career_summary": "Your primary career direction based on assessment results",
  "key_strengths": ["Strength 1", "Strength 2", "Strength 3", "Strength 4"],
  "immediate_actions": ["Action for next 30 days", "Action for next 60 days", "Action for next 90 days"],
  "career_paths": ["Primary career option", "Alternative career path", "Growth opportunity"],
  "next_steps": ["This week", "Next month", "Next quarter"]
}}"""

        try:
            response = await self.llm.ainvoke(prompt)
            response_content = response.content.strip()
            
            # Check for empty response
            if not response_content:
                return {
                    "success": False,
                    "message": f"Hi {user_name}! I'm working on your action plan but need a moment. Please try again in 30 seconds.",
                    "debug_info": "Empty response from model"
                }
                
            # Clean and parse JSON - improved cleaning
            cleaned_content = response_content
            
            # Remove common markdown artifacts
            cleaned_content = cleaned_content.replace("```json", "").replace("```", "").strip()
            
            # Remove any leading/trailing text that's not JSON
            start_brace = cleaned_content.find("{")
            end_brace = cleaned_content.rfind("}") + 1
            
            if start_brace != -1 and end_brace > start_brace:
                cleaned_content = cleaned_content[start_brace:end_brace]
            
            if not cleaned_content or cleaned_content == "{}":
                return {
                    "success": False,
                    "message": f"Hi {user_name}! The AI generated an empty response for your action plan. Please try again in a moment.",
                    "debug_info": f"Empty or invalid JSON after cleaning. Original length: {len(response_content)}"
                }
                
            result = json.loads(cleaned_content)
            return {"success": True, **result}
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "message": f"Hi {user_name}! I'm creating your personalized action plan but need a moment to organize everything. Please try again shortly.",
                "debug_info": f"JSON parse error: {str(e)}",
                "response_preview": response.content[:100] if 'response' in locals() else "No response captured"
            }
        except Exception as e:
            error_str = str(e)
            
            # Check for specific API errors  
            if '429' in error_str or 'quota' in error_str.lower():
                return {
                    "success": False,
                    "error_type": "rate_limit", 
                    "message": "AI service temporarily busy processing action plans. Please wait 1-2 minutes and try again.",
                    "technical_details": error_str
                }
            elif 'timeout' in error_str.lower():
                return {
                    "success": False,
                    "error_type": "timeout",
                    "message": "Action plan generation timed out. Please try again.",
                    "technical_details": error_str
                }
            else:
                # Fallback response for any other errors
                return {
                    "success": False,
                    "message": f"Hi {user_name}! Based on your assessments, I can see you're someone who values growth and self-awareness. Complete a few more assessments for a fully detailed action plan!",
                    "career_summary": {
                        "primary_direction": "Multiple promising paths - complete more assessments for specificity",
                        "key_strengths": ["Self-awareness", "Growth mindset", "Commitment to development"]
                    },
                    "technical_error": error_str
                }

@st.cache_resource
def initialize_system():
    """Initialize the system components with Enhanced Master Agent"""
    llm = get_llm()
    
    # Initialize the new Enhanced Master Agent as primary interface
    enhanced_master_agent = EnhancedMasterAgent(llm)
    
    # Initialize all 12D assessment agents
    agents = {
        'personality': EnhancedAgent(llm, "Personality & Work Style Counselor", "personality"),
        'interests': EnhancedAgent(llm, "Career Interests Counselor", "interests"),
        'aspirations': EnhancedAgent(llm, "Career Aspirations Counselor", "aspirations"),
        'skills': EnhancedAgent(llm, "Skills Assessment Counselor", "skills"),
        'motivations_values': EnhancedAgent(llm, "Values & Motivations Counselor", "motivations_values"),
        'cognitive_abilities': EnhancedAgent(llm, "Cognitive Abilities Counselor", "cognitive_abilities"),
        'learning_preferences': EnhancedAgent(llm, "Learning Preferences Counselor", "learning_preferences"),
        'physical_context': EnhancedAgent(llm, "Work Environment Counselor", "physical_context"),
        'strengths_weaknesses': EnhancedAgent(llm, "Strengths & Development Counselor", "strengths_weaknesses"),
        'emotional_intelligence': EnhancedAgent(llm, "Emotional Intelligence Counselor", "emotional_intelligence"),
        'track_record': EnhancedAgent(llm, "Achievement & Experience Counselor", "track_record"),
        'constraints': EnhancedAgent(llm, "Practical Considerations Counselor", "constraints"),
    }
    
    # Initialize career tools
    career_tools = {
        'resume_builder': ResumeBuilder(llm),
        'mock_interview': MockInterviewAI(llm),
        'job_matcher': JobMatcherSkillAnalyzer(llm),
        'linkedin_enhancer': LinkedInEnhancer(llm),
        'application_tracker': ApplicationTracker(llm)
    }
    
    # Keep the old master agent for backward compatibility
    master_agent = MasterCareerAgent(llm)
    user_manager = UserManager()
    
    return agents, career_tools, enhanced_master_agent, master_agent, user_manager

def apply_enhanced_css():
    """Apply comprehensive custom styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102,126,234,0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.95;
        margin: 0;
        font-weight: 400;
    }
    
    /* Progress Dashboard */
    .progress-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .progress-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #4a5568;
        font-weight: 500;
    }
    
    /* Agent Option Cards */
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .agent-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .agent-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .agent-card:hover::before {
        transform: scaleX(1);
    }
    
    .agent-card:hover {
        border-color: #667eea;
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(102,126,234,0.15);
    }
    
    .agent-card-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .agent-card-description {
        font-size: 1rem;
        color: #4a5568;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Chat Interface */
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .agent-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .agent-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
    }
    
    .agent-info h3 {
        margin: 0;
        color: #2d3748;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    .agent-info p {
        margin: 0.25rem 0 0 0;
        color: #4a5568;
        font-size: 1rem;
    }
    
    /* Action Plan Styling */
    .action-plan {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .action-plan-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .action-item {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    
    .action-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Assessment Badges */
    .assessment-badge {
        display: inline-block;
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.25rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(72,187,120,0.3);
    }
    
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(102,126,234,0.3);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        border-radius: 15px !important;
        border: none !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important;
    }
    
    /* Sidebar Enhancements */
    .sidebar-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Progress Bar Enhancement */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .agent-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .progress-container {
            padding: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_career_tools_interface(career_tools: Dict[str, Any], user_profile: Dict[str, Any]):
    """Display the career tools interface"""
    
    st.markdown("### 🛠️ Career Development Tools")
    st.markdown("Access professional tools to accelerate your career growth")
    
    # Tools grid
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Resume Builder & ATS Optimizer", use_container_width=True, help="Create professional resumes optimized for ATS systems"):
            st.session_state.active_tool = "resume_builder"
            st.rerun()
        
        if st.button("🔍 Job Matcher & Skill Gap Analyzer", use_container_width=True, help="Analyze job matches and identify skill gaps"):
            st.session_state.active_tool = "job_matcher"
            st.rerun()
        
        if st.button("📋 Application Tracker & Career Dashboard", use_container_width=True, help="Track applications and manage your job search"):
            st.session_state.active_tool = "application_tracker"
            st.rerun()
    
    with col2:
        if st.button("🎤 Mock Interview AI Simulator", use_container_width=True, help="Practice interviews with AI-powered feedback"):
            st.session_state.active_tool = "mock_interview"
            st.rerun()
        
        if st.button("💼 LinkedIn Profile Enhancer", use_container_width=True, help="Optimize your LinkedIn presence and networking"):
            st.session_state.active_tool = "linkedin_enhancer"
            st.rerun()
        
        # Placeholder for future tool
        st.button("🎯 Coming Soon: Salary Negotiator", use_container_width=True, disabled=True, help="AI-powered salary negotiation guidance (coming soon)")

def display_active_tool(career_tools: Dict[str, Any], user_profile: Dict[str, Any]):
    """Display the currently active career tool"""
    
    active_tool = st.session_state.get('active_tool', None)
    
    if not active_tool:
        return
    
    # Back button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅️ Back to Tools", key="back_to_tools"):
            st.session_state.active_tool = None
            st.rerun()
    
    # Display appropriate tool
    try:
        if active_tool == "resume_builder":
            career_tools['resume_builder'].display_resume_builder(user_profile)
        
        elif active_tool == "mock_interview":
            career_tools['mock_interview'].display_mock_interview(user_profile)
        
        elif active_tool == "job_matcher":
            career_tools['job_matcher'].display_job_matcher_analyzer(user_profile)
        
        elif active_tool == "linkedin_enhancer":
            career_tools['linkedin_enhancer'].display_linkedin_enhancer(user_profile)
        
        elif active_tool == "application_tracker":
            career_tools['application_tracker'].display_application_tracker(user_profile)
        
        else:
            st.error(f"Unknown tool: {active_tool}")
            st.session_state.active_tool = None
            st.rerun()
    
    except Exception as e:
        st.error(f"Error loading tool: {str(e)}")
        st.info("Please try again or contact support if the issue persists.")
        
        # Debug info for development
        st.expander("Debug Info").write(str(e))

def display_progress_dashboard(user_profile: Dict[str, Any], master_agent):
    """Display enhanced progress dashboard"""
    progress = master_agent.get_assessment_progress(user_profile)
    
    # DEBUG: Add debugging info (remove this after fixing)
    if st.checkbox("🔧 Debug Mode - Show Raw Data", key="debug_mode"):
        st.write("**DEBUG INFO:**")
        st.write(f"User Profile Name: {user_profile.get('name', 'Unknown')}")
        assessments = user_profile.get('assessments', {})
        st.write(f"Total assessments in profile: {len(assessments)}")
        
        for key, value in assessments.items():
            completed = value.get('completed', False)
            st.write(f"  {key}: completed = {completed}")
        
        st.write(f"Progress data: {progress}")
        
        # Add cache clear button
        if st.button("🔄 Clear Cache & Refresh", key="clear_cache_btn"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Cache cleared! Please refresh the page.")
            st.rerun()
        
        st.write("---")
    
    st.markdown(f"""
    <div class="progress-container fade-in">
        <div class="progress-title">🎯 Your Career Discovery Journey</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(progress['completed'])}</div>
            <div class="metric-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(progress['remaining'])}</div>
            <div class="metric-label">Remaining</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{progress['progress_percentage']}%</div>
            <div class="metric-label">Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">12</div>
            <div class="metric-label">Dimensions</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress['progress_percentage'] / 100)
    
    # Detailed Assessment Status
    st.markdown("### 📊 Assessment Status")
    
    # All 12 dimensions for reference
    all_dimensions = [
        'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
        'cognitive_abilities', 'learning_preferences', 'physical_context',
        'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
    ]
    
    # Create two columns for completed and remaining
    col_completed, col_remaining = st.columns(2)
    
    with col_completed:
        st.markdown("#### ✅ Completed")
        if progress['completed']:
            for dimension in progress['completed']:
                display_name = dimension.replace('_', ' ').title()
                st.markdown(f"✅ **{display_name}**")
        else:
            st.markdown("*No assessments completed yet*")
    
    with col_remaining:
        st.markdown("#### ⏳ Remaining")
        if progress['remaining']:
            for dimension in progress['remaining']:
                display_name = dimension.replace('_', ' ').title()
                st.markdown(f"⏳ {display_name}")
        else:
            st.markdown("🎉 **All assessments completed!**")

def display_agent_options(options: List[Dict[str, str]]):
    """Display enhanced agent options"""
    st.markdown("### 🎯 Choose Your Next Step")
    st.markdown("*Select any area below to continue your career discovery journey*")
    
    selected_agent = None
    
    # Create responsive grid based on number of options
    if len(options) <= 2:
        cols = st.columns(len(options))
    elif len(options) <= 4:
        cols = st.columns(2)
    elif len(options) <= 6:
        cols = st.columns(3)
    else:
        cols = st.columns(4)  # Handle more options with 4 columns
    
    for i, option in enumerate(options):
        col_index = i % len(cols)
        
        with cols[col_index]:
            # Create card HTML
            card_html = f"""
            <div class="agent-card fade-in" style="animation-delay: {i * 0.1}s;">
                <div class="agent-card-title">{option['title']}</div>
                <div class="agent-card-description">{option['description']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Button for selection - Use unique keys and immediate action
            button_key = f"btn_{option['agent']}_{i}_{hash(option['title'])}"
            if st.button(f"Start {option['title'].split()[-1]}", key=button_key, help=option['description']):
                # Store selection in session state for immediate processing
                st.session_state.selected_agent_action = option['agent']
                selected_agent = option['agent']
                # Force immediate rerun to process the selection
                st.rerun()
    
    # Check if there's a pending action from session state
    if hasattr(st.session_state, 'selected_agent_action') and st.session_state.selected_agent_action:
        selected_agent = st.session_state.selected_agent_action
        # Clear the action to prevent repeated execution
        st.session_state.selected_agent_action = None
    
    return selected_agent

def display_chat_interface(agent, user_profile: Dict[str, Any]):
    """Display enhanced chat interface with multiple choice questions"""
    user_name = user_profile.get('name', 'User')
    
    st.markdown(f"""
    <div class="chat-container fade-in">
        <div class="agent-header">
            <div class="agent-avatar">🤖</div>
            <div class="agent-info">
                <h3>{agent.agent_name}</h3>
                <p>Personalized guidance for {user_name}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for this agent
    agent_key = f"agent_{agent.assessment_type}"
    if f'{agent_key}_initialized' not in st.session_state:
        st.session_state[f'{agent_key}_initialized'] = False
        st.session_state[f'{agent_key}_current_result'] = None
    
    # Get initial question if not initialized
    if not st.session_state[f'{agent_key}_initialized']:
        with st.spinner("Loading assessment questions..."):
            try:
                initial_result = asyncio.run(agent.process_interaction("", user_profile))
                st.session_state[f'{agent_key}_current_result'] = initial_result
                st.session_state[f'{agent_key}_initialized'] = True
                st.rerun()
            except Exception as e:
                st.error(f"Error loading questions: {str(e)}")
                return
    
    # Display current question and handle responses
    current_result = st.session_state.get(f'{agent_key}_current_result')
    
    if current_result and current_result.get('success'):
        # Display the message
        with st.chat_message("assistant", avatar="🤖"):
            st.write(current_result['message'])
        
        # Check if assessment is complete
        if current_result.get('assessment_complete'):
            st.success("✅ Assessment completed successfully!")
            
            # Update user profile
            if current_result.get('assessment_data'):
                assessment_type = agent.assessment_type
                user_profile.setdefault('assessments', {})
                user_profile['assessments'][assessment_type] = {
                    'completed': True,
                    'data': current_result['assessment_data'],
                    'completed_at': datetime.now().isoformat()
                }
                
                # Save to user manager
                if 'user_manager' in st.session_state:
                    st.session_state.user_manager.save_user_profile(user_profile)
            
            # Show completion message and option to go back
            st.balloons()
            time.sleep(2)
            if st.button("🏠 Return to Dashboard", key=f"return_{agent.assessment_type}"):
                st.session_state.current_agent = None
                st.session_state[f'{agent_key}_initialized'] = False
                st.session_state[f'{agent_key}_current_result'] = None
                st.rerun()
            return
        
        # Display multiple choice question if available
        if current_result.get('show_options') and current_result.get('current_question'):
            question_data = current_result['current_question']
            question_num = current_result.get('question_number', 1)
            total_questions = current_result.get('total_questions', 1)
            
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border-left: 4px solid #667eea;">
                <h4 style="color: #2d3748; margin: 0 0 1rem 0;">
                    Question {question_num} of {total_questions}
                </h4>
                <p style="font-size: 1.1rem; color: #4a5568; margin: 0; font-weight: 500;">
                    {question_data['question']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create checkboxes for multiple selection
            st.markdown("**Select all options that apply to you:**")
            
            selected_options = []
            for i, option in enumerate(question_data['options']):
                if st.checkbox(option, key=f"{agent.assessment_type}_q{question_num}_option_{i}"):
                    selected_options.append(option)
            
            # Show progress
            progress_percentage = (question_num - 1) / total_questions
            st.progress(progress_percentage)
            st.write(f"Progress: {question_num - 1}/{total_questions} questions completed")
            
            # Submit button
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("➡️ Next", key=f"next_{agent.assessment_type}_{question_num}", 
                           disabled=len(selected_options) == 0,
                           help="Please select at least one option to continue"):
                    if selected_options:
                        # Process the selected options
                        selected_text = ", ".join(selected_options)
                        
                        with st.spinner("Processing your selections..."):
                            try:
                                result = asyncio.run(agent.process_interaction(selected_text, user_profile))
                                st.session_state[f'{agent_key}_current_result'] = result
                                
                                # Clear the checkboxes by rerunning
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"Error processing response: {str(e)}")
                    else:
                        st.warning("Please select at least one option before continuing.")
            
            # Show selected options
            if selected_options:
                st.markdown("**Your selections:**")
                for option in selected_options:
                    st.markdown(f"✓ {option}")
        
        else:
            # Fallback chat input for non-multiple-choice interactions
            user_input = st.chat_input(f"Share your thoughts with {agent.agent_name}...")
            
            if user_input:
                with st.spinner("Processing your response..."):
                    try:
                        result = asyncio.run(agent.process_interaction(user_input, user_profile))
                        st.session_state[f'{agent_key}_current_result'] = result
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    else:
        st.error("Unable to load assessment questions. Please try again.")

def display_action_plan(action_plan: Dict[str, Any]):
    """Display comprehensive action plan with enhanced features"""
    if not action_plan.get('success', True):
        st.info(action_plan.get('message', 'Complete more assessments for a detailed action plan.'))
        return
    
    st.markdown(f"""
    <div class="action-plan fade-in">
        <div class="action-plan-title">🎯 Your Personalized Career Action Plan</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    if action_plan.get('message'):
        st.success(action_plan['message'])
    
    # Career Summary
    if action_plan.get('career_summary'):
        st.markdown("## 📊 Career Direction")
        st.info(f"**🎯 Recommended Path:** {action_plan['career_summary']}")
    
    # Key Strengths
    if action_plan.get('key_strengths'):
        st.markdown("## 🌟 Your Key Strengths")
        strengths_html = ""
        for strength in action_plan['key_strengths']:
            strengths_html += f'<span class="skill-badge">{strength}</span> '
        st.markdown(strengths_html, unsafe_allow_html=True)
    
    # Immediate Actions
    if action_plan.get('immediate_actions'):
        st.markdown("## ⚡ Immediate Actions")
        for i, action in enumerate(action_plan['immediate_actions'], 1):
            st.markdown(f"""
            <div class="action-item">
                <h4>🎯 Step {i}</h4>
                <p>{action}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Career Paths
    if action_plan.get('career_paths'):
        st.markdown("## 🛤️ Career Path Options")
        for i, path in enumerate(action_plan['career_paths'], 1):
            st.markdown(f"**{i}.** {path}")
    
    # Next Steps
    if action_plan.get('next_steps'):
        st.markdown("## 📅 Next Steps Timeline")
        for i, step in enumerate(action_plan['next_steps'], 1):
            st.markdown(f"**{i}.** {step}")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Download Action Plan", use_container_width=True):
            st.info("Download feature coming soon!")
    with col2:
        if st.button("📧 Email to Myself", use_container_width=True):
            st.info("Email feature coming soon!")
    with col3:
        if st.button("🔄 Generate New Plan", use_container_width=True):
            if 'action_plan' in st.session_state:
                del st.session_state['action_plan']
            st.rerun()
    
    # Skill Development
    if action_plan.get('skill_development'):
        st.markdown("## 🛠️ Skill Development Plan")
        for skill in action_plan['skill_development']:
            st.markdown(f"""
            <div class="action-item">
                <h4>📚 {skill.get('skill', 'Skill to Develop')}</h4>
                <p><strong>Approach:</strong> {skill.get('approach', 'Structured learning')}</p>
                <p><strong>Timeline:</strong> {skill.get('timeline', '3-6 months')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Personalized Strategies
    if action_plan.get('personalized_strategies'):
        st.markdown("## 🎯 Personalized Success Strategies")
        for strategy in action_plan['personalized_strategies']:
            st.write(f"• {strategy}")
    
    # Next Steps
    if action_plan.get('next_steps'):
        st.markdown("## 📋 Your Next Steps")
        for i, step in enumerate(action_plan['next_steps'], 1):
            st.write(f"{i}. {step}")
    
    # Success Metrics
    if action_plan.get('success_metrics'):
        st.markdown("## 📊 Success Metrics")
        st.info("Track these indicators to measure your career progress:")
        for metric in action_plan['success_metrics']:
            st.write(f"• {metric}")
    
    # Download option
    if st.button("📥 Download Action Plan", use_container_width=True):
        st.info("📁 Your action plan has been saved to your profile!")
    
    st.markdown("---")
    st.success("🎉 Your personalized career roadmap is complete! Use this as your guide to career success.")

def display_conversation_interface(enhanced_master_agent, user_profile: Dict[str, Any]):
    """
    New conversational interface with Enhanced Master Agent
    """
    user_name = user_profile.get('name', 'there')
    
    # Initialize conversation history in session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
        
    # Display conversation header
    st.markdown(f"""
    <div class="chat-container fade-in">
        <div class="agent-header">
            <div class="agent-avatar">🤖</div>
            <div class="agent-info">
                <h3>Master AI Counselor</h3>
                <p>Your personal career guide and AI assistant</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display conversation history
    for message in st.session_state.conversation_history:
        role = message.get('role', 'user')
        content = message.get('content', '')
        
        if role == 'user':
            with st.chat_message("user", avatar="👤"):
                st.write(content)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(content)
    
    # Chat input for new conversation
    user_input = st.chat_input(f"Hi {user_name}! Ask me anything - career questions, travel advice, or let's start your assessment journey...")
    
    if user_input:
        # Add user message to history
        st.session_state.conversation_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Display user message immediately
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)
        
        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = asyncio.run(enhanced_master_agent.process_conversation(
                        user_input, 
                        user_profile, 
                        st.session_state.conversation_history
                    ))
                    
                    if response.get('success', True):
                        ai_message = response.get('message', 'I understand. Let me help you with that.')
                        st.write(ai_message)
                        
                        # Add AI message to history
                        st.session_state.conversation_history.append({
                            'role': 'assistant',
                            'content': ai_message,
                            'timestamp': datetime.now().isoformat(),
                            'response_data': response
                        })
                        
                        # Check if AI suggests next actions
                        if response.get('requires_action'):
                            st.info("💡 **Next Steps Available**: I can help you take specific actions based on our conversation!")
                        
                        # Display follow-up questions if available
                        if response.get('follow_up_questions'):
                            st.markdown("**🤔 I'd like to know more:**")
                            for question in response['follow_up_questions']:
                                if st.button(f"💬 {question}", key=f"followup_{hash(question)}"):
                                    # Add the follow-up question as if user asked it
                                    st.session_state.conversation_history.append({
                                        'role': 'user',
                                        'content': question,
                                        'timestamp': datetime.now().isoformat(),
                                        'type': 'follow_up'
                                    })
                                    st.rerun()
                        
                        # Check if we should transition to assessments
                        if response.get('stage') in ['assessment_prep', 'assessment_active']:
                            st.success("🎯 Ready to dive deeper? Let's start your personalized assessments!")
                            if st.button("🚀 Begin Assessments", key="start_assessments"):
                                st.session_state.show_assessment_options = True
                                st.rerun()
                    
                    else:
                        st.error("I apologize, but I'm having trouble right now. Please try asking again in a different way.")
                
                except Exception as e:
                    st.error("I encountered a brief technical difficulty. Let me try to help you anyway!")
                    fallback_response = f"Hi {user_name}! I'm here to help you with any questions - from career guidance to general inquiries. What would you like to explore today?"
                    st.write(fallback_response)
                    
                    # Add fallback to history
                    st.session_state.conversation_history.append({
                        'role': 'assistant',
                        'content': fallback_response,
                        'timestamp': datetime.now().isoformat(),
                        'error': str(e)
                    })
        
        # Force rerun to show the new messages
        st.rerun()

def display_assessment_transition(enhanced_master_agent, user_profile: Dict[str, Any], agents: Dict):
    """
    Display assessment options when user is ready to transition from conversation to assessments
    """
    st.markdown("### 🎯 Ready for Your Personalized Assessment Journey?")
    
    # Get assessment orchestration
    try:
        assessment_status = asyncio.run(enhanced_master_agent.orchestrate_assessment_flow(user_profile))
        
        if assessment_status.get('status') == 'complete':
            st.success("🎉 Congratulations! You've completed all assessments!")
            st.markdown(assessment_status.get('message', 'Ready for comprehensive insights!'))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Get Career Insights", use_container_width=True):
                    st.session_state.show_insights = True
                    st.rerun()
            with col2:
                if st.button("🎯 Generate Action Plan", use_container_width=True):
                    st.session_state.show_action_plan = True
                    st.rerun()
        
        else:
            # Show progress
            completed = assessment_status.get('completed_count', 0)
            total = assessment_status.get('total_count', 12)
            progress = assessment_status.get('progress_percentage', 0)
            
            st.markdown(f"**Progress: {completed}/{total} assessments completed ({progress}%)**")
            st.progress(progress / 100)
            
            # Show message
            if assessment_status.get('message'):
                st.info(assessment_status['message'])
            
            # Suggest next assessment
            next_dimension = assessment_status.get('next_dimension')
            if next_dimension and next_dimension in agents:
                st.markdown(f"### 🎯 Recommended Next: {next_dimension.replace('_', ' ').title()}")
                
                # Generate personalized questions for this dimension
                with st.spinner("🤔 Preparing personalized questions for you..."):
                    try:
                        personalized_questions = asyncio.run(
                            enhanced_master_agent.generate_personalized_questions(
                                next_dimension,
                                user_profile
                            )
                        )
                        
                        if personalized_questions:
                            st.success("✨ I've prepared personalized questions based on our conversation!")
                            st.write("Preview of personalized questions:")
                            for i, q in enumerate(personalized_questions[:2], 1):
                                st.write(f"**{i}.** {q}")
                            if len(personalized_questions) > 2:
                                st.write(f"*...and {len(personalized_questions) - 2} more personalized questions*")
                    
                    except Exception as e:
                        st.info("I'll prepare great questions for you during the assessment!")
                
                # Start assessment button
                if st.button(f"🚀 Start {next_dimension.replace('_', ' ').title()} Assessment", 
                           key=f"start_{next_dimension}", 
                           use_container_width=True):
                    st.session_state.current_agent = next_dimension
                    st.session_state.show_assessment_options = False
                    st.rerun()
            
            # Show all available assessment options
            st.markdown("### 📋 Or Choose Any Assessment:")
            
            # Get available options 
            remaining_assessments = [dim for dim in enhanced_master_agent.assessment_dimensions 
                                   if not user_profile.get('assessments', {}).get(dim, {}).get('completed', False)]
            
            if remaining_assessments:
                cols = st.columns(min(3, len(remaining_assessments)))
                for i, dimension in enumerate(remaining_assessments[:6]):  # Show max 6 options
                    col_index = i % len(cols)
                    with cols[col_index]:
                        display_name = dimension.replace('_', ' ').title()
                        if st.button(f"📝 {display_name}", key=f"assess_{dimension}", use_container_width=True):
                            st.session_state.current_agent = dimension
                            st.session_state.show_assessment_options = False
                            st.rerun()
    
    except Exception as e:
        st.error("Having trouble loading assessment options. Let's continue with the conversation!")
        st.session_state.show_assessment_options = False
        st.rerun()

def main():
    """Enhanced main function with conversational interface"""
    
    # Page configuration
    st.set_page_config(
        page_title="Remiro AI - Your Personal AI Career Counselor",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    apply_enhanced_css()
    
    # Main header with updated messaging
    st.markdown("""
    <div class="main-header fade-in">
        <h1>🤖 Remiro AI</h1>
        <p>Your Personal AI Career Counselor & Life Assistant</p>
        <p style="font-size: 1rem; opacity: 0.9;">Ask me anything • Get career guidance • Complete personalized assessments</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    try:
        agents, career_tools, enhanced_master_agent, master_agent, user_manager = initialize_system()
    except Exception as e:
        st.error(f"⚠️ System initialization failed: {str(e)}")
        st.info("Please check your Google API key and try refreshing the page.")
        st.stop()
    
    # Store in session state
    if 'user_manager' not in st.session_state:
        st.session_state.user_manager = user_manager
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None
        
    if 'show_assessment_options' not in st.session_state:
        st.session_state.show_assessment_options = False
    
    # Sidebar - Simplified
    with st.sidebar:
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.header("👤 Your Profile")
        
        # Profile setup form
        with st.form("profile_form"):
            name = st.text_input("Your Name", placeholder="Enter your full name")
            background = st.selectbox(
                "Background",
                ["Student", "Recent Graduate", "Professional", "Career Changer", "Returning to Work"],
                help="This helps me personalize our conversation"
            )
            
            submitted = st.form_submit_button("🚀 Start Conversation", use_container_width=True)
            
            if submitted and name.strip():
                user_profile = user_manager.get_or_create_user(name.strip(), {"background": background})
                st.session_state.user_profile = user_profile
                st.session_state.conversation_history = []
                st.success(f"Welcome {name}! 🎉")
                time.sleep(1)
                st.rerun()
        
        # Current user info
        if st.session_state.user_profile:
            user_profile = st.session_state.user_profile
            st.markdown(f"""
            <div style="margin-top: 1rem; padding: 1rem; background: #f8fafc; border-radius: 10px;">
                <h4>👋 Hello, {user_profile.get('name', 'User')}!</h4>
                <p><strong>Background:</strong> {user_profile.get('background', 'Not specified')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Assessment progress
            assessments = user_profile.get('assessments', {})
            completed_count = len([a for a in assessments.values() if a.get('completed', False)])
            st.markdown(f"**Assessments Completed:** {completed_count}/12")
            
            if completed_count > 0:
                progress_percentage = (completed_count / 12) * 100
                st.progress(progress_percentage / 100)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear conversation button
        if st.session_state.user_profile and st.button("🔄 New Conversation"):
            st.session_state.conversation_history = []
            st.session_state.show_assessment_options = False
            st.session_state.current_agent = None
            st.rerun()
        
        # Help section
        st.markdown("---")
        st.markdown("### 🤖 I Can Help With")
        st.markdown("""
        💬 **Any Question** - Travel, studies, rates, advice
        🎯 **Career Guidance** - Personalized counseling  
        📊 **Assessment Journey** - 12D personality analysis
        📋 **Action Plans** - Step-by-step career roadmap
        """)
    
    # Main content
    if st.session_state.user_profile:
        user_profile = st.session_state.user_profile
        
        # Handle different interface states
        if st.session_state.current_agent:
            # Display specific agent assessment interface
            current_agent_name = st.session_state.current_agent
            current_agent = agents.get(current_agent_name)
            
            if current_agent:
                display_chat_interface(current_agent, user_profile)
                
                # Back button
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("⬅️ Back to Chat", key="back_to_chat"):
                        st.session_state.current_agent = None
                        st.rerun()
        
        elif st.session_state.get('show_assessment_options', False):
            # Show assessment transition interface
            display_assessment_transition(enhanced_master_agent, user_profile, agents)
        
        else:
            # Main conversational interface
            display_conversation_interface(enhanced_master_agent, user_profile)
    
    else:
        # Welcome message for new users
        st.markdown("""
        ### 👋 Welcome to Remiro AI!
        
        I'm your personal AI career counselor and assistant. I can help you with:
        
        🤖 **General Questions** - Ask me about anything (gold rates, travel advice, study guidance, etc.)
        🎯 **Career Counseling** - Get personalized, empathetic career guidance
        📊 **Assessment Journey** - Complete a comprehensive 12-dimensional career analysis  
        🚀 **Action Plans** - Receive detailed, personalized career roadmaps
        
        **To get started, please enter your name and background in the sidebar** ➡️
        
        I'll ask follow-up questions to understand your unique situation before giving you personalized advice.
        """)
        
        # Example questions
        st.markdown("### 💡 Example Conversations")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **General Questions:**
            - "What's the gold rate in India today?"
            - "Can you create an SOP for studying in USA?"
            - "I want to study in USA from India, what do I need?"
            """)
        
        with col2:
            st.markdown("""
            **Career Questions:**
            - "I'm confused about my career direction"
            - "Help me understand my strengths"  
            - "What career options fit my personality?"
            """)

if __name__ == "__main__":
    main()
