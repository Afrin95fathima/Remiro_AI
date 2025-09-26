"""
Enhanced Remiro AI Career Assistant - Main Application

Advanced, personalized career assistance platform with:
- 12D empathetic assessment agents
- ChatGPT-like conversational AI
- Comprehensive career analysis & roadmaps
- Professional, interactive UI
"""

import streamlit as st
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
from datetime import datetime
import uuid

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import enhanced components
try:
    from ui.enhanced_components import (
        apply_custom_css, render_header, render_chat_interface,
        render_assessment_progress, render_career_analysis,
        render_conversation_suggestions, render_sidebar_info,
        render_input_area, create_progress_chart
    )
    from ui.interactive_questions import InteractiveQuestionSystem, render_assessment_progress
    from ui.agent_integration import AgentIntegrationSystem
    from core.local_storage import LocalDataManager, local_data_manager
except ImportError:
    try:
        from ui.simple_components import (
            apply_custom_css, render_header, render_chat_interface,
            render_assessment_progress, render_career_analysis,
            render_conversation_suggestions, render_sidebar_info,
            render_input_area, create_progress_chart
        )
        st.info("Using simplified UI components.")
    except ImportError as e:
        st.error(f"UI components not available: {e}")
        st.stop()

try:
    from agents.advanced_master_agent import AdvancedMasterAgent
    MASTER_AGENT_CLASS = AdvancedMasterAgent
except ImportError:
    try:
        from agents.simple_master_agent import SimpleMasterAgent
        MASTER_AGENT_CLASS = SimpleMasterAgent
        st.warning("Using simplified master agent. Some advanced features may not be available.")
    except ImportError as e:
        st.error(f"No master agent available: {e}")
        st.stop()

# Skip enhanced state models for now to avoid compatibility issues
ENHANCED_MODELS_AVAILABLE = False
print("Using simple state management for compatibility")

# Configure Streamlit
st.set_page_config(
    page_title="Remiro AI Career Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_llm():
    """Initialize the language model"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Get API key from multiple sources
        api_key = None
        
        # Try environment variable first
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # Try Streamlit secrets if environment variable not found
        if not api_key:
            try:
                api_key = st.secrets.get("GOOGLE_API_KEY")
            except Exception:
                pass  # Secrets file might not exist
        
        # Check if API key is placeholder or empty
        if not api_key or api_key == "YOUR_GOOGLE_API_KEY_HERE":
            st.error("🔑 **Google API Key Required**")
            st.markdown("""
            To use Remiro AI, you need a Google Gemini API key. Here's how to set it up:
            
            **Option 1: Using Streamlit Secrets (Recommended)**
            1. Edit the file: `.streamlit/secrets.toml`
            2. Replace `YOUR_GOOGLE_API_KEY_HERE` with your actual API key
            
            **Option 2: Using Environment Variable**
            1. Set environment variable: `GOOGLE_API_KEY=your_api_key_here`
            
            **How to get your API key:**
            1. Visit: https://ai.google.dev/
            2. Create a new API key for Gemini API
            3. Copy and paste it in the secrets.toml file
            """)
            st.stop()
        
        # Initialize with Gemini 1.5 Flash
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        return llm
    
    except ImportError:
        st.error("⚠️ Please install required dependencies: pip install langchain-google-genai")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error initializing AI model: {str(e)}")
        st.stop()

def initialize_session_state():
    """Initialize Streamlit session state"""
    
    # Initialize session ID and user ID
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = "default_user"
    
    # Initialize user onboarding state
    if 'user_onboarded' not in st.session_state:
        st.session_state.user_onboarded = False
        
    if 'user_details' not in st.session_state:
        st.session_state.user_details = {}
    
    # Initialize conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Initialize master agent
    if 'master_agent' not in st.session_state:
        llm = initialize_llm()
        st.session_state.master_agent = MASTER_AGENT_CLASS(llm)
    
    # Initialize agent integration system
    if 'agent_integration_system' not in st.session_state:
        llm = initialize_llm()
        st.session_state.agent_integration_system = AgentIntegrationSystem(llm)
    
    # Initialize assessment progress
    if 'assessment_progress' not in st.session_state:
        st.session_state.assessment_progress = {}
    
    # Initialize career analysis
    if 'career_analysis' not in st.session_state:
        st.session_state.career_analysis = None
    
    # Initialize UI state
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False
    
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "chat"
    
    # Interactive assessment system
    if 'question_system' not in st.session_state:
        st.session_state.question_system = InteractiveQuestionSystem()
    
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = local_data_manager
    
    # Time-based assessment
    if 'time_preference' not in st.session_state:
        st.session_state.time_preference = None
    
    if 'assessment_config' not in st.session_state:
        st.session_state.assessment_config = None
    
    # Assessment state tracking
    if 'assessment_mode' not in st.session_state:
        st.session_state.assessment_mode = "chat"  # "chat", "time_selection", "questions", "completed"
    
    if 'current_agent_index' not in st.session_state:
        st.session_state.current_agent_index = 0
    
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    
    if 'assessment_start_time' not in st.session_state:
        st.session_state.assessment_start_time = None

def save_conversation(user_input: str, assistant_response: str):
    """Save conversation to session state"""
    
    st.session_state.conversation_history.append({
        'user': user_input,
        'timestamp': datetime.now().isoformat()
    })
    
    st.session_state.conversation_history.append({
        'assistant': assistant_response,
        'timestamp': datetime.now().isoformat()
    })

def process_user_input(user_input: str) -> Dict[str, Any]:
    """Process user input through the master agent"""
    
    try:
        master_agent = st.session_state.master_agent
        response = master_agent.process_conversation(user_input, st.session_state.user_id)
        
        # Update assessment progress
        if hasattr(master_agent, 'assessment_progress'):
            st.session_state.assessment_progress = master_agent.assessment_progress
        
        # Check if assessment is complete
        if response.get('type') == 'assessment_complete':
            st.session_state.career_analysis = response.get('analysis')
            st.session_state.show_analysis = True
        
        return response
    
    except Exception as e:
        st.error(f"Error processing input: {str(e)}")
        return {
            "type": "error_response",
            "message": "I'm having some technical difficulties. Let me try to help you in a different way. What's on your mind?",
            "error": str(e)
        }

def render_user_onboarding():
    """Render user details collection form"""
    
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1 style="color: #FF6B6B; font-size: 3rem; margin-bottom: 10px;">
            🎯 Welcome to Remiro AI!
        </h1>
        <h3 style="color: #4ECDC4; font-size: 1.5rem; margin-bottom: 30px;">
            Your Advanced AI-Powered Career Counselor & 12D Assessment Platform
        </h3>
        <p style="color: #45B7D1; font-size: 1.2rem; margin-bottom: 40px;">
            Let's get to know you better to provide personalized career guidance!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(145deg, #667eea 0%, #764ba2 100%); 
                        padding: 30px; 
                        border-radius: 20px; 
                        box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: white; text-align: center; margin-bottom: 25px;'>Tell us about yourself! 📝</h3>", unsafe_allow_html=True)
            
            # User details form
            name = st.text_input("👤 What's your name?", placeholder="Enter your full name", key="user_name")
            age = st.number_input("🎂 How old are you?", min_value=16, max_value=100, value=25, key="user_age")
            location = st.text_input("🌍 Where are you located?", placeholder="City, Country", key="user_location")
            
            education = st.selectbox(
                "🎓 What's your highest education level?",
                ["High School", "Bachelor's Degree", "Master's Degree", "PhD/Doctorate", "Professional Certification", "Other"],
                key="user_education"
            )
            
            current_status = st.selectbox(
                "💼 What's your current status?",
                ["Student", "Employed Full-time", "Employed Part-time", "Unemployed", "Freelancer", "Entrepreneur", "Career Break"],
                key="user_status"
            )
            
            career_stage = st.selectbox(
                "🚀 What stage are you at in your career?",
                ["Just Starting", "Early Career (0-3 years)", "Mid Career (3-8 years)", "Senior Level (8+ years)", "Executive Level", "Career Change"],
                key="user_career_stage"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Submit button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🚀 Let's Start My Career Journey!", 
                           key="start_journey", 
                           type="primary",
                           use_container_width=True):
                    
                    if name and len(name.strip()) > 0:
                        # Save user details
                        st.session_state.user_details = {
                            'name': name.strip(),
                            'age': age,
                            'location': location.strip(),
                            'education': education,
                            'current_status': current_status,
                            'career_stage': career_stage
                        }
                        
                        # Generate user ID based on name
                        import hashlib
                        user_id_hash = hashlib.md5(name.lower().encode()).hexdigest()[:8]
                        st.session_state.user_id = f"{name.lower().replace(' ', '_')}_{user_id_hash}"
                        
                        # Mark as onboarded
                        st.session_state.user_onboarded = True
                        
                        st.success(f"Welcome aboard, {name}! 🎉")
                        st.rerun()
                    else:
                        st.error("Please enter your name to continue! 📝")

def render_interactive_assessment_view():
    """Render the new interactive assessment with checkboxes and time-based questions"""
    
    # Header for assessment
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #505050; margin-bottom: 20px; background: #2d2d2d;">
        <h2 style="color: #ffffff; margin: 0; font-weight: 600;">🎯 Interactive Career Assessment</h2>
        <p style="color: #cccccc; margin: 5px 0 0 0;">Checkbox-based questions with time customization</p>
        <p style="color: #0084ff; margin: 8px 0 0 0; font-size: 14px;">Choose your answers and let us guide your career path</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Time selection phase
    if st.session_state.assessment_mode == "time_selection":
        st.markdown("### ⏰ Choose Your Assessment Duration")
        
        time_choice = st.session_state.question_system.render_time_selection()
        
        if time_choice:
            # Save assessment config
            config_data = {
                "time_preference": time_choice,
                "assessment_config": st.session_state.assessment_config,
                "start_timestamp": datetime.now().isoformat()
            }
            
            st.session_state.data_manager.save_assessment_config(st.session_state.user_id, config_data)
            
            # Move to questions phase
            st.session_state.assessment_mode = "questions"
            st.session_state.assessment_start_time = datetime.now()
            
            # Initialize assessment tracking variables
            st.session_state.current_agent_index = 0
            st.session_state.current_question_index = 0
            
            st.rerun()
    
    # Questions phase
    elif st.session_state.assessment_mode == "questions":
        agent_types = ['interests', 'skills', 'personality', 'aspirations', 
                      'motivations_values', 'cognitive_abilities', 'strengths_weaknesses',
                      'learning_preferences', 'track_record', 'emotional_intelligence',
                      'constraints', 'physical_context']
        
        # Initialize assessment variables if not present or out of bounds
        if 'current_agent_index' not in st.session_state:
            st.session_state.current_agent_index = 0
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        if 'assessment_config' not in st.session_state or st.session_state.assessment_config is None:
            # Fallback to default config
            st.session_state.assessment_config = {"minutes": 7, "questions_per_agent": 3, "total_questions": 36}
        
        # Bounds checking for agent index
        if st.session_state.current_agent_index >= len(agent_types):
            st.session_state.assessment_mode = "completed"
            st.rerun()
            return
        
        current_agent = agent_types[st.session_state.current_agent_index]
        questions_per_agent = st.session_state.assessment_config.get('questions_per_agent', 3)
        
        # Calculate time remaining
        if st.session_state.assessment_start_time:
            elapsed_minutes = (datetime.now() - st.session_state.assessment_start_time).total_seconds() / 60
            time_remaining = max(0, st.session_state.assessment_config['minutes'] - elapsed_minutes)
        else:
            time_remaining = st.session_state.assessment_config['minutes']
        
        # Render progress
        render_assessment_progress(
            st.session_state.current_agent_index + 1, 
            len(agent_types), 
            int(time_remaining)
        )
        
        # Get questions for current agent
        questions = st.session_state.question_system.create_sample_questions(
            current_agent, 
            questions_per_agent
        )
        
        if st.session_state.current_question_index < len(questions):
            # Current question
            current_question = questions[st.session_state.current_question_index]
            
            st.markdown(f"### 📋 {current_agent.replace('_', ' ').title()} Assessment")
            st.markdown(f"**Question {st.session_state.current_question_index + 1} of {len(questions)}**")
            
            # Render the checkbox question
            selected_answers = st.session_state.question_system.render_checkbox_question(
                current_question, 
                current_agent, 
                st.session_state.current_question_index
            )
            
            if selected_answers is not None:
                # Save the response
                st.session_state.data_manager.save_question_response(
                    st.session_state.user_id,
                    current_agent,
                    st.session_state.current_question_index,
                    current_question,
                    selected_answers
                )
                
                # Get AI agent response to user's selections
                with st.spinner("🤖 Getting personalized feedback..."):
                    try:
                        user_profile = st.session_state.data_manager.load_user_profile(st.session_state.user_id)
                        agent_response = st.session_state.agent_integration_system.get_agent_response(
                            current_agent, 
                            selected_answers, 
                            user_profile
                        )
                        
                        # Display the agent's response
                        st.session_state.agent_integration_system.render_agent_response(
                            current_agent, 
                            agent_response
                        )
                        
                        # Save agent response for future reference
                        st.session_state.data_manager.save_agent_feedback(
                            st.session_state.user_id,
                            current_agent,
                            st.session_state.current_question_index,
                            agent_response
                        )
                        
                    except Exception as e:
                        st.error(f"Error getting agent feedback: {e}")
                        st.info("Your response has been saved and will be used for your final career analysis.")
                
                # Move to next question
                st.session_state.current_question_index += 1
                
                # Check if agent is complete
                if st.session_state.current_question_index >= len(questions):
                    # Agent completed - show summary
                    st.markdown("---")
                    st.success(f"✅ {current_agent.replace('_', ' ').title()} assessment completed!")
                    
                    # Move to next agent
                    st.session_state.current_agent_index += 1
                    st.session_state.current_question_index = 0
                    
                    # Check if assessment is complete
                    if st.session_state.current_agent_index >= len(agent_types):
                        st.session_state.assessment_mode = "completed"
                    else:
                        # Show next agent preview
                        next_agent = agent_types[st.session_state.current_agent_index]
                        st.info(f"🔄 Moving to next assessment: {next_agent.replace('_', ' ').title()}")
                        
                        # Add continue button
                        if st.button("Continue to Next Assessment →", key="continue_next_agent"):
                            st.rerun()
                
                st.rerun()
        
        else:
            # This shouldn't happen, but handle gracefully
            st.session_state.current_agent_index += 1
            st.session_state.current_question_index = 0
            st.rerun()
    
    # Completed phase
    elif st.session_state.assessment_mode == "completed":
        render_assessment_completion_view()

def render_assessment_completion_view():
    """Render the assessment completion and results view"""
    
    st.markdown("""
    <div style="text-align: center; padding: 30px; background: #3a3a3a; border-radius: 12px; margin: 20px 0;">
        <h2 style="color: #00ff84; margin-bottom: 15px;">🎉 Assessment Complete!</h2>
        <p style="color: #ffffff; font-size: 18px; margin-bottom: 20px;">
            Thank you for completing your career assessment!
        </p>
        <p style="color: #cccccc; margin-bottom: 25px;">
            We're now analyzing your responses to provide personalized career recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate analysis based on collected responses
    if st.button("📊 Generate My Career Analysis", key="generate_analysis", use_container_width=True):
        with st.spinner("🤖 Analyzing your responses..."):
            # Collect all responses
            all_responses = {}
            agent_types = ['interests', 'skills', 'personality', 'aspirations', 
                          'motivations_values', 'cognitive_abilities', 'strengths_weaknesses',
                          'learning_preferences', 'track_record', 'emotional_intelligence',
                          'constraints', 'physical_context']
            
            for agent_type in agent_types:
                responses = st.session_state.data_manager.load_agent_responses(
                    st.session_state.user_id, agent_type
                )
                all_responses[agent_type] = responses
            
            # Generate comprehensive career analysis using all agents
            with st.spinner("🤖 All 12 agents are analyzing your responses..."):
                career_analysis = st.session_state.agent_integration_system.get_comprehensive_analysis(all_responses)
            
            # Save the analysis
            summary_data = {
                "assessment_type": "interactive_checkbox",
                "time_preference": st.session_state.time_preference,
                "total_responses": sum(len(responses) for responses in all_responses.values()),
                "career_analysis": career_analysis,
                "all_responses": all_responses
            }
            
            st.session_state.data_manager.save_assessment_summary(st.session_state.user_id, summary_data)
            
            # Display results
            display_career_analysis_results(career_analysis)
    
    # Option to take full assessment
    if st.session_state.time_preference in ["3", "5", "7"]:
        st.markdown("---")
        st.markdown("### 🚀 Want More Personalized Guidance?")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: #2d4a4a; padding: 20px; border-radius: 8px; border: 1px solid #0084ff;">
                <h4 style="color: #00ff84;">Take the Full Assessment</h4>
                <p style="color: #cccccc; font-size: 14px;">
                    Get more detailed insights with our comprehensive 15+ minute assessment
                    including deeper questions and advanced career matching.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎯 Start Full Assessment", key="full_assessment"):
                st.session_state.assessment_mode = "time_selection"
                st.session_state.current_agent_index = 0
                st.session_state.current_question_index = 0
                st.rerun()
        
        with col2:
            st.markdown("""
            <div style="background: #4a2d4a; padding: 20px; border-radius: 8px; border: 1px solid #ff6b6b;">
                <h4 style="color: #ff6b6b;">Current Results</h4>
                <p style="color: #cccccc; font-size: 14px;">
                    Your current assessment provides good insights, but a longer assessment
                    would give you more precise career recommendations.
                </p>
            </div>
            """, unsafe_allow_html=True)

def generate_career_analysis_from_responses(all_responses: Dict) -> Dict[str, Any]:
    """Generate career analysis from checkbox responses"""
    
    # Simple analysis based on most selected options
    interests = []
    skills = []
    personality_traits = []
    
    # Extract top selections from each category
    for agent_type, responses in all_responses.items():
        for response in responses:
            selected_options = response.get('options_selected', [])
            
            if agent_type == 'interests':
                interests.extend(selected_options)
            elif agent_type == 'skills':
                skills.extend(selected_options)
            elif agent_type == 'personality':
                personality_traits.extend(selected_options)
    
    # Create basic career suggestions based on combinations
    career_matches = create_career_matches(interests, skills, personality_traits)
    
    return {
        "top_interests": list(set(interests))[:5],
        "top_skills": list(set(skills))[:5],
        "personality_traits": list(set(personality_traits))[:3],
        "career_matches": career_matches,
        "summary": f"Based on your responses, you show strong interest in {', '.join(interests[:3])} with skills in {', '.join(skills[:2])}."
    }

def create_career_matches(interests, skills, personality_traits):
    """Create career matches based on user responses"""
    
    career_database = {
        "Software Developer": {
            "interests": ["technology", "problem_solving", "creative"],
            "skills": ["technical", "analytical", "problem_solving"],
            "personality": ["independent", "detail_oriented"]
        },
        "Data Scientist": {
            "interests": ["analytical", "research", "technology"],
            "skills": ["data", "analytical", "technical"],
            "personality": ["analytical_thinker", "independent"]
        },
        "UX Designer": {
            "interests": ["creative", "people", "technology"],
            "skills": ["creative", "communication", "technical"],
            "personality": ["creative_solutions", "collaborative"]
        },
        "Product Manager": {
            "interests": ["business", "technology", "leadership"],
            "skills": ["leadership", "communication", "analytical"],
            "personality": ["leader", "team_player"]
        },
        "Marketing Specialist": {
            "interests": ["creative", "business", "people"],
            "skills": ["communication", "creative", "analytical"],
            "personality": ["collaborative", "spokesperson"]
        }
    }
    
    matches = []
    
    for career, requirements in career_database.items():
        score = 0
        
        # Calculate match score
        interest_match = len(set(interests) & set(requirements["interests"]))
        skill_match = len(set(skills) & set(requirements["skills"]))
        personality_match = len(set(personality_traits) & set(requirements["personality"]))
        
        total_score = (interest_match * 3 + skill_match * 2 + personality_match * 1)
        
        if total_score > 0:
            matches.append({
                "title": career,
                "match_score": min(95, total_score * 10),
                "reasons": [
                    f"Interest alignment: {interest_match} matches",
                    f"Skill alignment: {skill_match} matches", 
                    f"Personality fit: {personality_match} matches"
                ]
            })
    
    return sorted(matches, key=lambda x: x["match_score"], reverse=True)[:5]

def display_career_analysis_results(analysis):
    """Display the comprehensive career analysis results from all 12 agents"""
    
    st.markdown("## 🎯 Your Comprehensive 12-Agent Career Analysis")
    
    # Handle error case
    if "error" in analysis:
        st.error(f"Analysis Error: {analysis['error']}")
        if "fallback_summary" in analysis:
            st.info(analysis["fallback_summary"])
        return
    
    # Summary Overview
    if analysis.get("summary"):
        st.markdown(f"""
        <div style="background: #2a2a2a; padding: 25px; border-radius: 12px; margin: 20px 0; border: 2px solid #00ff84;">
            <h3 style="color: #00ff84; margin-bottom: 15px;">📋 Assessment Summary</h3>
            <p style="color: #ffffff; font-size: 16px; line-height: 1.6;">
                {analysis['summary']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Comprehensive Insights
    if analysis.get("comprehensive_insights"):
        st.markdown("### 🔍 Key Insights from All Agents")
        
        insights = analysis["comprehensive_insights"]
        
        # Display insights in columns
        col1, col2 = st.columns(2)
        
        for i, insight in enumerate(insights):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                st.markdown(f"""
                <div style="background: #3a3a3a; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 3px solid #0084ff;">
                    <p style="color: #ffffff; margin: 0; font-size: 14px; line-height: 1.5;">
                        💡 {insight}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Career Connections
    if analysis.get("career_matches"):
        st.markdown("### 🎯 Career Connections")
        
        # Display top career matches
        career_matches = analysis["career_matches"][:12]  # Show top 12
        
        # Group into columns
        cols = st.columns(3)
        for i, career in enumerate(career_matches):
            col_index = i % 3
            with cols[col_index]:
                st.markdown(f"""
                <div style="background: #2d4a2d; padding: 12px; border-radius: 8px; margin: 8px 0; border: 1px solid #00ff84;">
                    <p style="color: #ffffff; margin: 0; font-size: 14px; text-align: center;">
                        🚀 {career}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Key Recommendations  
    if analysis.get("key_recommendations"):
        st.markdown("### 💡 Personalized Recommendations")
        
        recommendations = analysis["key_recommendations"]
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div style="background: #4a2d4a; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 3px solid #ff6b6b;">
                <p style="color: #ffffff; margin: 0; font-size: 14px; line-height: 1.5;">
                    <strong style="color: #ff6b6b;">{i}.</strong> {rec}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Next Steps
    if analysis.get("next_steps"):
        st.markdown("### 🔄 Recommended Next Steps")
        
        for i, step in enumerate(analysis["next_steps"], 1):
            st.markdown(f"""
            <div style="background: #2d4a4a; padding: 12px; border-radius: 6px; margin: 8px 0; border-left: 3px solid #17a2b8;">
                <p style="color: #ffffff; margin: 0; font-size: 14px;">
                    <strong style="color: #17a2b8;">Step {i}:</strong> {step}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Action Buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download Report", key="download_report", use_container_width=True):
            # Generate downloadable report
            report_data = generate_downloadable_report(analysis)
            st.download_button(
                label="📥 Download PDF Report",
                data=report_data,
                file_name=f"career_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("🔄 Retake Assessment", key="retake_assessment", use_container_width=True):
            # Reset assessment
            st.session_state.assessment_mode = "time_selection"
            st.session_state.current_agent_index = 0
            st.session_state.current_question_index = 0
            st.rerun()
    
    with col3:
        if st.button("💬 Start Chat Session", key="start_chat", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()

def generate_downloadable_report(analysis):
    """Generate a text report of the career analysis"""
    report = f"""
REMIRO AI CAREER ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== ASSESSMENT SUMMARY ===
{analysis.get('summary', 'Assessment completed successfully')}

=== KEY INSIGHTS ===
"""
    
    for i, insight in enumerate(analysis.get('comprehensive_insights', []), 1):
        report += f"{i}. {insight}\n"
    
    report += "\n=== CAREER CONNECTIONS ===\n"
    for i, career in enumerate(analysis.get('career_matches', [])[:10], 1):
        report += f"{i}. {career}\n"
    
    report += "\n=== RECOMMENDATIONS ===\n"
    for i, rec in enumerate(analysis.get('key_recommendations', []), 1):
        report += f"{i}. {rec}\n"
    
    report += "\n=== NEXT STEPS ===\n"
    for i, step in enumerate(analysis.get('next_steps', []), 1):
        report += f"{i}. {step}\n"
    
    report += "\n\nThis report was generated by Remiro AI's 12-dimensional career assessment system.\n"
    
    return report
    
    # Hide header for full-page chat experience
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #505050; margin-bottom: 20px; background: #2d2d2d;">
        <h2 style="color: #ffffff; margin: 0; font-weight: 600;">🎯 Remiro AI Career Assistant</h2>
        <p style="color: #cccccc; margin: 5px 0 0 0;">Your AI-Powered 12D Career Counselor</p>
        <p style="color: #0084ff; margin: 8px 0 0 0; font-size: 14px;">Dark Theme • Professional Interface • All Agents Active</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main chat container with proper layout
    chat_container = st.container()
    
    with chat_container:
        # Chat history display area
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display conversation history
        if st.session_state.conversation_history:
            for i, message in enumerate(st.session_state.conversation_history[-15:]):  # Show last 15 messages
                if message.get('user'):
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong><br>
                        {message['user']}
                    </div>
                    """, unsafe_allow_html=True)
                
                if message.get('assistant'):
                    st.markdown(f"""
                    <div class="assistant-message">
                        <strong>🎯 Remiro AI:</strong><br>
                        {message['assistant']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Welcome message for first interaction
            user_name = st.session_state.user_details.get('name', 'Friend')
            st.markdown(f"""
            <div class="assistant-message">
                <strong>🎯 Remiro AI:</strong><br>
                Hey there, {user_name}! 👋 I'm Remiro, your friendly career companion! 
                <br><br>
                Welcome to our professional dark interface! I'm here to help you explore exciting career possibilities through our comprehensive 12D assessment. 
                <br><br>
                To get started, tell me - what kind of things do you love doing in your free time? What are your hobbies or interests that really get you excited? 🚀
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fixed input area at bottom
    st.markdown("""
    <div style="
        position: fixed; 
        bottom: 0; 
        left: 0; 
        right: 0; 
        background: #ffffff; 
        border-top: 1px solid #e5e5e7; 
        padding: 20px;
        z-index: 999;
    ">
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize message counter for unique keys
    if 'message_counter' not in st.session_state:
        st.session_state.message_counter = 0
    
    # Create input area
    st.markdown('<div style="margin-bottom: 100px;">', unsafe_allow_html=True)  # Space for fixed input
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Message",
            key=f"chat_input_{st.session_state.message_counter}", 
            placeholder="💬 Type your message here...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_clicked = st.button("Send", key=f"send_button_{st.session_state.message_counter}", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle user input - single source of truth
    if (send_clicked and user_input.strip()) or (user_input.strip() and st.session_state.get('enter_pressed')):
        # Reset enter pressed state
        if 'enter_pressed' in st.session_state:
            del st.session_state['enter_pressed']
            
        with st.spinner("🤔 Thinking..."):
            response = process_user_input(user_input)
            
            # Save conversation
            save_conversation(user_input, response.get('message', ''))
            
            # Increment counter to create new input field
            st.session_state.message_counter += 1
            
            # Rerun to clear input and update chat
            st.rerun()

def render_main_chat_view():
    """Render a full-page modern AI chatbot interface"""
    
    # Header with assessment option
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #505050; margin-bottom: 20px; background: #2d2d2d;">
        <h2 style="color: #ffffff; margin: 0; font-weight: 600;">🎯 Remiro AI Career Assistant</h2>
        <p style="color: #cccccc; margin: 5px 0 0 0;">Your AI-Powered 12D Career Counselor</p>
        <p style="color: #0084ff; margin: 8px 0 0 0; font-size: 14px;">Dark Theme • Professional Interface • All Agents Active</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Assessment mode selection
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Start Interactive Assessment", key="start_interactive", use_container_width=True):
            # Initialize assessment state properly
            st.session_state.assessment_mode = "time_selection"
            st.session_state.current_view = "interactive_assessment"
            st.session_state.current_agent_index = 0
            st.session_state.current_question_index = 0
            st.session_state.assessment_start_time = None
            st.session_state.time_preference = None
            st.session_state.assessment_config = None
            st.rerun()
    
    # Main chat container with proper layout
    chat_container = st.container()
    
    with chat_container:
        # Chat history display area
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display conversation history
        if st.session_state.conversation_history:
            for i, message in enumerate(st.session_state.conversation_history[-15:]):  # Show last 15 messages
                if message.get('user'):
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong><br>
                        {message['user']}
                    </div>
                    """, unsafe_allow_html=True)
                
                if message.get('assistant'):
                    st.markdown(f"""
                    <div class="assistant-message">
                        <strong>🎯 Remiro AI:</strong><br>
                        {message['assistant']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Welcome message for first interaction
            user_name = st.session_state.user_details.get('name', 'Friend')
            st.markdown(f"""
            <div class="assistant-message">
                <strong>🎯 Remiro AI:</strong><br>
                Hey there, {user_name}! 👋 I'm Remiro, your friendly career companion! 
                <br><br>
                Welcome to our professional dark interface! I'm here to help you explore exciting career possibilities through our comprehensive 12D assessment. 
                <br><br>
                To get started, tell me - what kind of things do you love doing in your free time? What are your hobbies or interests that really get you excited? 🚀
                <br><br>
                Or click the "Start Interactive Assessment" button above for our new checkbox-based assessment with customizable time options!
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fixed input area at bottom
    st.markdown("""
    <div style="
        position: fixed; 
        bottom: 0; 
        left: 0; 
        right: 0; 
        background: #ffffff; 
        border-top: 1px solid #e5e5e7; 
        padding: 20px;
        z-index: 999;
    ">
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize message counter for unique keys
    if 'message_counter' not in st.session_state:
        st.session_state.message_counter = 0
    
    # Create input area
    st.markdown('<div style="margin-bottom: 100px;">', unsafe_allow_html=True)  # Space for fixed input
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Message",
            key=f"chat_input_{st.session_state.message_counter}", 
            placeholder="💬 Type your message here...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_clicked = st.button("Send", key=f"send_button_{st.session_state.message_counter}", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle user input - single source of truth
    if (send_clicked and user_input.strip()) or (user_input.strip() and st.session_state.get('enter_pressed')):
        # Reset enter pressed state
        if 'enter_pressed' in st.session_state:
            del st.session_state['enter_pressed']
            
        with st.spinner("🤔 Thinking..."):
            response = process_user_input(user_input)
            
            # Save conversation
            save_conversation(user_input, response.get('message', ''))
            
            # Increment counter to create new input field
            st.session_state.message_counter += 1
            
            # Rerun to clear input and update chat
            st.rerun()

def render_enhanced_header():
    """Render enhanced header with user info"""
    user_name = st.session_state.user_details.get('name', 'Friend')
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%); 
                padding: 25px; 
                border-radius: 15px; 
                margin-bottom: 25px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h1 style="color: white; 
                   margin: 0; 
                   font-size: 2.8rem;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                   font-weight: bold;">
            🎯 Remiro AI
        </h1>
        <p style="color: rgba(255,255,255,0.95); 
                  margin: 8px 0 0 0; 
                  font-size: 1.3rem;
                  font-weight: 500;">
            Your Advanced AI-Powered Career Counselor & 12D Assessment Platform
        </p>
        <p style="color: #FFEB3B; 
                  margin: 15px 0 0 0; 
                  font-size: 1.1rem;
                  font-weight: 600;">
            👋 Welcome back, {user_name}! Ready to explore your career potential?
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_progress_view():
    """Render the progress tracking view"""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">📊 Assessment Progress</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Chat"):
        st.session_state.current_view = "chat"
        st.rerun()
    
    # Progress overview
    if st.session_state.assessment_progress:
        render_assessment_progress(st.session_state.assessment_progress)
        
        # Progress chart
        fig = create_progress_chart(st.session_state.assessment_progress)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed progress
        st.markdown('<h3>📋 Detailed Progress</h3>', unsafe_allow_html=True)
        
        for agent_type, progress in st.session_state.assessment_progress.items():
            with st.expander(f"{agent_type.title()} Agent"):
                st.write(f"**Status:** {'✅ Completed' if progress.get('completed') else '⏳ In Progress'}")
                st.write(f"**Responses:** {len(progress.get('responses', []))}")
                
                if progress.get('analysis'):
                    st.write("**Analysis:**")
                    st.json(progress['analysis'])
    else:
        st.info("No assessment progress yet. Start your assessment to see progress here!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_analysis_view():
    """Render the career analysis results view"""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">🎉 Your Career Analysis</h1>', unsafe_allow_html=True)
    
    if st.button("← Back to Chat"):
        st.session_state.current_view = "chat"
        st.rerun()
    
    if st.session_state.career_analysis:
        render_career_analysis(st.session_state.career_analysis)
        
        # Download results option
        if st.button("📄 Download Full Report"):
            analysis_json = json.dumps(st.session_state.career_analysis, indent=2)
            st.download_button(
                label="💾 Download as JSON",
                data=analysis_json,
                file_name=f"remiro_career_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    else:
        st.info("Complete your 12D assessment to see your career analysis here!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Check if user needs to be onboarded
    if not st.session_state.user_onboarded:
        render_user_onboarding()
        return
    
    # Navigation
    current_view = st.session_state.get('current_view', 'chat')
    
    # Show career analysis automatically when complete
    if st.session_state.get('show_analysis', False) and current_view == 'chat':
        st.session_state.current_view = 'analysis'
        st.session_state.show_analysis = False
        st.rerun()
    
    # Render appropriate view
    if current_view == 'chat':
        render_main_chat_view()
    elif current_view == 'interactive_assessment':
        render_interactive_assessment_view()
    elif current_view == 'progress':
        render_progress_view()
    elif current_view == 'analysis':
        render_analysis_view()
    
    # Footer with enhanced colors
    st.markdown(f"""
    <div style="text-align: center; 
                margin-top: 3rem; 
                padding: 2rem; 
                background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%); 
                border-radius: 15px;
                color: white; 
                font-size: 0.9rem;">
        🎯 <strong>Remiro AI Career Assistant</strong> - Advanced 12D Career Assessment Platform<br>
        <span style="color: #FFEB3B;">Powered by AI • Designed for {st.session_state.user_details.get('name', 'Your')} Success</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()