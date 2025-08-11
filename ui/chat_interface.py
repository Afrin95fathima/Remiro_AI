"""
Chat Interface for Remiro AI

This module provides the main chat interface for interacting with 
the career counselling agents.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

from core.user_manager import UserManager
from core.langgraph_workflow import RemiroWorkflow
from core.state_models import ConversationState, ConversationMessage, AgentType
from ui.components import (
    render_message_bubble, render_typing_indicator, 
    show_error_message, show_success_message
)

class ChatInterface:
    """Main chat interface for Remiro AI"""
    
    def __init__(self, user_manager: UserManager, workflow: RemiroWorkflow):
        self.user_manager = user_manager
        self.workflow = workflow
    
    def render(self):
        """Render the complete chat interface"""
        
        if 'current_user' not in st.session_state or not st.session_state.current_user:
            st.error("No user session found. Please restart the application.")
            return
        
        # Initialize conversation state if needed
        if 'conversation_state' not in st.session_state:
            self._initialize_conversation_state()
        
        # Render chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Chat header
        self._render_chat_header()
        
        # Messages container
        self._render_messages()
        
        # Input area
        self._render_input_area()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _initialize_conversation_state(self):
        """Initialize the conversation state"""
        
        user = st.session_state.current_user
        user_profile = self.user_manager.get_user_profile(user['user_id'])
        
        if not user_profile:
            show_error_message("Failed to load user profile")
            return
        
        # Create conversation state
        conversation_state = ConversationState(
            user_profile=user_profile,
            session_id=str(uuid.uuid4()),
            current_agent=AgentType.MASTER
        )
        
        # Add welcome message
        welcome_message = ConversationMessage(
            role="assistant",
            content=f"Welcome {user['name']}! I'm Remiro AI, your career counsellor. I'm here to help you discover your ideal career path through a comprehensive 12-dimensional assessment. Let's begin this journey together. To start, could you tell me a bit about your current career situation and what brings you here today?",
            agent_type=AgentType.MASTER
        )
        conversation_state.conversation_history.append(welcome_message)
        
        st.session_state.conversation_state = conversation_state
    
    def _render_chat_header(self):
        """Render chat header with agent info"""
        
        conversation_state = st.session_state.conversation_state
        current_agent = conversation_state.current_agent
        
        agent_names = {
            AgentType.MASTER: "Remiro AI",
            AgentType.COGNITIVE_ABILITIES: "Cognitive Abilities Specialist",
            AgentType.PERSONALITY: "Personality Assessment Specialist",
            # Add other agent names as needed
        }
        
        agent_name = agent_names.get(current_agent, "Remiro AI")
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    color: white;
                    text-align: center;">
            <h3 style="margin: 0;">Currently Speaking: {agent_name}</h3>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">
                Assessment Progress: {conversation_state.user_profile.get_completion_percentage():.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_messages(self):
        """Render conversation messages"""
        
        conversation_state = st.session_state.conversation_state
        
        # Create scrollable container for messages
        messages_container = st.container()
        
        with messages_container:
            for i, message in enumerate(conversation_state.conversation_history):
                agent_name = "You" if message.role == "user" else self._get_agent_display_name(message.agent_type)
                render_message_bubble(
                    message.content,
                    is_user=(message.role == "user"),
                    agent_name=agent_name
                )
                
                # Check if this is the last assistant message and has interactive options
                if (message.role == "assistant" and 
                    i == len(conversation_state.conversation_history) - 1 and
                    hasattr(st.session_state, 'last_agent_response') and
                    st.session_state.last_agent_response and
                    'interactive_options' in st.session_state.last_agent_response):
                    
                    self._render_interactive_options(st.session_state.last_agent_response)
    
    def _render_input_area(self):
        """Render message input area"""
        
        # Create input form
        with st.form(key="message_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_area(
                    "Your message:",
                    placeholder="Share your thoughts and responses...",
                    height=100,
                    label_visibility="collapsed"
                )
            
            with col2:
                submit_button = st.form_submit_button(
                    "Send",
                    use_container_width=True,
                    type="primary"
                )
            
            # Process message when submitted
            if submit_button and user_input.strip():
                self._process_user_message(user_input.strip())
    
    def _render_interactive_options(self, agent_response):
        """Render interactive multiple choice options with enhancement workflow"""
        
        if 'interactive_options' not in agent_response:
            return
        
        st.markdown("---")
        st.markdown("**Please select your answer:**")
        
        options = agent_response['interactive_options']
        question_type = agent_response.get('question_type', 'multiple_choice')
        
        # Create unique key for this question
        unique_key = f"interactive_{len(st.session_state.conversation_state.conversation_history)}"
        
        # Initialize session state for enhancement workflow
        if f"enhancement_step_{unique_key}" not in st.session_state:
            st.session_state[f"enhancement_step_{unique_key}"] = "selection"
        
        if f"selected_options_{unique_key}" not in st.session_state:
            st.session_state[f"selected_options_{unique_key}"] = []
        
        current_step = st.session_state[f"enhancement_step_{unique_key}"]
        
        if current_step == "selection":
            # Step 1: Option Selection
            if question_type == "multiple_choice":
                # Radio buttons for single selection
                selected_option = st.radio(
                    "Choose one option:",
                    options,
                    key=unique_key,
                    label_visibility="collapsed"
                )
                
                if selected_option:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("Enhance My Answer", key=f"enhance_{unique_key}"):
                            st.session_state[f"selected_options_{unique_key}"] = [selected_option]
                            st.session_state[f"enhancement_step_{unique_key}"] = "enhancement"
                            st.rerun()
                    
                    with col2:
                        if st.button("Submit As-Is", key=f"submit_direct_{unique_key}"):
                            self._process_user_message(selected_option)
                            self._clear_enhancement_session(unique_key)
                            st.rerun()
            
            elif question_type == "multiple_select":
                # Checkboxes for multiple selection
                st.markdown("Select all that apply:")
                selected_options = []
                
                for i, option in enumerate(options):
                    if st.checkbox(option, key=f"{unique_key}_{i}"):
                        selected_options.append(option)
                
                if selected_options:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("Enhance My Answers", key=f"enhance_{unique_key}"):
                            st.session_state[f"selected_options_{unique_key}"] = selected_options
                            st.session_state[f"enhancement_step_{unique_key}"] = "enhancement"
                            st.rerun()
                    
                    with col2:
                        if st.button("Submit As-Is", key=f"submit_direct_{unique_key}"):
                            response_text = "I selected: " + ", ".join(selected_options)
                            self._process_user_message(response_text)
                            self._clear_enhancement_session(unique_key)
                            st.rerun()
        
        elif current_step == "enhancement":
            # Step 2: Enhancement Display and Editing
            selected_options = st.session_state[f"selected_options_{unique_key}"]
            
            # Generate enhanced answer
            enhanced_answer = self._generate_enhanced_answer(selected_options, agent_response)
            
            st.markdown("**Your Enhanced Answer:**")
            st.info("Based on your selections, here's an enhanced response:")
            
            # Allow user to edit the enhanced answer
            final_answer = st.text_area(
                "You can edit this enhanced answer if needed:",
                value=enhanced_answer,
                height=150,
                key=f"enhanced_text_{unique_key}"
            )
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("Submit Enhanced Answer", key=f"submit_enhanced_{unique_key}"):
                    self._process_user_message(final_answer)
                    self._clear_enhancement_session(unique_key)
                    st.rerun()
            
            with col2:
                if st.button("Go Back to Selection", key=f"back_{unique_key}"):
                    st.session_state[f"enhancement_step_{unique_key}"] = "selection"
                    st.rerun()
            
            with col3:
                if st.button("Generate New Enhancement", key=f"regenerate_{unique_key}"):
                    # Force regeneration of enhanced answer
                    st.rerun()
    def _process_user_message(self, message: str):
        """Process user message through the workflow"""
        
        conversation_state = st.session_state.conversation_state
        
        # Show typing indicator
        with st.spinner("Remiro AI is thinking..."):
            try:
                # Process message through workflow
                result = self.workflow.process_message_sync(conversation_state, message)
                
                if result["success"]:
                    # Update current agent
                    if result.get("agent_type"):
                        try:
                            conversation_state.current_agent = AgentType(result["agent_type"])
                        except ValueError:
                            conversation_state.current_agent = AgentType.MASTER
                    
                    # Update user profile
                    self.user_manager.update_user_profile(conversation_state.user_profile)
                    
                    # Save conversation
                    self.user_manager.save_conversation(
                        conversation_state.user_profile.user_id,
                        conversation_state.session_id,
                        conversation_state.conversation_history
                    )
                    
                    # Store agent response for interactive options
                    if result.get("agent_response"):
                        st.session_state.last_agent_response = result["agent_response"]
                    else:
                        # Clear any previous interactive options
                        if hasattr(st.session_state, 'last_agent_response'):
                            del st.session_state.last_agent_response
                    
                    # Show success feedback
                    if result.get("assessment_complete"):
                        show_success_message("Assessment section completed!")
                    
                    # Rerun to show new message
                    st.rerun()
                    
                else:
                    show_error_message(result.get("error", "Failed to process message"))
                    
            except Exception as e:
                show_error_message(f"Error processing message: {str(e)}")
    
    def _get_agent_display_name(self, agent_type: Optional[AgentType]) -> str:
        """Get display name for agent"""
        
        agent_names = {
            AgentType.MASTER: "Remiro AI",
            AgentType.COGNITIVE_ABILITIES: "Cognitive Abilities Specialist",
            AgentType.PERSONALITY: "Personality Specialist",
            AgentType.EMOTIONAL_INTELLIGENCE: "Emotional Intelligence Specialist",
            AgentType.PHYSICAL_CONTEXT: "Work Environment Specialist",
            AgentType.STRENGTHS_WEAKNESSES: "Strengths & Weaknesses Specialist",
            AgentType.SKILLS: "Skills Assessment Specialist",
            AgentType.CONSTRAINTS: "Constraints Analysis Specialist",
            AgentType.INTERESTS: "Interests Mapping Specialist",
            AgentType.MOTIVATIONS_VALUES: "Values Assessment Specialist",
            AgentType.ASPIRATIONS: "Aspirations Specialist",
            AgentType.TRACK_RECORD: "Background Assessment Specialist",
            AgentType.LEARNING_PREFERENCES: "Learning Preferences Specialist",
        }
        
        return agent_names.get(agent_type, "Remiro AI") if agent_type else "Remiro AI"
    
    def _generate_enhanced_answer(self, selected_options: List[str], agent_response: Dict[str, Any]) -> str:
        """Generate an enhanced answer based on selected options"""
        
        # Get the original question from the agent response
        original_question = agent_response.get("message", "")
        
        # Create a comprehensive answer by combining the selected options
        if len(selected_options) == 1:
            enhanced_answer = f"When it comes to {self._extract_question_topic(original_question)}, I primarily {selected_options[0].lower()}. This approach works well for me because it aligns with my natural problem-solving style and has proven effective in various situations I've encountered."
        
        else:
            # Multiple selections - create a more detailed response
            primary_approach = selected_options[0]
            secondary_approaches = selected_options[1:]
            
            enhanced_answer = f"My approach to {self._extract_question_topic(original_question)} is multifaceted. My primary method involves {primary_approach.lower()}, which forms the foundation of how I tackle challenges."
            
            if len(secondary_approaches) == 1:
                enhanced_answer += f" Additionally, I also {secondary_approaches[0].lower()}, as this complementary approach helps me achieve better results."
            else:
                enhanced_answer += f" I also incorporate several other strategies: {', '.join([approach.lower() for approach in secondary_approaches[:-1]])}, and {secondary_approaches[-1].lower()}. This combination of approaches allows me to be flexible and adaptive depending on the specific situation."
            
            enhanced_answer += f" By utilizing these different methods, I can leverage my strengths while addressing various aspects of the challenge at hand."
        
        return enhanced_answer
    
    def _extract_question_topic(self, question: str) -> str:
        """Extract the main topic from a question for enhanced answer generation"""
        
        # Simple keyword extraction for common topics
        topic_keywords = {
            "problem": "problem-solving",
            "learn": "learning new concepts",
            "remember": "remembering information", 
            "analytical": "analytical thinking",
            "creative": "creative problem-solving",
            "approach": "approaching challenges",
            "style": "working style",
            "preference": "preferences"
        }
        
        question_lower = question.lower()
        for keyword, topic in topic_keywords.items():
            if keyword in question_lower:
                return topic
        
        return "this area"
    
    def _clear_enhancement_session(self, unique_key: str):
        """Clear enhancement session state variables"""
        
        keys_to_clear = [
            f"enhancement_step_{unique_key}",
            f"selected_options_{unique_key}",
            f"enhanced_text_{unique_key}"
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        # Clear the interactive options after submission
        if hasattr(st.session_state, 'last_agent_response'):
            del st.session_state.last_agent_response
