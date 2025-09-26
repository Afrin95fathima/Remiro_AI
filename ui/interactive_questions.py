"""
Interactive Question Components for Remiro AI
Checkbox-based questions with time-based assessment
"""

import streamlit as st
from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timedelta
import os
from pathlib import Path

class InteractiveQuestionSystem:
    """Handles checkbox-based questions and time-based assessments"""
    
    def __init__(self):
        self.time_options = {
            "3": {"minutes": 3, "questions_per_agent": 1, "total_questions": 12},
            "5": {"minutes": 5, "questions_per_agent": 2, "total_questions": 24},
            "7": {"minutes": 7, "questions_per_agent": 3, "total_questions": 36},
            "15": {"minutes": 15, "questions_per_agent": 5, "total_questions": 60},
            "15+": {"minutes": 20, "questions_per_agent": 8, "total_questions": 96}
        }
    
    def render_time_selection(self) -> Optional[str]:
        """Render time preference selection"""
        
        st.markdown("""
        <div style="background: #3a3a3a; padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid #505050;">
            <h3 style="color: #ffffff; margin-bottom: 15px;">⏰ How much time do you have today?</h3>
            <p style="color: #cccccc; margin-bottom: 20px;">
                Choose your available time for the assessment. We'll customize the questions accordingly:
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        time_choice = None
        
        with col1:
            if st.button("🚀 Quick\n3 minutes", key="time_3", use_container_width=True):
                time_choice = "3"
                st.markdown('<p style="color: #0084ff;">Quick assessment - 1 question per dimension</p>', 
                           unsafe_allow_html=True)
        
        with col2:
            if st.button("⚡ Fast\n5 minutes", key="time_5", use_container_width=True):
                time_choice = "5"
                st.markdown('<p style="color: #0084ff;">Fast assessment - 2 questions per dimension</p>', 
                           unsafe_allow_html=True)
        
        with col3:
            if st.button("📋 Standard\n7 minutes", key="time_7", use_container_width=True):
                time_choice = "7"
                st.markdown('<p style="color: #0084ff;">Standard assessment - 3 questions per dimension</p>', 
                           unsafe_allow_html=True)
        
        with col4:
            if st.button("📊 Detailed\n15 minutes", key="time_15", use_container_width=True):
                time_choice = "15"
                st.markdown('<p style="color: #0084ff;">Detailed assessment - 5 questions per dimension</p>', 
                           unsafe_allow_html=True)
        
        with col5:
            if st.button("🎯 Complete\n15+ minutes", key="time_15plus", use_container_width=True):
                time_choice = "15+"
                st.markdown('<p style="color: #0084ff;">Complete assessment - Full comprehensive analysis</p>', 
                           unsafe_allow_html=True)
        
        if time_choice:
            st.session_state.time_preference = time_choice
            st.session_state.assessment_config = self.time_options[time_choice]
            return time_choice
            
        return None
    
    def render_checkbox_question(self, question_data: Dict[str, Any], agent_type: str, question_index: int) -> Optional[List[str]]:
        """Render a checkbox-based question"""
        
        question_key = f"{agent_type}_q{question_index}"
        
        st.markdown(f"""
        <div style="background: #3a3a3a; padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid #505050;">
            <h4 style="color: #ffffff; margin-bottom: 15px;">
                🎯 {question_data['question']}
            </h4>
            <p style="color: #cccccc; font-size: 14px; margin-bottom: 20px;">
                💡 {question_data.get('description', 'Select all options that apply to you')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create checkboxes for each option
        selected_options = []
        
        for i, option in enumerate(question_data['options']):
            checkbox_key = f"{question_key}_option_{i}"
            
            if st.checkbox(
                option['text'], 
                key=checkbox_key,
                help=option.get('description', '')
            ):
                selected_options.append(option['value'])
        
        # Add a submit button for this question
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"✅ Submit Answer", key=f"{question_key}_submit", use_container_width=True):
                if selected_options:
                    return selected_options
                else:
                    st.error("Please select at least one option before submitting.")
                    return None
        
        return None
    
    def create_sample_questions(self, agent_type: str, question_count: int) -> List[Dict[str, Any]]:
        """Create sample questions for each agent type"""
        
        questions_bank = {
            "interests": [
                {
                    "question": "Which activities energize and excite you the most?",
                    "description": "Think about what you love doing in your free time",
                    "options": [
                        {"text": "🎨 Creative activities (art, writing, design)", "value": "creative"},
                        {"text": "💻 Technology and coding", "value": "technology"},
                        {"text": "🤝 Working with people and teams", "value": "people"},
                        {"text": "📊 Analyzing data and solving problems", "value": "analytical"},
                        {"text": "🌍 Helping others and making a difference", "value": "helping"},
                        {"text": "🏢 Business and entrepreneurship", "value": "business"},
                        {"text": "🔬 Research and learning new things", "value": "research"},
                        {"text": "🎯 Leading and managing projects", "value": "leadership"}
                    ]
                },
                {
                    "question": "What type of content do you enjoy consuming the most?",
                    "description": "Consider what you read, watch, or listen to regularly",
                    "options": [
                        {"text": "📚 Educational content and tutorials", "value": "educational"},
                        {"text": "📰 News and current events", "value": "news"},
                        {"text": "🎬 Entertainment and stories", "value": "entertainment"},
                        {"text": "💡 Innovation and technology trends", "value": "tech_trends"},
                        {"text": "💰 Business and finance", "value": "finance"},
                        {"text": "🏥 Health and wellness", "value": "health"},
                        {"text": "🌱 Environmental and social issues", "value": "social"},
                        {"text": "🎵 Arts and culture", "value": "arts"}
                    ]
                },
                {
                    "question": "In your ideal work environment, what would you be doing?",
                    "description": "Imagine your perfect workday activities",
                    "options": [
                        {"text": "💡 Brainstorming creative solutions", "value": "creative_solving"},
                        {"text": "📈 Analyzing trends and patterns", "value": "analysis"},
                        {"text": "👥 Collaborating with diverse teams", "value": "collaboration"},
                        {"text": "🎓 Teaching or mentoring others", "value": "teaching"},
                        {"text": "🔧 Building or creating products", "value": "building"},
                        {"text": "📞 Communicating with clients/customers", "value": "client_work"},
                        {"text": "🔍 Researching and experimenting", "value": "research_exp"},
                        {"text": "📋 Planning and organizing projects", "value": "planning"}
                    ]
                }
            ],
            "skills": [
                {
                    "question": "Which skills do you feel most confident using?",
                    "description": "Select skills you're good at or enjoy developing",
                    "options": [
                        {"text": "💬 Communication and presentation", "value": "communication"},
                        {"text": "🧮 Mathematical and analytical thinking", "value": "analytical"},
                        {"text": "💻 Technical and computer skills", "value": "technical"},
                        {"text": "🎨 Creative and design abilities", "value": "creative"},
                        {"text": "🤝 Leadership and team management", "value": "leadership"},
                        {"text": "📊 Data analysis and interpretation", "value": "data"},
                        {"text": "🔧 Problem-solving and troubleshooting", "value": "problem_solving"},
                        {"text": "📝 Writing and documentation", "value": "writing"}
                    ]
                },
                {
                    "question": "What type of skills would you like to develop further?",
                    "description": "Think about areas you want to grow in",
                    "options": [
                        {"text": "🚀 Project management", "value": "project_management"},
                        {"text": "💼 Business strategy", "value": "business_strategy"},
                        {"text": "🤖 Artificial Intelligence/ML", "value": "ai_ml"},
                        {"text": "🎯 Digital marketing", "value": "marketing"},
                        {"text": "💰 Financial analysis", "value": "finance"},
                        {"text": "🌐 Web development", "value": "web_dev"},
                        {"text": "📱 Mobile app development", "value": "mobile_dev"},
                        {"text": "🎤 Public speaking", "value": "public_speaking"}
                    ]
                }
            ],
            "personality": [
                {
                    "question": "How do you prefer to work and interact with others?",
                    "description": "Choose your natural working style preferences",
                    "options": [
                        {"text": "👥 I thrive in team environments", "value": "team_player"},
                        {"text": "🧘 I work best independently", "value": "independent"},
                        {"text": "🎯 I like to lead and guide others", "value": "leader"},
                        {"text": "📚 I prefer to support and assist", "value": "supporter"},
                        {"text": "💡 I enjoy brainstorming with others", "value": "collaborative"},
                        {"text": "🔍 I like to work behind the scenes", "value": "behind_scenes"},
                        {"text": "🎤 I'm comfortable being the spokesperson", "value": "spokesperson"},
                        {"text": "⚖️ I prefer to mediate and balance", "value": "mediator"}
                    ]
                },
                {
                    "question": "How do you handle challenges and stress?",
                    "description": "Select your typical responses to difficult situations",
                    "options": [
                        {"text": "🧘 I stay calm and think through solutions", "value": "calm_thinker"},
                        {"text": "⚡ I act quickly and decisively", "value": "quick_action"},
                        {"text": "🤝 I seek advice and input from others", "value": "seek_advice"},
                        {"text": "📊 I research and analyze options thoroughly", "value": "thorough_analysis"},
                        {"text": "💡 I get creative and think outside the box", "value": "creative_solutions"},
                        {"text": "🎯 I break problems into smaller parts", "value": "systematic"},
                        {"text": "🔄 I learn from failures and adapt", "value": "adaptive"},
                        {"text": "💪 I push through with determination", "value": "determined"}
                    ]
                }
            ],
            
            "aspirations": [
                {
                    "question": "What are your long-term career aspirations?",
                    "description": "Think about where you want to be in 5-10 years",
                    "options": [
                        {"text": "🎯 Leading a team or organization", "value": "leadership"},
                        {"text": "🔬 Becoming an expert in my field", "value": "expertise"},
                        {"text": "💰 Achieving financial independence", "value": "financial"},
                        {"text": "🌍 Making a positive impact on society", "value": "social_impact"},
                        {"text": "🚀 Starting my own business", "value": "entrepreneurship"},
                        {"text": "📚 Continuous learning and growth", "value": "learning"},
                        {"text": "⚖️ Achieving work-life balance", "value": "balance"},
                        {"text": "🏆 Recognition and awards in my field", "value": "recognition"}
                    ]
                },
                {
                    "question": "What type of legacy do you want to leave?",
                    "description": "Consider the impact you want to have on the world",
                    "options": [
                        {"text": "🌱 Environmental sustainability", "value": "environmental"},
                        {"text": "📖 Educational advancement", "value": "education"},
                        {"text": "🏥 Health and wellness improvements", "value": "health"},
                        {"text": "💡 Technological innovation", "value": "technology"},
                        {"text": "🤝 Community development", "value": "community"},
                        {"text": "🎨 Creative and cultural contributions", "value": "cultural"},
                        {"text": "⚖️ Social justice and equality", "value": "justice"},
                        {"text": "👨‍👩‍👧‍👦 Family and personal relationships", "value": "family"}
                    ]
                }
            ],
            
            "motivations_values": [
                {
                    "question": "What motivates you most in your work?",
                    "description": "Select what drives you to do your best",
                    "options": [
                        {"text": "🏆 Achievement and recognition", "value": "achievement"},
                        {"text": "🤝 Helping others succeed", "value": "helping"},
                        {"text": "💡 Creating something new", "value": "innovation"},
                        {"text": "📈 Continuous improvement", "value": "growth"},
                        {"text": "🎯 Solving complex problems", "value": "problem_solving"},
                        {"text": "💰 Financial rewards", "value": "financial"},
                        {"text": "🌍 Making a difference", "value": "impact"},
                        {"text": "🔒 Job security and stability", "value": "security"}
                    ]
                },
                {
                    "question": "What values are most important to you?",
                    "description": "Choose the principles that guide your decisions",
                    "options": [
                        {"text": "🎯 Honesty and integrity", "value": "integrity"},
                        {"text": "🤝 Respect and fairness", "value": "respect"},
                        {"text": "💪 Excellence and quality", "value": "excellence"},
                        {"text": "🌟 Innovation and creativity", "value": "creativity"},
                        {"text": "👥 Collaboration and teamwork", "value": "teamwork"},
                        {"text": "⚖️ Work-life balance", "value": "balance"},
                        {"text": "🌍 Social responsibility", "value": "responsibility"},
                        {"text": "📚 Learning and development", "value": "development"}
                    ]
                }
            ],
            
            "cognitive_abilities": [
                {
                    "question": "How do you prefer to process information?",
                    "description": "Think about your natural thinking style",
                    "options": [
                        {"text": "📊 I like data and detailed analysis", "value": "analytical"},
                        {"text": "🎨 I think visually and creatively", "value": "visual"},
                        {"text": "🗣️ I process through discussion", "value": "verbal"},
                        {"text": "⚡ I make quick intuitive decisions", "value": "intuitive"},
                        {"text": "📝 I need to write things down", "value": "written"},
                        {"text": "🔄 I like step-by-step processes", "value": "sequential"},
                        {"text": "🎯 I see the big picture first", "value": "holistic"},
                        {"text": "🤔 I need time to reflect", "value": "reflective"}
                    ]
                },
                {
                    "question": "What type of mental challenges energize you?",
                    "description": "Select the thinking activities you enjoy most",
                    "options": [
                        {"text": "🧩 Solving complex puzzles", "value": "puzzles"},
                        {"text": "💡 Brainstorming new ideas", "value": "ideation"},
                        {"text": "📊 Analyzing patterns in data", "value": "pattern_analysis"},
                        {"text": "🎭 Understanding people's motivations", "value": "psychology"},
                        {"text": "🔧 Figuring out how things work", "value": "mechanics"},
                        {"text": "📈 Planning and strategizing", "value": "strategy"},
                        {"text": "🎨 Creating original concepts", "value": "creativity"},
                        {"text": "⚖️ Making fair decisions", "value": "judgment"}
                    ]
                }
            ],
            
            "strengths_weaknesses": [
                {
                    "question": "What are your key strengths?",
                    "description": "Select the areas where you consistently excel",
                    "options": [
                        {"text": "💬 Communication and presentation", "value": "communication"},
                        {"text": "🎯 Problem-solving abilities", "value": "problem_solving"},
                        {"text": "👥 Leadership and influence", "value": "leadership"},
                        {"text": "📊 Analytical thinking", "value": "analytical"},
                        {"text": "🎨 Creativity and innovation", "value": "creativity"},
                        {"text": "⏰ Time management", "value": "time_management"},
                        {"text": "🤝 Relationship building", "value": "relationships"},
                        {"text": "📈 Learning quickly", "value": "learning"}
                    ]
                },
                {
                    "question": "What areas would you like to develop?",
                    "description": "Choose skills you want to improve",
                    "options": [
                        {"text": "🎤 Public speaking confidence", "value": "public_speaking"},
                        {"text": "💻 Technical skills", "value": "technical"},
                        {"text": "📈 Strategic thinking", "value": "strategic"},
                        {"text": "🤝 Delegation abilities", "value": "delegation"},
                        {"text": "⚖️ Decision-making speed", "value": "decisions"},
                        {"text": "📊 Data analysis skills", "value": "data_analysis"},
                        {"text": "🌐 Cultural awareness", "value": "cultural"},
                        {"text": "💪 Stress management", "value": "stress"}
                    ]
                }
            ],
            
            "learning_preferences": [
                {
                    "question": "How do you learn best?",
                    "description": "Select your most effective learning methods",
                    "options": [
                        {"text": "👀 Visual aids and diagrams", "value": "visual"},
                        {"text": "👂 Listening to explanations", "value": "auditory"},
                        {"text": "✋ Hands-on practice", "value": "kinesthetic"},
                        {"text": "📚 Reading and research", "value": "reading"},
                        {"text": "👥 Group discussions", "value": "collaborative"},
                        {"text": "🧘 Individual reflection", "value": "solitary"},
                        {"text": "🎮 Interactive simulations", "value": "interactive"},
                        {"text": "📝 Taking detailed notes", "value": "note_taking"}
                    ]
                },
                {
                    "question": "What learning environment suits you best?",
                    "description": "Consider where you focus and absorb information most effectively",
                    "options": [
                        {"text": "🏫 Structured classroom setting", "value": "structured"},
                        {"text": "💻 Online and flexible", "value": "online"},
                        {"text": "🤝 Mentorship and coaching", "value": "mentorship"},
                        {"text": "🏢 On-the-job training", "value": "practical"},
                        {"text": "📚 Self-directed study", "value": "self_directed"},
                        {"text": "👥 Peer learning groups", "value": "peer"},
                        {"text": "🎯 Project-based learning", "value": "project"},
                        {"text": "🔄 Trial and error", "value": "experiential"}
                    ]
                }
            ],
            
            "track_record": [
                {
                    "question": "What types of achievements are you most proud of?",
                    "description": "Reflect on your past successes and accomplishments",
                    "options": [
                        {"text": "🎓 Academic excellence", "value": "academic"},
                        {"text": "🏆 Competition victories", "value": "competitive"},
                        {"text": "👥 Team leadership success", "value": "leadership"},
                        {"text": "💡 Creative projects", "value": "creative"},
                        {"text": "🤝 Community service", "value": "service"},
                        {"text": "💼 Professional recognition", "value": "professional"},
                        {"text": "🛠️ Technical accomplishments", "value": "technical"},
                        {"text": "📈 Personal growth milestones", "value": "personal"}
                    ]
                },
                {
                    "question": "In what areas have you shown consistent progress?",
                    "description": "Think about skills or abilities you've steadily improved",
                    "options": [
                        {"text": "💬 Communication skills", "value": "communication"},
                        {"text": "👥 Leadership abilities", "value": "leadership"},
                        {"text": "🔧 Technical expertise", "value": "technical"},
                        {"text": "🎨 Creative abilities", "value": "creative"},
                        {"text": "📊 Analytical skills", "value": "analytical"},
                        {"text": "🤝 Interpersonal relationships", "value": "interpersonal"},
                        {"text": "📈 Strategic thinking", "value": "strategic"},
                        {"text": "💪 Physical capabilities", "value": "physical"}
                    ]
                }
            ],
            
            "emotional_intelligence": [
                {
                    "question": "How do you typically handle emotions in professional settings?",
                    "description": "Consider your emotional awareness and management",
                    "options": [
                        {"text": "😌 I stay calm under pressure", "value": "calm"},
                        {"text": "🎯 I can read others' emotions well", "value": "empathetic"},
                        {"text": "💬 I communicate feelings clearly", "value": "expressive"},
                        {"text": "🤝 I help others manage their emotions", "value": "supportive"},
                        {"text": "⚖️ I maintain emotional balance", "value": "balanced"},
                        {"text": "🔄 I adapt to others' emotional needs", "value": "adaptive"},
                        {"text": "💪 I motivate and inspire others", "value": "motivating"},
                        {"text": "🧘 I practice self-reflection", "value": "self_aware"}
                    ]
                },
                {
                    "question": "How do you build relationships with colleagues?",
                    "description": "Select your approach to workplace relationships",
                    "options": [
                        {"text": "👂 I listen actively and attentively", "value": "listening"},
                        {"text": "🤝 I build trust through reliability", "value": "trustworthy"},
                        {"text": "💬 I communicate openly and honestly", "value": "open"},
                        {"text": "🎯 I show genuine interest in others", "value": "interested"},
                        {"text": "⚖️ I respect different perspectives", "value": "respectful"},
                        {"text": "🤗 I offer help and support", "value": "helpful"},
                        {"text": "😊 I maintain positive energy", "value": "positive"},
                        {"text": "🔄 I give constructive feedback", "value": "constructive"}
                    ]
                }
            ],
            
            "constraints": [
                {
                    "question": "What practical constraints influence your career decisions?",
                    "description": "Consider the real-world factors that affect your choices",
                    "options": [
                        {"text": "📍 Geographic location preferences", "value": "location"},
                        {"text": "⏰ Work schedule flexibility needs", "value": "schedule"},
                        {"text": "💰 Financial requirements", "value": "financial"},
                        {"text": "👨‍👩‍👧‍👦 Family responsibilities", "value": "family"},
                        {"text": "🎓 Education or certification needs", "value": "education"},
                        {"text": "🏥 Health considerations", "value": "health"},
                        {"text": "✈️ Travel limitations", "value": "travel"},
                        {"text": "🏡 Remote work preferences", "value": "remote"}
                    ]
                },
                {
                    "question": "What would make you turn down a job opportunity?",
                    "description": "Identify your non-negotiable factors",
                    "options": [
                        {"text": "🕐 Poor work-life balance", "value": "work_life_balance"},
                        {"text": "💰 Inadequate compensation", "value": "compensation"},
                        {"text": "🌍 Company values don't align", "value": "values"},
                        {"text": "📈 Limited growth opportunities", "value": "growth"},
                        {"text": "🏢 Toxic work culture", "value": "culture"},
                        {"text": "🚗 Long commute required", "value": "commute"},
                        {"text": "📚 Insufficient learning opportunities", "value": "learning"},
                        {"text": "👥 Poor team dynamics", "value": "team"}
                    ]
                }
            ],
            
            "physical_context": [
                {
                    "question": "What type of work environment do you thrive in?",
                    "description": "Consider the physical settings where you work best",
                    "options": [
                        {"text": "🏢 Traditional office setting", "value": "office"},
                        {"text": "🏡 Remote/home office", "value": "remote"},
                        {"text": "🌐 Co-working spaces", "value": "coworking"},
                        {"text": "🏭 Industrial/workshop environment", "value": "industrial"},
                        {"text": "🌳 Outdoor settings", "value": "outdoor"},
                        {"text": "🏥 Clinical/laboratory setting", "value": "clinical"},
                        {"text": "🎪 Dynamic/event-based locations", "value": "dynamic"},
                        {"text": "✈️ Travel and varied locations", "value": "travel"}
                    ]
                },
                {
                    "question": "What physical work style suits you best?",
                    "description": "Think about how you prefer to engage physically with work",
                    "options": [
                        {"text": "💻 Primarily computer-based work", "value": "computer"},
                        {"text": "🤝 Face-to-face interactions", "value": "interpersonal"},
                        {"text": "✋ Hands-on and manual tasks", "value": "manual"},
                        {"text": "🚶 Active and mobile work", "value": "active"},
                        {"text": "🧘 Quiet and contemplative", "value": "quiet"},
                        {"text": "🎤 Presenting and speaking", "value": "presenting"},
                        {"text": "🔬 Detailed and precise work", "value": "precise"},
                        {"text": "🎨 Creative and expressive", "value": "creative"}
                    ]
                }
            ]
        }
        
        # Return the specified number of questions for the agent type
        agent_questions = questions_bank.get(agent_type, [])
        return agent_questions[:question_count] if agent_questions else []

def render_assessment_progress(current_agent: int, total_agents: int, time_remaining: int):
    """Render assessment progress bar with time tracking"""
    
    progress_percentage = (current_agent / total_agents) * 100
    
    st.markdown(f"""
    <div style="background: #3a3a3a; padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #505050;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="color: #ffffff; margin: 0;">Assessment Progress</h4>
            <span style="color: #0084ff; font-weight: 600;">⏰ {time_remaining} min remaining</span>
        </div>
        <div style="background: #1a1a1a; border-radius: 10px; height: 20px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #0084ff, #00ff84); height: 100%; width: {progress_percentage}%; transition: width 0.3s ease;"></div>
        </div>
        <p style="color: #cccccc; margin: 10px 0 0 0; font-size: 14px;">
            Dimension {current_agent} of {total_agents} • {progress_percentage:.0f}% complete
        </p>
    </div>
    """, unsafe_allow_html=True)