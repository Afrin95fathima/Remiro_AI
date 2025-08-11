"""
LangGraph Workflow for Remiro AI Multi-Agent System

This module orchestrates the conversation flow between the master agent
and 12 specialized agents using LangGraph for sophisticated state management.
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

from core.state_models import (
    WorkflowState, ConversationState, AgentType, AssessmentStatus
)
from agents.master_agent import MasterAgent
from agents.cognitive_abilities import CognitiveAbilitiesAgent
from agents.personality import PersonalityAgent
from agents.emotional_intelligence import EmotionalIntelligenceAgent
from agents.physical_context import PhysicalContextAgent
from agents.strengths_weaknesses import StrengthsWeaknessesAgent
from agents.skills import SkillsAgent
from agents.constraints import ConstraintsAgent
from agents.interests import InterestsAgent
from agents.motivations_values import MotivationsValuesAgent
from agents.aspirations import AspirationsAgent
from agents.track_record import TrackRecordAgent
from agents.learning_preferences import LearningPreferencesAgent

class RemiroWorkflow:
    """Main workflow orchestrator for Remiro AI"""
    
    def __init__(self):
        # Load environment variables explicitly
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Initialize LLM with proper configuration
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_key,
            temperature=0.7,
            max_tokens=2048
        )
        
        # Initialize agents
        self.master_agent = MasterAgent(self.llm)
        self.agents = {
            AgentType.COGNITIVE_ABILITIES: CognitiveAbilitiesAgent(self.llm),
            AgentType.PERSONALITY: PersonalityAgent(self.llm),
            AgentType.EMOTIONAL_INTELLIGENCE: EmotionalIntelligenceAgent(self.llm),
            AgentType.PHYSICAL_CONTEXT: PhysicalContextAgent(self.llm),
            AgentType.STRENGTHS_WEAKNESSES: StrengthsWeaknessesAgent(self.llm),
            AgentType.SKILLS: SkillsAgent(self.llm),
            AgentType.CONSTRAINTS: ConstraintsAgent(self.llm),
            AgentType.INTERESTS: InterestsAgent(self.llm),
            AgentType.MOTIVATIONS_VALUES: MotivationsValuesAgent(self.llm),
            AgentType.ASPIRATIONS: AspirationsAgent(self.llm),
            AgentType.TRACK_RECORD: TrackRecordAgent(self.llm),
            AgentType.LEARNING_PREFERENCES: LearningPreferencesAgent(self.llm),
        }
        
        # Initialize memory saver for state persistence
        self.memory = MemorySaver()
        
        # Build workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Define workflow graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("master_router", self._master_router_node)
        workflow.add_node("specialized_agent", self._specialized_agent_node)
        workflow.add_node("synthesis", self._synthesis_node)
        
        # Define edges
        workflow.add_conditional_edges(
            "master_router",
            self._route_decision,
            {
                "specialized_agent": "specialized_agent",
                "synthesis": "synthesis",
                END: END
            }
        )
        workflow.add_edge("specialized_agent", "synthesis")
        workflow.add_edge("synthesis", END)
        
        # Set entry point
        workflow.set_entry_point("master_router")
        
        return workflow.compile(checkpointer=self.memory)
    
    def _master_router_node(self, state: WorkflowState) -> WorkflowState:
        """Master agent routing node"""
        try:
            conversation_state = state["conversation_state"]
            
            # Get the latest user message
            recent_messages = conversation_state.get_recent_messages(5)
            user_message = None
            for msg in reversed(recent_messages):
                if msg.role == "user":
                    user_message = msg.content
                    break
            
            if not user_message:
                state["next_action"] = "master_response"
                # Add a fallback response
                fallback_message = "I'm here to help you with your career assessment. Could you tell me about your current career situation?"
                conversation_state.add_message("assistant", fallback_message, AgentType.MASTER)
                return state
            
            # Master agent determines routing
            routing_decision = self.master_agent.route_conversation(
                user_message, 
                conversation_state.user_profile,
                recent_messages
            )
            
            # Ensure routing_decision is a dict
            if not isinstance(routing_decision, dict):
                routing_decision = {"should_route_to_agent": False, "target_agent": None}
            
            # Update state based on routing decision
            if routing_decision.get("should_route_to_agent", False):
                target_agent = routing_decision.get("target_agent")
                if target_agent:
                    # Store agent type as string for TypedDict compatibility
                    state["should_route_to_agent"] = True
                    state["target_agent"] = target_agent  # Keep as string
                    state["next_action"] = "route_to_specialist"
                else:
                    state["should_route_to_agent"] = False
                    state["next_action"] = "master_response"
            else:
                state["should_route_to_agent"] = False
                state["next_action"] = "master_response"
                
                # Generate master agent response
                master_response = self.master_agent.generate_response(
                    user_message,
                    conversation_state.user_profile,
                    recent_messages
                )
                
                # Ensure we have a valid response
                if not master_response or not isinstance(master_response, str):
                    master_response = "Thank you for sharing that. Let me ask you another question to better understand your career preferences and goals."
                
                # Add response to conversation
                conversation_state.add_message("assistant", master_response, AgentType.MASTER)
            
            return state
            
        except Exception as e:
            print(f"Error in master router node: {e}")
            # Provide fallback response
            fallback_message = "I appreciate you sharing that with me. Let's continue with your career assessment. What aspects of work do you find most engaging?"
            state["conversation_state"].add_message("assistant", fallback_message, AgentType.MASTER)
            state["next_action"] = "master_response"
            return state
    
    def _specialized_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Specialized agent processing node"""
        try:
            target_agent_str = state["target_agent"]
            if not target_agent_str or target_agent_str not in self.agents:
                # Fallback to master response
                fallback_message = "Let me continue helping you with your career assessment. What would you like to explore next?"
                state["conversation_state"].add_message("assistant", fallback_message, AgentType.MASTER)
                state["next_action"] = "synthesis"
                return state
            
            conversation_state = state["conversation_state"]
            specialized_agent = self.agents[target_agent_str]
            
            # Get the latest user message
            recent_messages = conversation_state.get_recent_messages(5)
            user_message = None
            for msg in reversed(recent_messages):
                if msg.role == "user":
                    user_message = msg.content
                    break
            
            if not user_message:
                # Provide a fallback question from the specialist
                agent_name = self._get_agent_display_name_from_string(target_agent_str)
                fallback_message = f"As your {agent_name}, I'd like to learn more about you. Could you share your thoughts on this topic?"
                conversation_state.add_message("assistant", fallback_message, AgentType(target_agent_str))
                state["next_action"] = "synthesis"
                return state
            
            # Process with specialized agent
            agent_response = specialized_agent.process_interaction(
                user_message,
                conversation_state.user_profile,
                recent_messages
            )
            
            # Ensure we have a valid response
            if not isinstance(agent_response, dict):
                agent_response = {
                    "message": "Thank you for sharing that. Let me ask you another question to better understand this aspect of your profile.",
                    "assessment_complete": False
                }
            
            # Store the full agent response for interactive options
            state["last_agent_response"] = agent_response
            
            # Add agent response to conversation
            response_message = agent_response.get("message", "Thank you for that insight.")
            conversation_state.add_message("assistant", response_message, AgentType(target_agent_str))
            
            # Update user profile if assessment data provided
            if agent_response.get("assessment_data"):
                self._update_profile_assessment(
                    conversation_state.user_profile,
                    AgentType(target_agent_str),
                    agent_response["assessment_data"]
                )
            
            # Check if assessment is complete
            if agent_response.get("assessment_complete", False):
                state["assessment_complete"] = True
                
            state["next_action"] = "synthesis"
            return state
            
        except Exception as e:
            print(f"Error in specialized agent node: {e}")
            # Provide fallback response
            fallback_message = "Thank you for sharing that information. Let's continue with your assessment."
            state["conversation_state"].add_message("assistant", fallback_message, AgentType.MASTER)
            state["next_action"] = "synthesis"
            return state
        
        # Check if assessment is complete
        if agent_response.get("assessment_complete", False):
            state.assessment_complete = True
        
        return state
    
    def _synthesis_node(self, state: WorkflowState) -> WorkflowState:
        """Synthesis and final processing node with error handling"""
        try:
            conversation_state = state["conversation_state"]
            
            # Check if all assessments are complete
            if conversation_state.user_profile.get_completion_percentage() == 100:
                try:
                    # Generate career recommendations
                    career_recommendations = self.master_agent.generate_career_recommendations(
                        conversation_state.user_profile
                    )
                    state["career_recommendations"] = career_recommendations
                except Exception as e:
                    print(f"Error generating career recommendations: {e}")
                    # Provide fallback career guidance
                    state["career_recommendations"] = [
                        "Based on your assessment, I recommend exploring careers that align with your strengths.",
                        "Consider seeking additional career counseling to develop a personalized career plan.",
                        "Focus on developing skills in areas where you showed strong aptitude."
                    ]
            
            state["next_action"] = "complete"
            return state
            
        except Exception as e:
            print(f"Error in synthesis node: {e}")
            # Return a valid WorkflowState with error handling
            state["conversation_state"].current_message = "I'm completing your assessment. Thank you for your responses."
            state["next_action"] = "complete"
            return state
    
    def _route_decision(self, state: WorkflowState) -> str:
        """Decide routing based on state"""
        next_action = state.get("next_action")
        if next_action == "route_to_specialist":
            return "specialized_agent"
        elif next_action == "master_response":
            return "synthesis"
        else:
            return END
    
    def _update_profile_assessment(self, user_profile, agent_type: AgentType, assessment_data: Dict[str, Any]):
        """Update user profile with assessment data"""
        assessment_mapping = {
            AgentType.COGNITIVE_ABILITIES: user_profile.cognitive_abilities,
            AgentType.PERSONALITY: user_profile.personality,
            AgentType.EMOTIONAL_INTELLIGENCE: user_profile.emotional_intelligence,
            AgentType.PHYSICAL_CONTEXT: user_profile.physical_context,
            AgentType.STRENGTHS_WEAKNESSES: user_profile.strengths_weaknesses,
            AgentType.SKILLS: user_profile.skills,
            AgentType.CONSTRAINTS: user_profile.constraints,
            AgentType.INTERESTS: user_profile.interests,
            AgentType.MOTIVATIONS_VALUES: user_profile.motivations_values,
            AgentType.ASPIRATIONS: user_profile.aspirations,
            AgentType.TRACK_RECORD: user_profile.track_record,
            AgentType.LEARNING_PREFERENCES: user_profile.learning_preferences,
        }
        
        if agent_type in assessment_mapping:
            assessment = assessment_mapping[agent_type]
            
            # Update assessment data
            for key, value in assessment_data.items():
                if hasattr(assessment, key):
                    setattr(assessment, key, value)
            
            # Mark as completed if indicated
            if assessment_data.get("status") == "completed":
                assessment.status = AssessmentStatus.COMPLETED
                assessment.completed_at = assessment_data.get("completed_at")
    
    async def process_message(self, conversation_state: ConversationState, message: str) -> Dict[str, Any]:
        """Process a user message through the workflow"""
        try:
            # Add user message to conversation
            conversation_state.add_message("user", message)
            
            # Create workflow state using TypedDict format
            workflow_state: WorkflowState = {
                "conversation_state": conversation_state,
                "next_action": "master_router",
                "should_route_to_agent": False,
                "target_agent": None,
                "assessment_complete": False,
                "career_recommendations": None,
                "last_agent_response": None
            }
            
            # Run workflow
            config = {"configurable": {"thread_id": conversation_state.session_id}}
            result = await self.workflow.ainvoke(workflow_state, config=config)
            
            # Get the latest assistant message
            recent_messages = conversation_state.get_recent_messages(1)
            assistant_message = None
            if recent_messages and recent_messages[-1].role == "assistant":
                assistant_message = recent_messages[-1]
            
            return {
                "success": True,
                "message": assistant_message.content if assistant_message else "I apologize, but I encountered an issue processing your message.",
                "agent_type": assistant_message.agent_type.value if assistant_message and assistant_message.agent_type else "master",
                "assessment_complete": result.assessment_complete,
                "career_recommendations": result.career_recommendations,
                "profile_completion": conversation_state.user_profile.get_completion_percentage(),
                "next_assessment": conversation_state.user_profile.get_next_assessment()
            }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return {
                "success": False,
                "message": "I apologize, but I encountered an error processing your message. Please try again.",
                "error": str(e)
            }
    
    def process_message_sync(self, conversation_state: ConversationState, message: str) -> Dict[str, Any]:
        """Synchronous version of process_message for Streamlit compatibility"""
        try:
            # Add user message to conversation
            conversation_state.add_message("user", message)
            
            # Create workflow state using TypedDict format
            workflow_state: WorkflowState = {
                "conversation_state": conversation_state,
                "next_action": "master_router",
                "should_route_to_agent": False,
                "target_agent": None,
                "assessment_complete": False,
                "career_recommendations": None,
                "last_agent_response": None
            }
            
            # Run workflow synchronously
            config = {"configurable": {"thread_id": conversation_state.session_id}}
            result = self.workflow.invoke(workflow_state, config=config)
            
            # For TypedDict, check if it's a dictionary with required keys
            if not isinstance(result, dict) or "conversation_state" not in result:
                return {
                    "success": False,
                    "message": "I apologize, but I encountered an issue processing your message. Please try again.",
                    "error": "Invalid workflow result type"
                }
            
            # Get the latest assistant message
            conversation_state = result["conversation_state"]
            recent_messages = conversation_state.get_recent_messages(1)
            assistant_message = None
            if recent_messages and recent_messages[-1].role == "assistant":
                assistant_message = recent_messages[-1]
            
            return {
                "success": True,
                "message": assistant_message.content if assistant_message else "Hello! I'm here to help you with your career assessment. What would you like to discuss?",
                "agent_type": assistant_message.agent_type.value if assistant_message and assistant_message.agent_type else "master",
                "assessment_complete": result.get("assessment_complete", False),
                "career_recommendations": result.get("career_recommendations", None),
                "profile_completion": conversation_state.user_profile.get_completion_percentage(),
                "next_assessment": conversation_state.user_profile.get_next_assessment().value if conversation_state.user_profile.get_next_assessment() else None,
                "agent_response": result.get("last_agent_response", None)
            }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            # Add a fallback response to the conversation
            fallback_message = "I apologize, but I'm having trouble connecting to my AI services right now. Let me ask you a simple question to get started: What is your current career situation, and what are you hoping to achieve through this assessment?"
            conversation_state.add_message("assistant", fallback_message, AgentType.MASTER)
            
            return {
                "success": True,  # Still return success to continue conversation
                "message": fallback_message,
                "agent_type": "master",
                "assessment_complete": False,
                "error": str(e)
            }
    
    def _get_agent_display_name_from_string(self, agent_str: str) -> str:
        """Get display name for agent from string"""
        agent_names = {
            "cognitive_abilities": "Cognitive Abilities Specialist",
            "personality": "Personality Specialist", 
            "emotional_intelligence": "Emotional Intelligence Specialist",
            "physical_context": "Work Environment Specialist",
            "strengths_weaknesses": "Strengths & Weaknesses Specialist",
            "skills": "Skills Assessment Specialist",
            "constraints": "Constraints Analysis Specialist",
            "interests": "Interests Mapping Specialist",
            "motivations_values": "Values Assessment Specialist",
            "aspirations": "Aspirations Specialist",
            "track_record": "Background Assessment Specialist",
            "learning_preferences": "Learning Preferences Specialist",
        }
        return agent_names.get(agent_str, "Career Specialist")
