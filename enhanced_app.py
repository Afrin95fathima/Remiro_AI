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

try:
    from core.enhanced_state_models import (
        UserProfile, ConversationHistory, ConversationMessage,
        AssessmentProgress, SystemState
    )
except ImportError:
    # Fallback if enhanced models not available
    pass

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
        
        # Get API key from environment or Streamlit secrets
        api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        
        if not api_key:
            st.error("⚠️ Google API Key not found. Please set GOOGLE_API_KEY in your environment or Streamlit secrets.")
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
    
    # Initialize conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Initialize master agent
    if 'master_agent' not in st.session_state:
        llm = initialize_llm()
        st.session_state.master_agent = MASTER_AGENT_CLASS(llm)
    
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

def render_main_chat_view():
    """Render the main chat interface view"""
    
    # Header
    render_header()
    
    # Sidebar
    render_sidebar_info()
    
    # Assessment progress (if in progress)
    if st.session_state.assessment_progress:
        render_assessment_progress(st.session_state.assessment_progress)
    
    # Chat history
    render_chat_interface(st.session_state.conversation_history)
    
    # Input area
    user_input, send_clicked = render_input_area()
    
    # Handle user input
    if send_clicked and user_input.strip():
        with st.spinner("🤔 Thinking..."):
            response = process_user_input(user_input)
            
            # Save conversation
            save_conversation(user_input, response.get('message', ''))
            
            # Show suggestions if available
            if response.get('suggestions'):
                suggested = render_conversation_suggestions(response['suggestions'])
                if suggested:
                    # Process suggested input
                    response = process_user_input(suggested)
                    save_conversation(suggested, response.get('message', ''))
            
            # Rerun to update chat
            st.rerun()
    
    # Handle suggestion clicks
    if st.session_state.conversation_history:
        last_response = st.session_state.conversation_history[-1]
        if last_response.get('assistant'):
            # Show quick action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🎯 Start Assessment", key="start_assessment"):
                    response = process_user_input("I want to start my 12D career assessment")
                    save_conversation("Start Assessment", response.get('message', ''))
                    st.rerun()
            
            with col2:
                if st.button("💼 Career Advice", key="career_advice"):
                    response = process_user_input("Give me career advice")
                    save_conversation("Career Advice", response.get('message', ''))
                    st.rerun()
            
            with col3:
                if st.button("📊 View Progress", key="view_progress"):
                    st.session_state.current_view = "progress"
                    st.rerun()

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
    
    # Navigation
    current_view = st.session_state.get('current_view', 'chat')
    
    # Show career analysis automatically when complete
    if st.session_state.show_analysis and current_view == 'chat':
        st.session_state.current_view = 'analysis'
        st.session_state.show_analysis = False
        st.rerun()
    
    # Render appropriate view
    if current_view == 'chat':
        render_main_chat_view()
    elif current_view == 'progress':
        render_progress_view()
    elif current_view == 'analysis':
        render_analysis_view()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1rem; color: #666; font-size: 0.9rem;">
        🎯 <strong>Remiro AI Career Assistant</strong> - Advanced 12D Career Assessment Platform<br>
        Powered by AI • Designed for Your Success
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()