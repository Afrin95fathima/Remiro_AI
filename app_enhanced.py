"""
Enhanced Remiro AI - Comprehensive Career Counseling System
A personalized 12-dimensional career assessment and planning platform
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
import time
import random

# Enhanced imports for all agents
from core.user_manager import UserManager
from core.langgraph_workflow import CareerCounselingWorkflow
from agents.master_agent import MasterAgent
from agents.aspirations import AspirationsAgent
from agents.personality import PersonalityAgent
from agents.interests import InterestsAgent
from agents.motivations_values import MotivationsValuesAgent
from agents.skills import SkillsAgent
from agents.cognitive_abilities import CognitiveAbilitiesAgent
from agents.learning_preferences import LearningPreferencesAgent
from agents.physical_context import PhysicalContextAgent
from agents.strengths_weaknesses import StrengthsWeaknessesAgent
from agents.emotional_intelligence import EmotionalIntelligenceAgent
from agents.track_record import TrackRecordAgent
from agents.constraints import ConstraintsAgent

# Initialize LLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os

@st.cache_resource
def get_llm():
    """Initialize and cache the LLM"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Please set your GOOGLE_API_KEY environment variable")
        st.stop()
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key,
        temperature=0.7
    )

@st.cache_resource
def initialize_system():
    """Initialize all system components"""
    llm = get_llm()
    
    # Initialize all agents
    agents = {
        "master": MasterAgent(llm),
        "aspirations": AspirationsAgent(llm),
        "personality": PersonalityAgent(llm),
        "interests": InterestsAgent(llm),
        "motivations_values": MotivationsValuesAgent(llm),
        "skills": SkillsAgent(llm),
        "cognitive_abilities": CognitiveAbilitiesAgent(llm),
        "learning_preferences": LearningPreferencesAgent(llm),
        "physical_context": PhysicalContextAgent(llm),
        "strengths_weaknesses": StrengthsWeaknessesAgent(llm),
        "emotional_intelligence": EmotionalIntelligenceAgent(llm),
        "track_record": TrackRecordAgent(llm),
        "constraints": ConstraintsAgent(llm)
    }
    
    # Initialize workflow and user manager
    workflow = CareerCounselingWorkflow(agents)
    user_manager = UserManager()
    
    return agents, workflow, user_manager

def apply_custom_css():
    """Apply enhanced custom CSS styling"""
    st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Enhanced agent option cards */
    .agent-option-card {
        background: white;
        border: 2px solid #e8ecf0;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
    }
    
    .agent-option-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .agent-option-card:hover:before {
        transform: scaleX(1);
    }
    
    .agent-option-card:hover {
        border-color: #667eea;
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(102,126,234,0.15);
    }
    
    .agent-card-title {
        color: #2d3748;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .agent-card-description {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Enhanced progress dashboard */
    .progress-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .progress-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .progress-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .progress-subtitle {
        color: #4a5568;
        font-size: 1rem;
    }
    
    /* Metrics styling */
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1.5rem 0;
    }
    
    .metric-item {
        text-align: center;
        padding: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #4a5568;
        margin-top: 0.5rem;
    }
    
    /* Enhanced chat interface */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .agent-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
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
    }
    
    .agent-info h3 {
        margin: 0;
        color: #2d3748;
        font-size: 1.3rem;
    }
    
    .agent-info p {
        margin: 0;
        color: #4a5568;
        font-size: 0.9rem;
    }
    
    /* Action plan styling */
    .action-plan-section {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .action-plan-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .action-plan-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .career-path-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    
    .career-path-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
        font-weight: 500;
    }
    
    /* Completed assessment badges */
    .assessment-badge {
        display: inline-block;
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        font-size: 0.9rem;
        margin: 0.25rem;
        font-weight: 500;
    }
    
    /* Button enhancements */
    .stButton > button {
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    
    /* Sidebar styling */
    .sidebar-content {
        padding: 1rem;
    }
    
    .user-profile-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Animation classes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .agent-option-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .progress-container {
            padding: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_progress_dashboard(user_profile: Dict[str, Any], master_agent):
    """Display enhanced progress dashboard with visual indicators"""
    
    # Get progress data
    try:
        progress = master_agent.get_assessment_progress(user_profile)
    except:
        # Fallback progress calculation
        assessments = user_profile.get('assessments', {})
        completed = [k for k, v in assessments.items() if v.get('completed', False)]
        total = 12
        progress = {
            "completed": completed,
            "remaining": [k for k in ['personality', 'interests', 'motivations_values', 'skills', 
                         'cognitive_abilities', 'learning_preferences', 'physical_context', 
                         'aspirations', 'strengths_weaknesses', 'emotional_intelligence', 
                         'track_record', 'constraints'] if k not in completed],
            "progress_percentage": round((len(completed) / total) * 100, 1),
            "total_dimensions": total
        }
    
    st.markdown('<div class="progress-container fade-in">', unsafe_allow_html=True)
    
    # Progress header
    st.markdown(f"""
    <div class="progress-header">
        <div class="progress-title">🎯 Your Career Discovery Journey</div>
        <div class="progress-subtitle">Comprehensive 12-Dimensional Assessment</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-value">{len(progress['completed'])}</div>
            <div class="metric-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-value">{len(progress['remaining'])}</div>
            <div class="metric-label">Remaining</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-value">{progress['progress_percentage']}%</div>
            <div class="metric-label">Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        stage_display = progress.get('stage', 'assessment').title()
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-value" style="font-size: 1.2rem;">{stage_display}</div>
            <div class="metric-label">Current Stage</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress['progress_percentage'] / 100)
    
    # Completed assessments
    if progress['completed']:
        st.markdown("### ✅ Completed Assessments")
        completed_html = ""
        for dimension in progress['completed']:
            display_name = dimension.replace('_', ' ').title()
            completed_html += f'<span class="assessment-badge">✓ {display_name}</span> '
        st.markdown(completed_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_agent_options(options: List[Dict[str, str]], key_prefix: str = "option"):
    """Display enhanced agent selection options"""
    st.markdown("### 🎯 Choose Your Next Step")
    st.markdown("*Click on any area below to continue your career discovery journey*")
    
    selected_agent = None
    
    # Create columns for better layout
    cols = st.columns(2)
    
    for i, option in enumerate(options):
        col = cols[i % 2]
        
        with col:
            # Extract emoji from title if present
            title = option['title']
            description = option['description']
            agent_key = option['agent']
            
            # Create unique key for this button
            button_key = f"{key_prefix}_{i}_{agent_key}"
            
            # Custom card HTML
            card_html = f"""
            <div class="agent-option-card fade-in" style="animation-delay: {i * 0.1}s;">
                <div class="agent-card-title">{title}</div>
                <div class="agent-card-description">{description}</div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Button for selection
            if st.button(f"Start {title.split(' ', 1)[-1]}", key=button_key, help=description):
                selected_agent = agent_key
    
    return selected_agent

def display_chat_interface(agent, user_profile: Dict[str, Any]):
    """Display enhanced chat interface"""
    user_name = user_profile.get('name', 'User')
    agent_name = getattr(agent, 'agent_name', 'Career Counselor')
    
    st.markdown('<div class="chat-container fade-in">', unsafe_allow_html=True)
    
    # Agent header
    agent_emoji = "🤖"  # Could be customized per agent
    st.markdown(f"""
    <div class="agent-header">
        <div class="agent-avatar">{agent_emoji}</div>
        <div class="agent-info">
            <h3>{agent_name}</h3>
            <p>Personalized guidance for {user_name}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages container
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        if message['role'] == 'assistant':
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message['content'])
        else:
            with st.chat_message("user", avatar="👤"):
                st.write(message['content'])
    
    # Input area
    user_input = st.chat_input(f"Share your thoughts with {agent_name}...")
    
    if user_input:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        # Process with agent
        with st.spinner("Processing your response..."):
            try:
                result = asyncio.run(agent.process_interaction(user_input, user_profile))
                
                if result.get('success'):
                    # Add assistant message
                    st.session_state.chat_messages.append({
                        "role": "assistant", 
                        "content": result['message']
                    })
                    
                    # Handle assessment completion
                    if result.get('assessment_complete'):
                        st.success("✅ Assessment completed successfully!")
                        
                        # Save assessment data
                        if result.get('assessment_data'):
                            # Update user profile with assessment data
                            current_agent_type = type(agent).__name__.lower().replace('agent', '')
                            user_profile.setdefault('assessments', {})
                            user_profile['assessments'][current_agent_type] = {
                                'completed': True,
                                'data': result['assessment_data'],
                                'completed_at': datetime.now().isoformat()
                            }
                        
                        time.sleep(2)
                        st.rerun()
                else:
                    st.error("I apologize, but I encountered an issue. Please try again.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

async def generate_action_plan(user_profile: Dict[str, Any], master_agent):
    """Generate comprehensive action plan"""
    try:
        result = await master_agent.generate_action_plan(user_profile)
        return result
    except Exception as e:
        return {
            "success": False,
            "message": f"Hi {user_profile.get('name', 'there')}! I'm working on creating your personalized action plan. Please complete more assessments for a comprehensive career strategy.",
            "executive_summary": {
                "career_identity": "Developing professional focused on self-discovery",
                "primary_career_direction": "Multiple paths available - complete assessments for specificity"
            }
        }

def display_action_plan(action_plan: Dict[str, Any]):
    """Display comprehensive action plan"""
    if not action_plan.get('success', True):
        st.info(action_plan.get('message', 'Complete more assessments for a detailed action plan.'))
        return
    
    st.markdown('<div class="action-plan-section fade-in">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="action-plan-header">
        <div class="action-plan-title">🎯 Your Personalized Career Action Plan</div>
        <p style="color: #4a5568; font-size: 1.1rem;">A comprehensive roadmap for your career success</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Executive Summary
    if action_plan.get('executive_summary'):
        summary = action_plan['executive_summary']
        
        st.markdown("## 📊 Executive Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Career Identity")
            st.info(summary.get('career_identity', 'Professional in development'))
            
            st.markdown("### 🛤️ Primary Direction")
            st.success(summary.get('primary_career_direction', 'Exploring multiple pathways'))
        
        with col2:
            if summary.get('key_differentiators'):
                st.markdown("### ⭐ Your Unique Strengths")
                for strength in summary['key_differentiators']:
                    st.markdown(f'<span class="skill-badge">{strength}</span>', unsafe_allow_html=True)
            
            if summary.get('success_probability'):
                st.markdown("### 📈 Success Outlook")
                st.info(summary['success_probability'])
    
    # Career Strategy
    if action_plan.get('career_strategy'):
        strategy = action_plan['career_strategy']
        
        st.markdown("## 🚀 Career Strategy")
        
        if strategy.get('primary_career_paths'):
            st.markdown("### 🎯 Recommended Career Paths")
            
            for i, path in enumerate(strategy['primary_career_paths']):
                with st.expander(f"🔥 {path.get('title', f'Career Path {i+1}')} - {path.get('match_score', 85)}% Match"):
                    st.write(f"**Why this fits:** {path.get('description', 'Great alignment with your profile')}")
                    
                    if path.get('entry_strategies'):
                        st.write("**Entry Strategies:**")
                        for strategy_item in path['entry_strategies']:
                            st.write(f"• {strategy_item}")
                    
                    if path.get('growth_trajectory'):
                        st.write(f"**Growth Path:** {path['growth_trajectory']}")
    
    # Action Roadmap
    if action_plan.get('action_roadmap'):
        roadmap = action_plan['action_roadmap']
        
        st.markdown("## 🗺️ Action Roadmap")
        
        # Phase 1: Immediate
        if roadmap.get('phase_1_immediate'):
            phase1 = roadmap['phase_1_immediate']
            st.markdown(f"### ⚡ Phase 1: {phase1.get('timeline', 'Immediate Actions')}")
            
            for action in phase1.get('actions', []):
                st.markdown(f"""
                <div class="career-path-card">
                    <strong>🎯 {action.get('task', 'Action item')}</strong><br>
                    <em>Deadline:</em> {action.get('deadline', 'ASAP')}<br>
                    <em>Impact:</em> {action.get('impact', 'Important for progress')}
                </div>
                """, unsafe_allow_html=True)
        
        # Phase 2: Short-term
        if roadmap.get('phase_2_short_term'):
            phase2 = roadmap['phase_2_short_term']
            st.markdown(f"### 📈 Phase 2: {phase2.get('timeline', 'Short-term Goals')}")
            
            for goal in phase2.get('goals', []):
                with st.expander(f"🎯 {goal.get('objective', 'Goal')}"):
                    if goal.get('success_metrics'):
                        st.write("**Success Metrics:**")
                        for metric in goal['success_metrics']:
                            st.write(f"• {metric}")
                    
                    if goal.get('resources_needed'):
                        st.write("**Resources Needed:**")
                        for resource in goal['resources_needed']:
                            st.write(f"• {resource}")
    
    # Skill Development
    if action_plan.get('skill_development_plan'):
        skills = action_plan['skill_development_plan']
        
        st.markdown("## 🛠️ Skill Development Plan")
        
        if skills.get('core_skills_to_develop'):
            for skill in skills['core_skills_to_develop']:
                with st.expander(f"📚 {skill.get('skill', 'Skill')} ({skill.get('current_level', 'Current')} → {skill.get('target_level', 'Target')})"):
                    st.write(f"**Learning Path:** {skill.get('learning_path', 'Structured development approach')}")
                    st.write(f"**Timeline:** {skill.get('timeline', '3-6 months')}")
        
        if skills.get('learning_resources'):
            resources = skills['learning_resources']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if resources.get('online_courses'):
                    st.markdown("**📖 Recommended Courses:**")
                    for course in resources['online_courses']:
                        st.write(f"• {course}")
            
            with col2:
                if resources.get('books'):
                    st.markdown("**📚 Recommended Reading:**")
                    for book in resources['books']:
                        st.write(f"• {book}")
    
    # Networking Strategy
    if action_plan.get('networking_and_relationship_strategy'):
        networking = action_plan['networking_and_relationship_strategy']
        
        st.markdown("## 🤝 Networking Strategy")
        
        if networking.get('target_connections'):
            st.markdown("### 👥 Target Connections")
            for connection in networking['target_connections']:
                st.markdown(f"""
                <div class="career-path-card">
                    <strong>{connection.get('type', 'Professional Contact')}</strong><br>
                    <em>Where to find:</em> {connection.get('where_to_find', 'Professional networks')}<br>
                    <em>Approach:</em> {connection.get('conversation_approach', 'Professional introduction')}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Remiro AI - Career Counselor",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    apply_custom_css()
    
    # Main header
    st.markdown("""
    <div class="main-header fade-in">
        <h1>🎯 Remiro AI Career Counselor</h1>
        <p>Your Personalized 12-Dimensional Career Discovery & Planning System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    try:
        agents, workflow, user_manager = initialize_system()
    except Exception as e:
        st.error(f"Failed to initialize system: {str(e)}")
        st.stop()
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # Sidebar for user profile setup
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        st.header("👤 Your Profile")
        
        # User profile form
        with st.form("user_profile_form"):
            name = st.text_input("Your Name", placeholder="Enter your full name")
            background = st.selectbox(
                "Background",
                ["Student", "Recent Graduate", "Professional", "Career Changer", "Returning to Work"],
                help="This helps us personalize your experience"
            )
            
            submitted = st.form_submit_button("🚀 Start Your Journey")
            
            if submitted and name.strip():
                # Create or load user profile
                user_profile = user_manager.get_or_create_user(name.strip(), {"background": background})
                st.session_state.user_profile = user_profile
                st.session_state.chat_messages = []  # Reset chat
                st.success(f"Welcome {name}! Your personalized career journey begins now.")
                time.sleep(1)
                st.rerun()
        
        # Display current user info
        if st.session_state.user_profile:
            user_profile = st.session_state.user_profile
            st.markdown(f"""
            <div class="user-profile-card">
                <h4>👋 Hello, {user_profile.get('name', 'User')}!</h4>
                <p><strong>Background:</strong> {user_profile.get('background', 'Not specified')}</p>
                <p><strong>Journey Started:</strong> {user_profile.get('created_at', 'Today')[:10]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main application content
    if st.session_state.user_profile:
        user_profile = st.session_state.user_profile
        master_agent = agents['master']
        
        # Display progress dashboard
        display_progress_dashboard(user_profile, master_agent)
        
        # Handle current agent interaction
        if st.session_state.current_agent:
            current_agent_name = st.session_state.current_agent
            current_agent = agents.get(current_agent_name)
            
            if current_agent:
                # Display chat interface
                display_chat_interface(current_agent, user_profile)
                
                # Back to options button
                if st.button("⬅️ Back to Options", key="back_to_options"):
                    st.session_state.current_agent = None
                    st.session_state.chat_messages = []
                    st.rerun()
            else:
                st.error(f"Agent '{current_agent_name}' not found.")
                st.session_state.current_agent = None
        
        else:
            # Get available options from master agent
            try:
                options = master_agent.get_next_agent_options(user_profile)
            except:
                # Fallback options
                options = [
                    {"agent": "personality", "title": "🧠 Personality Assessment", "description": "Discover your natural work style and preferences"},
                    {"agent": "interests", "title": "💡 Career Interests", "description": "Explore what truly engages and motivates you"},
                    {"agent": "aspirations", "title": "🎯 Career Aspirations", "description": "Define your career goals and future vision"},
                    {"agent": "skills", "title": "🛠️ Skills Assessment", "description": "Evaluate your current abilities and strengths"}
                ]
            
            # Check if ready for action plan
            assessments = user_profile.get('assessments', {})
            completed_count = len([a for a in assessments.values() if a.get('completed', False)])
            
            if completed_count >= 8:  # Threshold for action plan
                st.markdown("### 🎉 Ready for Your Action Plan!")
                st.info("You've completed enough assessments to generate a comprehensive career action plan!")
                
                if st.button("🎯 Generate My Career Action Plan", type="primary", key="generate_action_plan"):
                    with st.spinner("Creating your personalized career action plan..."):
                        action_plan = asyncio.run(generate_action_plan(user_profile, master_agent))
                        st.session_state.action_plan = action_plan
                        st.rerun()
            
            # Display action plan if available
            if 'action_plan' in st.session_state:
                display_action_plan(st.session_state.action_plan)
                
                # Option to continue assessments
                st.markdown("---")
                st.markdown("### Continue Your Assessment")
                st.info("You can still complete additional assessments to refine your career plan!")
            
            # Display agent options
            selected_agent = display_agent_options(options, "main_options")
            
            if selected_agent:
                if selected_agent == "insights":
                    # Generate insights
                    with st.spinner("Generating your career insights..."):
                        try:
                            insights = asyncio.run(master_agent.generate_insights(user_profile))
                            
                            if insights.get('success'):
                                st.success("✨ **Your Career Insights**")
                                st.write(insights.get('message', 'Here are your personalized insights...'))
                                
                                # Display additional insight data
                                if insights.get('career_profile'):
                                    profile = insights['career_profile']
                                    
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        if profile.get('primary_strengths'):
                                            st.markdown("**🌟 Key Strengths:**")
                                            for strength in profile['primary_strengths']:
                                                st.write(f"• {strength}")
                                    
                                    with col2:
                                        if profile.get('natural_talents'):
                                            st.markdown("**💎 Natural Talents:**")
                                            for talent in profile['natural_talents']:
                                                st.write(f"• {talent}")
                            else:
                                st.info("Complete more assessments for deeper insights!")
                                
                        except Exception as e:
                            st.error(f"Unable to generate insights: {str(e)}")
                
                elif selected_agent in agents:
                    # Start agent interaction
                    st.session_state.current_agent = selected_agent
                    st.session_state.chat_messages = []
                    
                    # Initialize with agent's first message
                    agent = agents[selected_agent]
                    try:
                        initial_result = asyncio.run(agent.process_interaction("", user_profile))
                        if initial_result.get('success'):
                            st.session_state.chat_messages.append({
                                "role": "assistant",
                                "content": initial_result['message']
                            })
                    except Exception as e:
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": f"Hello! I'm ready to help you explore this important aspect of your career journey. Let's begin!"
                        })
                    
                    st.rerun()
    
    else:
        # Welcome screen for new users
        st.markdown("### 👋 Welcome to Your Career Discovery Journey!")
        
        st.markdown("""
        Remiro AI is your personal career counselor, designed to help you discover your ideal career path through 
        a comprehensive 12-dimensional assessment. Our system provides:
        
        - **🧠 Personality Assessment** - Understanding your natural work style
        - **💡 Interest Exploration** - Discovering what truly engages you  
        - **⭐ Values Clarification** - Identifying what matters most to you
        - **🛠️ Skills Evaluation** - Assessing your current capabilities
        - **🎯 Goal Setting** - Defining your career aspirations
        - **📈 Action Planning** - Creating your personalized roadmap
        
        **To begin your journey, please enter your information in the sidebar** 👈
        """)
        
        # Demo statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Career Paths Explored", "500+")
        
        with col2:
            st.metric("Success Rate", "94%")
        
        with col3:
            st.metric("Assessment Dimensions", "12")

if __name__ == "__main__":
    main()
