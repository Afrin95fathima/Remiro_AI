"""
Agent Integration System for Interactive Assessment
Combines checkbox questions with real AI agent responses
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import json
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.interests import InterestsAgent
from agents.skills import SkillsAgent  
from agents.personality import PersonalityAgent
from agents.aspirations import AspirationsAgent
from agents.motivations_values import MotivationsValuesAgent
from agents.cognitive_abilities import CognitiveAbilitiesAgent
from agents.strengths_weaknesses import StrengthsWeaknessesAgent
from agents.learning_preferences import LearningPreferencesAgent
from agents.track_record import TrackRecordAgent
from agents.emotional_intelligence import EmotionalIntelligenceAgent
from agents.constraints import ConstraintsAgent
from agents.physical_context import PhysicalContextAgent

class AgentIntegrationSystem:
    """Integrates checkbox questions with real AI agent responses"""
    
    def __init__(self, llm):
        self.llm = llm
        self.agents = {}
        self.initialize_agents()
        
    def initialize_agents(self):
        """Initialize all 12 specialized agents"""
        try:
            self.agents = {
                'interests': InterestsAgent(self.llm),
                'skills': SkillsAgent(self.llm),
                'personality': PersonalityAgent(self.llm),
                'aspirations': AspirationsAgent(self.llm),
                'motivations_values': MotivationsValuesAgent(self.llm),
                'cognitive_abilities': CognitiveAbilitiesAgent(self.llm),
                'strengths_weaknesses': StrengthsWeaknessesAgent(self.llm),
                'learning_preferences': LearningPreferencesAgent(self.llm),
                'track_record': TrackRecordAgent(self.llm),
                'emotional_intelligence': EmotionalIntelligenceAgent(self.llm),
                'constraints': ConstraintsAgent(self.llm),
                'physical_context': PhysicalContextAgent(self.llm)
            }
        except Exception as e:
            st.error(f"Error initializing agents: {e}")
            # Fallback to empty dict
            self.agents = {}
    
    def get_agent_response(self, agent_type: str, user_responses: List[str], user_profile: Dict) -> Dict[str, Any]:
        """Get AI-powered response from specific agent based on user selections"""
        
        if agent_type not in self.agents:
            return {"error": f"Agent {agent_type} not available"}
        
        try:
            agent = self.agents[agent_type]
            
            # Convert checkbox responses to natural language for agent
            response_text = self.format_responses_for_agent(agent_type, user_responses)
            
            # Create interaction data
            interaction_data = {
                "user_background": user_profile.get("background", "Professional"),
                "user_responses": response_text,
                "user_context": user_profile.get("context", {}),
                "session_data": {
                    "timestamp": datetime.now().isoformat(),
                    "agent_type": agent_type,
                    "response_format": "checkbox_integration"
                }
            }
            
            # Get agent's professional response
            agent_response = agent.process_interaction(interaction_data)
            
            return agent_response
            
        except Exception as e:
            return {
                "error": f"Error getting response from {agent_type} agent: {str(e)}",
                "fallback_message": f"Thank you for sharing your {agent_type.replace('_', ' ')} information. This helps us understand you better for career recommendations."
            }
    
    def format_responses_for_agent(self, agent_type: str, user_responses: List[str]) -> str:
        """Convert checkbox selections to natural language for agent processing"""
        
        if not user_responses:
            return "No specific preferences selected."
        
        # Create a natural language summary based on agent type
        response_formatters = {
            'interests': lambda responses: f"I am interested in: {', '.join(responses)}. These are the areas that genuinely capture my attention and excitement.",
            'skills': lambda responses: f"My key skills and capabilities include: {', '.join(responses)}. These represent areas where I feel confident and competent.",
            'personality': lambda responses: f"My personality traits include: {', '.join(responses)}. This reflects how I naturally approach work and relationships.",
            'aspirations': lambda responses: f"My career aspirations involve: {', '.join(responses)}. These represent what I hope to achieve in my professional life.",
            'motivations_values': lambda responses: f"I am motivated by and value: {', '.join(responses)}. These are the driving forces behind my career decisions.",
            'cognitive_abilities': lambda responses: f"My cognitive strengths include: {', '.join(responses)}. These are the thinking styles and mental processes I excel at.",
            'strengths_weaknesses': lambda responses: f"Key aspects of my professional profile: {', '.join(responses)}. These represent both my strengths and areas for development.",
            'learning_preferences': lambda responses: f"My preferred learning styles are: {', '.join(responses)}. This is how I best absorb and process new information.",
            'track_record': lambda responses: f"My experience includes: {', '.join(responses)}. These represent my background and achievements to date.",
            'emotional_intelligence': lambda responses: f"My emotional and social capabilities include: {', '.join(responses)}. This reflects how I handle emotions and relationships.",
            'constraints': lambda responses: f"My current constraints and considerations are: {', '.join(responses)}. These factors influence my career decisions.",
            'physical_context': lambda responses: f"My work environment preferences include: {', '.join(responses)}. These are the physical and logistical factors that matter to me."
        }
        
        formatter = response_formatters.get(agent_type, lambda responses: f"Selected preferences: {', '.join(responses)}")
        return formatter(user_responses)
    
    def render_agent_response(self, agent_type: str, agent_response: Dict[str, Any]):
        """Render the AI agent's response in the UI"""
        
        if "error" in agent_response:
            st.error(f"Agent Response Error: {agent_response['error']}")
            if "fallback_message" in agent_response:
                st.info(agent_response["fallback_message"])
            return
        
        # Get agent display name
        agent_names = {
            'interests': '🎯 Career Interests Counselor',
            'skills': '🛠️ Skills Assessment Expert', 
            'personality': '👤 Personality Insights Advisor',
            'aspirations': '🌟 Career Aspirations Guide',
            'motivations_values': '💝 Values & Motivations Counselor',
            'cognitive_abilities': '🧠 Cognitive Abilities Analyst',
            'strengths_weaknesses': '⚖️ Strengths & Development Coach',
            'learning_preferences': '📚 Learning Style Expert',
            'track_record': '📈 Experience & Achievement Advisor',
            'emotional_intelligence': '🤝 Emotional Intelligence Coach',
            'constraints': '🎚️ Career Constraints Counselor',
            'physical_context': '🏢 Work Environment Specialist'
        }
        
        agent_name = agent_names.get(agent_type, f"{agent_type.replace('_', ' ').title()} Agent")
        
        # Display agent response
        with st.container():
            st.markdown(f"""
            <div style="background: #2a2a2a; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #0084ff;">
                <h4 style="color: #00ff84; margin-bottom: 15px;">{agent_name}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Display main message
            if "message" in agent_response:
                st.markdown(f"""
                <div style="background: #3a3a3a; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <p style="color: #ffffff; line-height: 1.6; margin: 0;">
                        {agent_response['message']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display assessment insights if available
            if "assessment_data" in agent_response and agent_response["assessment_data"]:
                assessment_data = agent_response["assessment_data"]
                
                if "insights" in assessment_data:
                    st.markdown("**🔍 Key Insights:**")
                    for insight in assessment_data["insights"]:
                        st.markdown(f"• {insight}")
                
                if "recommendations" in assessment_data:
                    st.markdown("**💡 Recommendations:**")
                    for rec in assessment_data["recommendations"]:
                        st.markdown(f"• {rec}")
                
                if "career_connections" in assessment_data:
                    st.markdown("**🎯 Career Connections:**")
                    for connection in assessment_data["career_connections"]:
                        st.markdown(f"• {connection}")
    
    def get_comprehensive_analysis(self, all_responses: Dict[str, List]) -> Dict[str, Any]:
        """Generate comprehensive career analysis using all agent responses"""
        
        try:
            # Collect insights from all agents
            all_insights = []
            all_recommendations = []
            career_matches = []
            
            for agent_type, responses in all_responses.items():
                if responses and agent_type in self.agents:
                    # Get agent analysis
                    user_profile = {"background": "Professional", "context": {}}
                    agent_response = self.get_agent_response(agent_type, responses, user_profile)
                    
                    if "assessment_data" in agent_response:
                        assessment = agent_response["assessment_data"]
                        if "insights" in assessment:
                            all_insights.extend(assessment["insights"])
                        if "recommendations" in assessment:
                            all_recommendations.extend(assessment["recommendations"])
                        if "career_connections" in assessment:
                            career_matches.extend(assessment["career_connections"])
            
            # Generate consolidated analysis
            return {
                "comprehensive_insights": all_insights[:10],  # Top 10 insights
                "key_recommendations": all_recommendations[:8],  # Top 8 recommendations  
                "career_matches": career_matches[:15],  # Top 15 career connections
                "summary": "Based on your comprehensive 12-dimensional assessment, we've analyzed your interests, skills, personality, aspirations, and all other key factors to provide personalized career guidance.",
                "next_steps": [
                    "Review the career connections that align with your profile",
                    "Consider the key recommendations for your professional development",
                    "Explore the specific insights about your career preferences",
                    "Take action on the most relevant suggestions for your situation"
                ]
            }
            
        except Exception as e:
            return {
                "error": f"Error generating comprehensive analysis: {str(e)}",
                "fallback_summary": "Your responses have been collected and provide valuable insights for career planning."
            }