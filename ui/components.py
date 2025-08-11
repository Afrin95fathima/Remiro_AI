"""
Reusable UI Components for Remiro AI

This module contains common UI components used throughout the Streamlit interface.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_header():
    """Render the main application header"""
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; 
                border-radius: 10px; 
                margin-bottom: 20px;
                text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">
            🎯 Remiro AI
        </h1>
        <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 1.2rem;">
            Your 12D Career Counsellor
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with user info and progress"""
    
    if 'current_user' not in st.session_state or not st.session_state.current_user:
        return
    
    user = st.session_state.current_user
    
    with st.sidebar:
        st.markdown("### 👤 User Profile")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**User ID:** {user['user_id'][:8]}...")
        
        st.markdown("---")
        
        # Progress Overview
        st.markdown("### 📊 Assessment Progress")
        
        if 'user_manager' in st.session_state:
            try:
                user_profile = st.session_state.user_manager.get_user_profile(user['user_id'])
                if user_profile:
                    completion = user_profile.get_completion_percentage()
                    st.progress(completion / 100)
                    st.write(f"**{completion:.1f}%** Complete")
                    
                    # Show next assessment
                    next_assessment = user_profile.get_next_assessment()
                    if next_assessment:
                        st.info(f"**Next:** {next_assessment.value.replace('_', ' ').title()}")
                    else:
                        st.success("All assessments complete!")
            except Exception as e:
                st.error("Error loading progress")
        
        st.markdown("---")
        
        # Action buttons
        if st.button("📈 View Dashboard", use_container_width=True):
            st.switch_page("Dashboard")
        
        if st.button("🔄 New Session", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()

def render_agent_card(agent_name: str, agent_description: str, is_active: bool = False):
    """Render an agent information card"""
    
    card_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);" if is_active else "background: #f8f9fa; border: 2px solid #e9ecef;"
    text_color = "color: white;" if is_active else "color: #495057;"
    
    st.markdown(f"""
    <div style="{card_style} 
                padding: 15px; 
                border-radius: 10px; 
                margin: 10px 0;
                text-align: center;">
        <h4 style="{text_color} margin: 0;">{agent_name}</h4>
        <p style="{text_color} margin: 5px 0 0 0; font-size: 0.9rem;">{agent_description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_progress_chart(assessment_data: Dict[str, Any]):
    """Render a progress chart for assessments"""
    
    dimensions = [
        "Cognitive Abilities", "Personality", "Emotional Intelligence",
        "Physical Context", "Strengths & Weaknesses", "Skills",
        "Constraints", "Interests", "Motivations & Values",
        "Aspirations", "Track Record", "Learning Preferences"
    ]
    
    # Create sample data (replace with actual data)
    completion_status = [1 if i < 3 else 0 for i in range(12)]  # Example: first 3 completed
    
    fig = go.Figure(data=go.Bar(
        x=dimensions,
        y=completion_status,
        marker_color=['#667eea' if status else '#e9ecef' for status in completion_status]
    ))
    
    fig.update_layout(
        title="Assessment Progress",
        xaxis_title="Dimensions",
        yaxis_title="Completion Status",
        xaxis_tickangle=-45,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_message_bubble(message: str, is_user: bool = False, agent_name: str = "Remiro AI"):
    """Render a chat message bubble"""
    
    if is_user:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
            <div style="background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                        color: white;
                        padding: 12px 16px;
                        border-radius: 18px;
                        border-bottom-right-radius: 4px;
                        max-width: 70%;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
            <div style="background: white;
                        color: #2d3748;
                        padding: 12px 16px;
                        border-radius: 18px;
                        border-bottom-left-radius: 4px;
                        max-width: 70%;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        border-left: 4px solid #667eea;">
                <div style="font-size: 0.8rem; color: #667eea; margin-bottom: 5px;">
                    {agent_name}
                </div>
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_typing_indicator():
    """Render a typing indicator"""
    st.markdown("""
    <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
        <div style="background: white;
                    color: #2d3748;
                    padding: 12px 16px;
                    border-radius: 18px;
                    border-bottom-left-radius: 4px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    border-left: 4px solid #667eea;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="font-size: 0.8rem; color: #667eea;">Remiro AI is thinking</div>
                <div style="display: flex; gap: 4px;">
                    <div style="width: 6px; height: 6px; border-radius: 50%; background: #667eea; animation: bounce 1.4s ease-in-out infinite;"></div>
                    <div style="width: 6px; height: 6px; border-radius: 50%; background: #667eea; animation: bounce 1.4s ease-in-out infinite; animation-delay: 0.2s;"></div>
                    <div style="width: 6px; height: 6px; border-radius: 50%; background: #667eea; animation: bounce 1.4s ease-in-out infinite; animation-delay: 0.4s;"></div>
                </div>
            </div>
        </div>
    </div>
    <style>
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    </style>
    """, unsafe_allow_html=True)

def render_assessment_summary(assessment_data: Dict[str, Any]):
    """Render assessment summary card"""
    
    st.markdown("""
    <div style="background: white; 
                padding: 20px; 
                border-radius: 15px; 
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                margin: 20px 0;">
        <h3 style="color: #2d3748; margin-bottom: 15px;">Assessment Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Add assessment details here
    for key, value in assessment_data.items():
        st.write(f"**{key.replace('_', ' ').title()}:** {value}")

def show_error_message(message: str):
    """Show an error message with consistent styling"""
    st.error(f"❌ {message}")

def show_success_message(message: str):
    """Show a success message with consistent styling"""
    st.success(f"✅ {message}")

def show_info_message(message: str):
    """Show an info message with consistent styling"""
    st.info(f"ℹ️ {message}")

def show_warning_message(message: str):
    """Show a warning message with consistent styling"""
    st.warning(f"⚠️ {message}")
