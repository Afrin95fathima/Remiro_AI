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

# Add this to the app.py file temporarily to test
def main_enhanced():
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
    main_enhanced()  # Use the new enhanced main function
