"""
Simple UI Components - Fallback Implementation

Basic UI components that work without external dependencies.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import json

def apply_custom_css():
    """Apply basic custom CSS"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-content {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: #007bff;
        color: white;
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        margin-left: 20%;
    }
    
    .assistant-message {
        background: #f8f9fa;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        margin-right: 20%;
        border: 1px solid #e9ecef;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render application header"""
    st.markdown("""
    <div class="main-content">
        <h1 class="main-title">🎯 Remiro AI Career Assistant</h1>
        <p style="text-align: center; color: #666; font-size: 1.1rem;">
            Your AI-Powered Career Counselor & Assessment Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface(conversation_history: List[Dict], current_input: str = ""):
    """Render chat interface"""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    for message in conversation_history[-8:]:  # Show last 8 messages
        if message.get('user'):
            st.markdown(f"""
            <div class="user-message">
                {message['user']}
            </div>
            """, unsafe_allow_html=True)
        
        if message.get('assistant'):
            st.markdown(f"""
            <div class="assistant-message">
                {message['assistant']}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_assessment_progress(progress: Dict[str, Any]):
    """Render assessment progress"""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown("## 📊 Assessment Progress")
    
    total_agents = 4  # Simplified to 4 agents
    completed = sum(1 for data in progress.values() if data.get('completed', False))
    percentage = (completed / total_agents) * 100
    
    st.progress(percentage / 100)
    st.write(f"Completed: {completed}/{total_agents} assessments ({percentage:.0f}%)")
    
    # Show agent status
    agent_names = ['Interests', 'Skills', 'Personality', 'Aspirations']
    for i, agent in enumerate(agent_names):
        key = agent.lower()
        status = "✅ Completed" if progress.get(key, {}).get('completed') else "⏳ Pending"
        st.write(f"{i+1}. **{agent}**: {status}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_career_analysis(analysis: Dict[str, Any]):
    """Render career analysis results"""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown("## 🎉 Your Career Analysis")
    
    # Role recommendations
    if analysis.get('role_recommendations'):
        st.markdown("### 🎯 Recommended Roles")
        for role in analysis['role_recommendations'][:3]:
            st.write(f"**{role.get('title', 'Role')}** - {role.get('match_score', 0)}% match")
            if role.get('reasons'):
                st.write(f"*Why it fits: {', '.join(role['reasons'])}*")
            st.write("")
    
    # Skills development
    if analysis.get('skill_development_plan'):
        st.markdown("### 📈 Skills to Develop")
        for skill in analysis['skill_development_plan'][:3]:
            priority = skill.get('priority', 'medium').upper()
            st.write(f"**{skill.get('skill', 'Skill')}** ({priority} priority)")
    
    # Career roadmap
    if analysis.get('career_roadmap'):
        st.markdown("### 🗺️ Your Career Roadmap")
        roadmap = analysis['career_roadmap']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**6 Months**")
            for goal in roadmap.get('6_months', [])[:2]:
                st.write(f"• {goal}")
        
        with col2:
            st.markdown("**1 Year**") 
            for goal in roadmap.get('1_year', [])[:2]:
                st.write(f"• {goal}")
        
        with col3:
            st.markdown("**3 Years**")
            for goal in roadmap.get('3_years', [])[:2]:
                st.write(f"• {goal}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_conversation_suggestions(suggestions: List[str]):
    """Render conversation suggestions"""
    
    if suggestions:
        st.markdown("### 💡 Quick Actions")
        cols = st.columns(len(suggestions) if len(suggestions) <= 3 else 3)
        
        for i, suggestion in enumerate(suggestions[:3]):
            with cols[i]:
                if st.button(suggestion, key=f"suggestion_{i}"):
                    return suggestion
    
    return None

def render_sidebar_info():
    """Render sidebar information"""
    
    st.sidebar.markdown("""
    ### 🎯 About Remiro AI
    
    Your AI career counselor featuring:
    - **Career Assessment**
    - **Personalized Recommendations** 
    - **Career Roadmaps**
    - **Professional Guidance**
    
    ---
    
    ### 📊 Assessment Areas
    
    1. 🎪 **Interests** - What drives you
    2. 🛠️ **Skills** - Your capabilities
    3. 🧠 **Personality** - Your work style
    4. 🎯 **Aspirations** - Your goals
    
    ---
    
    ### 💬 How to Use
    
    1. Start a conversation
    2. Take the assessment
    3. Get personalized recommendations
    4. Plan your career path
    
    """)

def render_input_area():
    """Render user input area"""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    user_input = st.text_input(
        "💬 Type your message:",
        placeholder="Ask me about your career or start your assessment!"
    )
    
    send_clicked = st.button("🚀 Send", type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return user_input, send_clicked

def create_progress_chart(progress_data: Dict[str, Any]):
    """Create simple progress visualization"""
    
    # Simple fallback - return None since plotly may not be available
    return None