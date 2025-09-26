"""
Enhanced UI Components for Remiro AI Career Assistant

Professional, interactive interface with modern styling and excellent UX.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

def apply_custom_css():
    """Apply custom CSS for professional styling with vibrant colors"""
    st.markdown("""
    <style>
    /* Professional Dark Theme */
    .stApp {
        background: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Main Content Container - Dark */
    .main-content {
        background: #2d2d2d !important;
        border-radius: 12px;
        padding: 0;
        margin: 20px auto;
        max-width: 1000px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        border: 1px solid #404040;
    }
    
    /* Chat Interface Styling */
    .chat-container {
        background: transparent !important;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: none !important;
        backdrop-filter: none;
    }
    
    /* Dark theme chat messages */
    .user-message {
        background: #0084ff;
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 18px;
        margin: 12px 0;
        margin-left: 25%;
        max-width: 75%;
        box-shadow: 0 2px 8px rgba(0,132,255,0.3);
        font-weight: 400;
        font-size: 16px;
        line-height: 1.5;
        border: none;
    }
    
    .assistant-message {
        background: #3a3a3a;
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 18px;
        margin: 12px 0;
        margin-right: 25%;
        max-width: 75%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        font-weight: 400;
        font-size: 16px;
        line-height: 1.5;
        border: 1px solid #505050;
    }
    
    /* Dark chat container */
    .chat-container {
        background: #2d2d2d !important;
        min-height: 70vh;
        padding: 20px;
        border-radius: 12px;
        margin: 0;
        border: none !important;
        color: #ffffff;
    }
    
    /* Progress Bar Styling */
    .progress-container {
        background: linear-gradient(135deg, #FFEAA7 0%, #FDCB6E 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 2px solid rgba(255,234,167,0.5);
    }
    
    .progress-bar {
        width: 100%;
        height: 12px;
        background: rgba(255,255,255,0.3);
        border-radius: 6px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00B894, #00CEC9);
        transition: width 0.3s ease;
        transition: width 0.3s ease;
    }
    
    /* Card Styling */
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    
    /* Button Styling */
    .custom-button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
    }
    
    .custom-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(102,126,234,0.4);
    }
    
    /* Agent Status Indicators */
    .agent-status {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 2px;
    }
    
    .status-completed {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-active {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .status-pending {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    /* Typography */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #495057;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 0.5rem;
    }
    
    /* Analysis Results Styling */
    .analysis-section {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #007bff;
    }
    
    .role-recommendation {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        position: relative;
    }
    
    .match-score {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: #28a745;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-content {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .user-message, .assistant-message {
            margin-left: 5%;
            margin-right: 5%;
        }
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide Streamlit default containers */
    .stContainer > div {
        background: transparent !important;
    }
    
    .element-container {
        background: transparent !important;
    }
    
    /* Remove white blocks from chat area */
    .block-container {
        background: transparent !important;
        padding-top: 1rem !important;
    }
    
    /* Make text input area blend better */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid rgba(255,107,107,0.3) !important;
        border-radius: 20px !important;
        color: #333 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255,107,107,0.4) !important;
    }
    
    /* Prevent duplicate text inputs */
    .element-container:has(> .stTextInput) + .element-container:has(> .stTextInput) {
        display: none !important;
    }
    
    /* Style text input properly */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid rgba(78,205,196,0.5) !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        background: rgba(255,255,255,0.9) !important;
        color: #2c3e50 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4ECDC4 !important;
        box-shadow: 0 0 10px rgba(78,205,196,0.3) !important;
    }
    
    /* Ensure proper chat message layout */
    .user-message, .assistant-message {
        max-width: 70%;
        word-wrap: break-word;
        display: block;
        clear: both;
    }
    
    .user-message {
        float: right;
        margin-left: 30%;
    }
    
    .assistant-message {
        float: left;
        margin-right: 30%;
    }
    
    /* Dark theme input and button styling */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #505050 !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        background: #3a3a3a !important;
        color: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0084ff !important;
        box-shadow: 0 0 0 3px rgba(0,132,255,0.2) !important;
        outline: none !important;
    }
    
    .stButton > button {
        background: #0084ff !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #0066cc !important;
        transform: translateY(-1px) !important;
    }
    
    /* Dark theme for all text */
    .stMarkdown, .stText, p, div {
        color: #ffffff !important;
    }
    
    /* Dark sidebar */
    .css-1d391kg {
        background: #2d2d2d !important;
    }
    
    .css-1lcbmhc {
        background: #2d2d2d !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the application header"""
    st.markdown("""
    <div class="main-content">
        <h1 class="main-title">🎯 Remiro AI Career Assistant</h1>
        <p style="text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 2rem;">
            Your Advanced AI-Powered Career Counselor & 12D Assessment Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface(conversation_history: List[Dict], current_input: str = ""):
    """Render the clean chat interface"""
    
    # Chat container with messages
    if conversation_history:
        st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
        
        # Display conversation history
        for i, message in enumerate(conversation_history[-10:]):  # Show last 10 messages
            if message.get('user'):
                st.markdown(f"""
                <div class="user-message fade-in">
                    {message['user']}
                </div>
                """, unsafe_allow_html=True)
            
            if message.get('assistant'):
                st.markdown(f"""
                <div class="assistant-message fade-in">
                    {message['assistant']}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Welcome message for first interaction
        st.markdown(f"""
        <div class="assistant-message fade-in">
            Hey there! 👋 I'm Remiro, your friendly career companion! 

            It's great to meet you! I'm here to have a nice chat and help you explore some exciting career possibilities. 

            So, tell me - what kind of things do you love doing in your free time? What are your hobbies or interests that really get you excited? 🎯
        </div>
        """, unsafe_allow_html=True)

def render_assessment_progress(progress: Dict[str, Any]):
    """Render assessment progress visualization"""
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">📊 Assessment Progress</h3>', unsafe_allow_html=True)
    
    # Calculate progress percentage
    total_agents = 12
    completed = sum(1 for agent_data in progress.values() if agent_data.get('completed', False))
    percentage = (completed / total_agents) * 100
    
    # Progress bar
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {percentage}%"></div>
    </div>
    <p style="text-align: center; margin-top: 0.5rem; color: #666;">
        {completed}/{total_agents} Assessments Completed ({percentage:.0f}%)
    </p>
    """, unsafe_allow_html=True)
    
    # Agent status grid
    agent_names = [
        "🎪 Interests", "🛠️ Skills", "🧠 Personality", "🎯 Aspirations",
        "💭 Motivations", "🧮 Cognitive", "💝 Strengths", "🎓 Learning",
        "🏆 Track Record", "🧘 Emotional IQ", "⚠️ Constraints", "🏃 Physical"
    ]
    
    cols = st.columns(4)
    for i, agent_name in enumerate(agent_names):
        col = cols[i % 4]
        with col:
            agent_key = agent_name.split(' ')[1].lower()
            status = "completed" if progress.get(agent_key, {}).get('completed', False) else "pending"
            status_class = f"status-{status}"
            
            st.markdown(f"""
            <div class="agent-status {status_class}">
                {agent_name}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_career_analysis(analysis: Dict[str, Any]):
    """Render comprehensive career analysis results"""
    
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🎉 Your Career Analysis Results</h2>', unsafe_allow_html=True)
    
    # Role Recommendations
    if analysis.get('role_recommendations'):
        st.markdown('<h3>🎯 Perfect Role Matches</h3>', unsafe_allow_html=True)
        
        for role in analysis['role_recommendations'][:5]:
            match_score = role.get('match_score', 0)
            st.markdown(f"""
            <div class="role-recommendation">
                <div class="match-score">{match_score}% Match</div>
                <h4>{role.get('title', 'Role')}</h4>
                <p><strong>Why it fits:</strong> {', '.join(role.get('reasons', []))}</p>
                {f"<p><strong>Companies:</strong> {', '.join(role.get('companies', []))}</p>" if role.get('companies') else ""}
            </div>
            """, unsafe_allow_html=True)
    
    # Skills Development Plan
    if analysis.get('skill_development_plan'):
        st.markdown('<h3>📈 Your Skill Development Plan</h3>', unsafe_allow_html=True)
        
        high_priority = [s for s in analysis['skill_development_plan'] if s.get('priority') == 'high']
        medium_priority = [s for s in analysis['skill_development_plan'] if s.get('priority') == 'medium']
        
        if high_priority:
            st.markdown('<h4 style="color: #dc3545;">🔥 High Priority Skills</h4>', unsafe_allow_html=True)
            for skill in high_priority[:3]:
                st.markdown(f"""
                <div class="info-card">
                    <h5>{skill.get('skill', 'Skill')}</h5>
                    <p><strong>Timeline:</strong> {skill.get('timeline', 'TBD')}</p>
                    <p><strong>Resources:</strong> {', '.join(skill.get('resources', []))}</p>
                </div>
                """, unsafe_allow_html=True)
        
        if medium_priority:
            st.markdown('<h4 style="color: #ffc107;">⭐ Medium Priority Skills</h4>', unsafe_allow_html=True)
            for skill in medium_priority[:2]:
                st.markdown(f"""
                <div class="info-card">
                    <h5>{skill.get('skill', 'Skill')}</h5>
                    <p><strong>Timeline:</strong> {skill.get('timeline', 'TBD')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Career Roadmap
    if analysis.get('career_roadmap'):
        st.markdown('<h3>🗺️ Your Career Roadmap</h3>', unsafe_allow_html=True)
        
        roadmap = analysis['career_roadmap']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="info-card">
                <h4 style="color: #28a745;">📅 6 Months</h4>
                <ul>
                    {''.join([f"<li>{goal}</li>" for goal in roadmap.get('6_months', [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-card">
                <h4 style="color: #17a2b8;">📅 1 Year</h4>
                <ul>
                    {''.join([f"<li>{goal}</li>" for goal in roadmap.get('1_year', [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="info-card">
                <h4 style="color: #6f42c1;">📅 3 Years</h4>
                <ul>
                    {''.join([f"<li>{goal}</li>" for goal in roadmap.get('3_years', [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Industry Insights
    if analysis.get('industry_insights'):
        st.markdown('<h3>🏭 Industry Insights</h3>', unsafe_allow_html=True)
        
        insights = analysis['industry_insights']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="info-card">
                <h4>🎯 Best Industries for You</h4>
                <ul>
                    {''.join([f"<li>{industry}</li>" for industry in insights.get('best_industries', [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-card">
                <h4>🚀 Growth Sectors</h4>
                <ul>
                    {''.join([f"<li>{sector}</li>" for sector in insights.get('growth_sectors', [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_conversation_suggestions(suggestions: List[str]):
    """Render conversation suggestions as clickable buttons"""
    
    if suggestions:
        st.markdown('<h4>💡 Suggestions</h4>', unsafe_allow_html=True)
        
        cols = st.columns(len(suggestions) if len(suggestions) <= 3 else 3)
        
        for i, suggestion in enumerate(suggestions[:3]):
            with cols[i]:
                if st.button(suggestion, key=f"suggestion_{i}"):
                    return suggestion
    
    return None

def render_sidebar_info():
    """Render sidebar with additional information"""
    
    st.sidebar.markdown("""
    ### 🎯 About Remiro AI
    
    Your advanced AI career counselor powered by:
    - **12D Assessment Framework**
    - **Empathetic Conversation AI**
    - **Personalized Career Roadmaps**
    - **Industry-Specific Insights**
    
    ---
    
    ### 📊 Assessment Dimensions
    
    1. 🎪 **Interests** - What drives your passion
    2. 🛠️ **Skills** - Your current capabilities  
    3. 🧠 **Personality** - Your natural work style
    4. 🎯 **Aspirations** - Your career vision
    5. 💭 **Motivations** - What motivates you
    6. 🧮 **Cognitive Style** - How you think
    7. 💝 **Strengths** - Your natural talents
    8. 🎓 **Learning** - How you learn best
    9. 🏆 **Track Record** - Your achievements
    10. 🧘 **Emotional IQ** - Your people skills
    11. ⚠️ **Constraints** - Your limitations
    12. 🏃 **Physical Context** - Your environment needs
    
    ---
    
    ### 🚀 What You'll Get
    
    ✅ **Role Recommendations** with match scores  
    ✅ **Skill Development Plans** with priorities  
    ✅ **Career Roadmap** with timelines  
    ✅ **Industry Insights** and market trends  
    ✅ **Personalized Action Steps**  
    
    ---
    
    ### 💬 Need Help?
    
    Just ask me anything! I can help with:
    - Career advice and guidance
    - Resume and interview tips  
    - Industry insights
    - Skill development planning
    - Job search strategies
    
    """)

def create_progress_chart(progress_data: Dict[str, Any]) -> go.Figure:
    """Create a progress visualization chart"""
    
    agent_names = [
        "Interests", "Skills", "Personality", "Aspirations",
        "Motivations", "Cognitive", "Strengths", "Learning", 
        "Track Record", "Emotional IQ", "Constraints", "Physical"
    ]
    
    completion_status = []
    for agent in agent_names:
        agent_key = agent.lower().replace(' ', '_')
        status = progress_data.get(agent_key, {}).get('completed', False)
        completion_status.append(1 if status else 0)
    
    fig = go.Figure(data=go.Bar(
        x=agent_names,
        y=completion_status,
        marker_color=['#28a745' if status else '#dc3545' for status in completion_status],
        text=['✓' if status else '○' for status in completion_status],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="12D Assessment Progress",
        xaxis_title="Assessment Dimensions",
        yaxis_title="Completion Status",
        yaxis=dict(tickvals=[0, 1], ticktext=['Pending', 'Complete']),
        height=400,
        showlegend=False
    )
    
    return fig

def render_input_area():
    """Render the user input area"""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Text input
    user_input = st.text_input(
        "💬 Type your message here...",
        placeholder="Ask me anything about your career or start your 12D assessment!",
        key="user_input"
    )
    
    # Send button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        send_clicked = st.button("🚀 Send", key="send_button", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return user_input, send_clicked