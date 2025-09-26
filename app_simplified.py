"""
Simplified Remiro AI - Direct 12D Assessment with Career Insights
Powered by Gemini 2.5 Flash - NO async issues, direct workflow
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Remiro AI - 12D Career Assessment",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .assessment-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 20px;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_llm():
    """Initialize Gemini 2.5 LLM"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        st.error("🚨 Google API Key not found!")
        st.stop()
    
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # Using Gemini 1.5 Flash (stable and reliable)
        google_api_key=api_key,
        temperature=0.7,
        max_retries=2,
        request_timeout=30
    )

def get_assessment_questions(dimension: str) -> List[Dict]:
    """Get questions for each assessment dimension"""
    questions_db = {
        "interests": [
            {
                "question": "What activities make you lose track of time because you enjoy them so much?",
                "options": [
                    "🎨 Creative projects (writing, designing, art)",
                    "🔬 Research and analysis",
                    "👥 Helping and teaching others", 
                    "💼 Leading teams and projects",
                    "🛠️ Building and fixing things",
                    "📊 Working with data and numbers"
                ]
            },
            {
                "question": "In your ideal work environment, you would be:",
                "options": [
                    "🏢 In a structured office setting",
                    "🏠 Working from home flexibly",
                    "🌍 Traveling and meeting people",
                    "🔬 In a lab or research facility",
                    "🎨 In a creative studio space",
                    "🏥 Helping people directly"
                ]
            }
        ],
        "personality": [
            {
                "question": "When facing a big decision, you typically:",
                "options": [
                    "📊 Analyze all data carefully before deciding",
                    "💭 Trust your intuition and gut feeling",
                    "👥 Seek advice from others first",
                    "⚡ Make quick decisions and adapt later",
                    "📝 Create detailed pros and cons lists",
                    "🎯 Focus on long-term outcomes"
                ]
            },
            {
                "question": "You feel most energized when:",
                "options": [
                    "👥 Working with a team on shared goals",
                    "🧘 Working independently with deep focus",
                    "🎤 Presenting ideas to groups",
                    "🤝 Having one-on-one conversations",
                    "🏃 Moving between different tasks",
                    "🔬 Diving deep into complex problems"
                ]
            }
        ],
        "skills": [
            {
                "question": "Which skills do you feel strongest in?",
                "options": [
                    "💻 Technical and analytical skills",
                    "🎨 Creative and artistic abilities",
                    "🤝 Communication and people skills",
                    "📊 Strategic thinking and planning",
                    "🛠️ Practical and hands-on skills",
                    "📚 Research and learning abilities"
                ]
            },
            {
                "question": "What type of challenges excite you most?",
                "options": [
                    "🧩 Complex problem-solving puzzles",
                    "🎯 Meeting ambitious targets",
                    "👥 Improving team dynamics",
                    "💡 Creating innovative solutions",
                    "📈 Growing and scaling projects",
                    "🎨 Expressing ideas creatively"
                ]
            }
        ],
        "goals": [
            {
                "question": "In 5 years, your ideal career achievement would be:",
                "options": [
                    "🚀 Leading a major project or team",
                    "🎓 Becoming an expert in your field",
                    "💰 Achieving financial independence",
                    "🌍 Making a positive impact on society",
                    "⚖️ Achieving excellent work-life balance",
                    "🏆 Being recognized for your expertise"
                ]
            }
        ],
        "values": [
            {
                "question": "What matters most to you in a career?",
                "options": [
                    "💰 Financial security and growth",
                    "🌟 Purpose and meaningful work",
                    "⚖️ Work-life balance and flexibility",
                    "🏆 Recognition and achievement",
                    "🤝 Positive relationships with colleagues",
                    "📚 Continuous learning and growth"
                ]
            }
        ]
    }
    
    return questions_db.get(dimension, [])

def analyze_responses_with_ai(llm, dimension: str, responses: List[str], user_profile: Dict) -> Dict:
    """Use Gemini 2.5 to analyze assessment responses"""
    
    system_prompt = f"""You are an expert career counselor analyzing {dimension} assessment responses.
    
    Based on the user's selections, provide:
    1. Key insights about their {dimension}
    2. Specific career fields that match
    3. Actionable recommendations
    4. Potential growth areas
    
    Be specific, encouraging, and practical. Return in JSON format:
    {{
        "insights": "key insights about their {dimension}",
        "matching_careers": ["career1", "career2", "career3"],
        "recommendations": ["rec1", "rec2", "rec3"],
        "growth_areas": ["area1", "area2"]
    }}
    """
    
    user_message = f"""
    Dimension: {dimension}
    User responses: {responses}
    User name: {user_profile.get('name', 'User')}
    Background: {user_profile.get('background', 'Not specified')}
    
    Please analyze these responses and provide career insights.
    """
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        response = llm.invoke(messages)
        result = json.loads(response.content)
        return result
    except Exception as e:
        st.error(f"Analysis error: {e}")
        return {
            "insights": f"Based on your {dimension} responses, you show strong preferences that can guide your career direction.",
            "matching_careers": ["General roles matching your profile"],
            "recommendations": ["Continue exploring your interests", "Develop your strengths"],
            "growth_areas": ["Professional development", "Skill enhancement"]
        }

def generate_comprehensive_career_insights(llm, all_assessments: Dict, user_profile: Dict) -> Dict:
    """Generate comprehensive career recommendations based on all assessments"""
    
    system_prompt = """You are a senior career counselor creating a comprehensive career roadmap.
    
    Based on ALL assessment dimensions, provide:
    1. Top 3 recommended career paths with specific job titles
    2. Personalized action plan with timeline
    3. Skills to develop
    4. Industry insights and trends
    5. Next immediate steps
    
    Return in JSON format:
    {
        "top_careers": [
            {
                "title": "Career Title",
                "description": "Why this fits",
                "salary_range": "Range",
                "growth_outlook": "Outlook"
            }
        ],
        "action_plan": {
            "immediate": ["step1", "step2"],
            "3_months": ["step1", "step2"],
            "6_months": ["step1", "step2"],
            "1_year": ["step1", "step2"]
        },
        "skills_to_develop": ["skill1", "skill2", "skill3"],
        "industry_insights": "Market trends and opportunities",
        "success_tips": ["tip1", "tip2", "tip3"]
    }
    """
    
    assessment_summary = ""
    for dimension, data in all_assessments.items():
        assessment_summary += f"\n{dimension}: {data.get('insights', 'No insights')}"
        assessment_summary += f" | Careers: {', '.join(data.get('matching_careers', []))}"
    
    user_message = f"""
    User Profile:
    Name: {user_profile.get('name', 'User')}
    Background: {user_profile.get('background', 'Not specified')}
    
    Assessment Results:
    {assessment_summary}
    
    Create a comprehensive career roadmap for this person.
    """
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        response = llm.invoke(messages)
        result = json.loads(response.content)
        return result
    except Exception as e:
        st.error(f"Career insights generation error: {e}")
        return {
            "top_careers": [
                {
                    "title": "Career Path Analysis",
                    "description": "Based on your assessments, you have strong potential in multiple areas",
                    "salary_range": "Competitive",
                    "growth_outlook": "Positive"
                }
            ],
            "action_plan": {
                "immediate": ["Explore recommended career fields", "Network with professionals"],
                "3_months": ["Develop key skills", "Update resume"],
                "6_months": ["Apply for relevant positions", "Build portfolio"],
                "1_year": ["Establish career momentum", "Set advanced goals"]
            },
            "skills_to_develop": ["Professional communication", "Industry knowledge", "Technical skills"],
            "industry_insights": "Continue developing your strengths and exploring opportunities in your areas of interest.",
            "success_tips": ["Stay curious and keep learning", "Build professional relationships", "Set clear goals"]
        }

def main():
    """Main application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Remiro AI Career Assessment</h1>
        <p>Powered by Gemini 1.5 Flash | Discover Your Perfect Career Path</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize LLM
    llm = initialize_llm()
    
    # Sidebar for user info
    with st.sidebar:
        st.markdown("### 👤 Your Information")
        user_name = st.text_input("Your Name", value="")
        user_background = st.selectbox(
            "Background",
            ["Student", "Recent Graduate", "Professional", "Career Changer", "Returning to Work"]
        )
        
        if not user_name:
            st.warning("Please enter your name to begin!")
            st.stop()
    
    user_profile = {
        "name": user_name,
        "background": user_background
    }
    
    # Initialize session state
    if 'current_assessment' not in st.session_state:
        st.session_state.current_assessment = None
    if 'assessment_results' not in st.session_state:
        st.session_state.assessment_results = {}
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    
    # Assessment dimensions
    dimensions = {
        "interests": {"title": "🎨 Interests & Passions", "desc": "What motivates and excites you"},
        "personality": {"title": "🧠 Personality & Work Style", "desc": "How you naturally operate"},
        "skills": {"title": "💪 Skills & Abilities", "desc": "Your current strengths"},
        "goals": {"title": "🎯 Goals & Aspirations", "desc": "Your career dreams"},
        "values": {"title": "💝 Values & Motivations", "desc": "What matters most to you"}
    }
    
    # Progress tracking
    completed_assessments = len(st.session_state.assessment_results)
    total_assessments = len(dimensions)
    progress = completed_assessments / total_assessments if total_assessments > 0 else 0
    
    # Main content
    if completed_assessments == total_assessments:
        # Show comprehensive insights
        st.markdown("## 🎉 Assessment Complete!")
        st.progress(1.0)
        
        if st.button("🚀 Generate My Career Roadmap", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your complete profile..."):
                comprehensive_insights = generate_comprehensive_career_insights(
                    llm, st.session_state.assessment_results, user_profile
                )
                
                st.session_state.career_roadmap = comprehensive_insights
        
        # Display career roadmap if generated
        if 'career_roadmap' in st.session_state:
            roadmap = st.session_state.career_roadmap
            
            st.markdown("""
            <div class="insight-box">
                <h2>🎯 Your Personalized Career Roadmap</h2>
                <p>Based on your comprehensive assessment results</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Top career recommendations
            st.markdown("### 🚀 Top Career Recommendations")
            for i, career in enumerate(roadmap.get('top_careers', []), 1):
                with st.expander(f"🏆 #{i}: {career.get('title', 'Career Option')}"):
                    st.write(f"**Why this fits you:** {career.get('description', 'Great match')}")
                    st.write(f"**Salary Range:** {career.get('salary_range', 'Competitive')}")
                    st.write(f"**Growth Outlook:** {career.get('growth_outlook', 'Positive')}")
            
            # Action plan
            st.markdown("### 📅 Your Action Plan")
            action_plan = roadmap.get('action_plan', {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🎯 Immediate Steps**")
                for step in action_plan.get('immediate', []):
                    st.write(f"• {step}")
                
                st.markdown("**📈 3-Month Goals**")
                for step in action_plan.get('3_months', []):
                    st.write(f"• {step}")
            
            with col2:
                st.markdown("**🚀 6-Month Targets**")
                for step in action_plan.get('6_months', []):
                    st.write(f"• {step}")
                
                st.markdown("**🏆 1-Year Vision**")
                for step in action_plan.get('1_year', []):
                    st.write(f"• {step}")
            
            # Skills and insights
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 💡 Skills to Develop")
                for skill in roadmap.get('skills_to_develop', []):
                    st.write(f"🎯 {skill}")
            
            with col2:
                st.markdown("### 🌟 Success Tips")
                for tip in roadmap.get('success_tips', []):
                    st.write(f"✨ {tip}")
            
            # Industry insights
            st.markdown("### 📊 Industry Insights")
            st.info(roadmap.get('industry_insights', 'Keep developing your skills and stay updated with industry trends.'))
            
            # Reset option
            if st.button("🔄 Take Assessment Again", use_container_width=True):
                for key in ['assessment_results', 'current_assessment', 'current_question_index', 'career_roadmap']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    elif st.session_state.current_assessment:
        # Show current assessment
        dimension = st.session_state.current_assessment
        dimension_info = dimensions[dimension]
        questions = get_assessment_questions(dimension)
        
        st.markdown(f"## {dimension_info['title']}")
        st.write(dimension_info['desc'])
        
        # Progress for this assessment
        current_q = st.session_state.current_question_index
        total_q = len(questions)
        st.progress((current_q) / total_q)
        st.write(f"Question {current_q + 1} of {total_q}")
        
        if current_q < len(questions):
            question_data = questions[current_q]
            
            st.markdown(f"### {question_data['question']}")
            
            # Multiple choice options
            selected_options = []
            for i, option in enumerate(question_data['options']):
                if st.checkbox(option, key=f"q_{current_q}_option_{i}"):
                    selected_options.append(option)
            
            # Custom input
            custom_input = st.text_area("Add your own thoughts:", key=f"custom_{current_q}")
            if custom_input.strip():
                selected_options.append(f"Personal insight: {custom_input.strip()}")
            
            # Navigation
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("➡️ Next Question", disabled=len(selected_options) == 0, use_container_width=True):
                    # Store responses
                    if f'{dimension}_responses' not in st.session_state:
                        st.session_state[f'{dimension}_responses'] = []
                    st.session_state[f'{dimension}_responses'].append(selected_options)
                    
                    st.session_state.current_question_index += 1
                    st.rerun()
        
        else:
            # Assessment complete - analyze
            st.success(f"✅ {dimension_info['title']} Assessment Complete!")
            
            if st.button("🤖 Analyze My Responses", type="primary", use_container_width=True):
                with st.spinner("🧠 AI is analyzing your responses..."):
                    responses = st.session_state.get(f'{dimension}_responses', [])
                    flat_responses = [item for sublist in responses for item in sublist]
                    
                    analysis = analyze_responses_with_ai(llm, dimension, flat_responses, user_profile)
                    st.session_state.assessment_results[dimension] = analysis
                    
                    # Reset for next assessment
                    st.session_state.current_assessment = None
                    st.session_state.current_question_index = 0
                    
                    st.rerun()
    
    else:
        # Show assessment selection
        st.markdown(f"### 🎯 Your Assessment Progress ({completed_assessments}/{total_assessments})")
        if completed_assessments > 0:
            st.progress(progress)
        
        st.markdown("### 📋 Choose Your Next Assessment:")
        
        # Display available assessments
        cols = st.columns(min(3, len(dimensions)))
        for i, (dim_key, dim_info) in enumerate(dimensions.items()):
            col_index = i % len(cols)
            
            with cols[col_index]:
                # Check if completed
                if dim_key in st.session_state.assessment_results:
                    st.success(f"✅ {dim_info['title']}")
                    st.write(dim_info['desc'])
                    
                    # Show quick insights
                    insights = st.session_state.assessment_results[dim_key].get('insights', '')
                    if insights:
                        st.write(f"💡 {insights[:100]}...")
                else:
                    if st.button(f"▶️ {dim_info['title']}", key=f"start_{dim_key}", use_container_width=True):
                        st.session_state.current_assessment = dim_key
                        st.session_state.current_question_index = 0
                        st.rerun()
                    st.write(dim_info['desc'])

if __name__ == "__main__":
    main()
