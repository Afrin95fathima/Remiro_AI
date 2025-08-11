"""
Remiro AI - 12D Career Counselling Multi-Agent Chatbot
Main Streamlit Application

This is the entry point for the Remiro AI career counselling system.
It provides a professional web interface for users to interact with
the 12-dimensional career assessment agents.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Import core components
from core.user_manager import UserManager
from core.langgraph_workflow import RemiroWorkflow
from ui.chat_interface import ChatInterface

def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="Remiro AI - Your Career Counsellor",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .agent-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
    .progress-container {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .welcome-card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 50px auto;
        max-width: 600px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'user_manager' not in st.session_state:
        st.session_state.user_manager = UserManager()
    
    if 'workflow' not in st.session_state:
        st.session_state.workflow = RemiroWorkflow()
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Render header
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-bottom: 30px;">
        <h1 style="color: white; font-size: 3rem; margin: 0;">🎯 Remiro AI</h1>
        <h3 style="color: rgba(255,255,255,0.9); margin: 5px 0;">Your 12D Career Counsellor</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Main application logic
    if st.session_state.current_user is None:
        render_welcome_screen()
    else:
        # Main Chat Interface
        user = st.session_state.current_user
        
        # Display welcome message and user info
        st.success(f"Welcome back, {user['name']}!")
        
        # Initialize chat interface
        chat_interface = ChatInterface(st.session_state.user_manager, st.session_state.workflow)
        chat_interface.render()
        
        # Add logout button in sidebar
        with st.sidebar:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.current_user = None
                st.session_state.pop('conversation_state', None)
                st.rerun()

def render_welcome_screen():
    """Render the welcome screen for user registration"""
    
    st.markdown("""
    <div class="welcome-card">
        <h1>🎯 Welcome to Remiro AI</h1>
        <h3>Your 12D Career Counsellor</h3>
        <p style="font-size: 18px; color: #666; margin: 20px 0;">
            I'm here to help you discover your ideal career path through 
            a comprehensive 12-dimensional assessment. Let's begin this 
            journey together.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # User registration form
    with st.container():
        st.markdown("### Get Started")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            user_name = st.text_input(
                "What's your name?",
                placeholder="Enter your full name",
                help="This will be used to create your personalized career profile"
            )
            
            if st.button("Begin My Career Assessment", type="primary", use_container_width=True):
                if user_name.strip():
                    try:
                        # Create user profile
                        user = st.session_state.user_manager.create_user(user_name.strip())
                        st.session_state.current_user = user
                        
                        # Show success message and rerun
                        st.success(f"Welcome {user_name}! Let's start your career assessment.")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Failed to create user profile: {str(e)}")
                else:
                    st.warning("Please enter your name to continue.")
    
    # Show features overview
    st.markdown("---")
    st.markdown("### What You'll Discover")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🧠 Cognitive Profile**
        - Reasoning abilities
        - Learning agility
        - Problem-solving style
        - Memory patterns
        """)
    
    with col2:
        st.markdown("""
        **💼 Professional Fit**
        - Personality traits
        - Skills inventory
        - Work preferences
        - Leadership style
        """)
    
    with col3:
        st.markdown("""
        **🎯 Career Direction**
        - Interest mapping
        - Values alignment
        - Growth aspirations
        - Action planning
        """)

if __name__ == "__main__":
    main()
