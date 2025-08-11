"""
State Models for Remiro AI Multi-Agent System

This module defines the data structures and state models used throughout
the Remiro AI career counselling system.
"""

from typing import Dict, List, Optional, Any, Union, TypedDict
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class AssessmentStatus(str, Enum):
    """Status of individual assessments"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class AgentType(str, Enum):
    """Types of agents in the system"""
    MASTER = "master"
    COGNITIVE_ABILITIES = "cognitive_abilities"
    PERSONALITY = "personality"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    PHYSICAL_CONTEXT = "physical_context"
    STRENGTHS_WEAKNESSES = "strengths_weaknesses"
    SKILLS = "skills"
    CONSTRAINTS = "constraints"
    INTERESTS = "interests"
    MOTIVATIONS_VALUES = "motivations_values"
    ASPIRATIONS = "aspirations"
    TRACK_RECORD = "track_record"
    LEARNING_PREFERENCES = "learning_preferences"

class ConversationMessage(BaseModel):
    """Individual conversation message"""
    timestamp: datetime = Field(default_factory=datetime.now)
    role: str = Field(description="user or assistant")
    content: str = Field(description="Message content")
    agent_type: Optional[AgentType] = Field(default=None, description="Which agent generated this message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional message metadata")

class AssessmentData(BaseModel):
    """Base class for assessment data"""
    status: AssessmentStatus = AssessmentStatus.NOT_STARTED
    score: Optional[float] = Field(default=None, ge=0, le=100)
    insights: List[str] = Field(default_factory=list)
    completed_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)

class CognitiveAbilitiesData(AssessmentData):
    """Cognitive abilities assessment data"""
    analytical_thinking: Optional[float] = None
    learning_agility: Optional[float] = None
    memory_retention: Optional[float] = None
    pattern_recognition: Optional[float] = None
    creative_problem_solving: Optional[float] = None

class PersonalityData(AssessmentData):
    """Big Five personality assessment data"""
    openness: Optional[float] = None
    conscientiousness: Optional[float] = None
    extraversion: Optional[float] = None
    agreeableness: Optional[float] = None
    neuroticism: Optional[float] = None
    dominant_traits: List[str] = Field(default_factory=list)

class EmotionalIntelligenceData(AssessmentData):
    """Emotional intelligence assessment data"""
    self_awareness: Optional[float] = None
    self_regulation: Optional[float] = None
    empathy: Optional[float] = None
    social_skills: Optional[float] = None
    motivation: Optional[float] = None

class PhysicalContextData(AssessmentData):
    """Physical work context preferences"""
    work_location_preference: Optional[str] = None  # remote, hybrid, onsite
    environment_type: Optional[str] = None  # indoor, outdoor, mixed
    physical_demands_tolerance: Optional[str] = None  # sedentary, active, manual
    travel_willingness: Optional[str] = None  # none, occasional, frequent
    sensory_preferences: Dict[str, str] = Field(default_factory=dict)

class StrengthsWeaknessesData(AssessmentData):
    """Strengths and weaknesses assessment"""
    energy_givers: List[str] = Field(default_factory=list)
    energy_drains: List[str] = Field(default_factory=list)
    natural_talents: List[str] = Field(default_factory=list)
    growth_areas: List[str] = Field(default_factory=list)
    flow_state_activities: List[str] = Field(default_factory=list)

class SkillsData(AssessmentData):
    """Skills inventory assessment"""
    technical_skills: List[Dict[str, Union[str, int]]] = Field(default_factory=list)
    soft_skills: List[Dict[str, Union[str, int]]] = Field(default_factory=list)
    domain_expertise: List[Dict[str, Union[str, int]]] = Field(default_factory=list)
    tools_technologies: List[Dict[str, Union[str, int]]] = Field(default_factory=list)
    language_skills: List[Dict[str, Union[str, int]]] = Field(default_factory=list)

class ConstraintsData(AssessmentData):
    """Life constraints and limitations"""
    geographic_constraints: List[str] = Field(default_factory=list)
    financial_requirements: Dict[str, Any] = Field(default_factory=dict)
    family_commitments: List[str] = Field(default_factory=list)
    time_constraints: Dict[str, Any] = Field(default_factory=dict)
    health_considerations: List[str] = Field(default_factory=list)

class InterestsData(AssessmentData):
    """Interest areas and passions"""
    subject_interests: List[str] = Field(default_factory=list)
    activity_preferences: List[str] = Field(default_factory=list)
    industry_curiosity: List[str] = Field(default_factory=list)
    problem_areas: List[str] = Field(default_factory=list)
    hobby_connections: List[str] = Field(default_factory=list)

class MotivationsValuesData(AssessmentData):
    """Core motivations and values"""
    primary_motivators: List[str] = Field(default_factory=list)
    core_values: List[str] = Field(default_factory=list)
    work_meaning_sources: List[str] = Field(default_factory=list)
    recognition_preferences: List[str] = Field(default_factory=list)
    autonomy_needs: Dict[str, Any] = Field(default_factory=dict)

class AspirationsData(AssessmentData):
    """Future goals and aspirations"""
    career_vision: Optional[str] = None
    lifestyle_goals: List[str] = Field(default_factory=list)
    impact_aspirations: List[str] = Field(default_factory=list)
    personal_growth_goals: List[str] = Field(default_factory=list)
    work_life_balance_vision: Optional[str] = None

class TrackRecordData(AssessmentData):
    """Educational and professional history"""
    education_background: List[Dict[str, Any]] = Field(default_factory=list)
    work_experience: List[Dict[str, Any]] = Field(default_factory=list)
    projects_accomplishments: List[Dict[str, Any]] = Field(default_factory=list)
    leadership_roles: List[Dict[str, Any]] = Field(default_factory=list)
    patterns_themes: List[str] = Field(default_factory=list)

class LearningPreferencesData(AssessmentData):
    """Learning style and preferences"""
    learning_modality: List[str] = Field(default_factory=list)  # visual, auditory, kinesthetic
    pace_preference: Optional[str] = None  # self-paced, structured
    social_learning_preference: Optional[str] = None  # individual, group, mixed
    feedback_style: Optional[str] = None
    content_format_preferences: List[str] = Field(default_factory=list)

class UserProfile(BaseModel):
    """Complete user profile with all assessments"""
    user_id: str
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Assessment data for each dimension
    cognitive_abilities: CognitiveAbilitiesData = Field(default_factory=CognitiveAbilitiesData)
    personality: PersonalityData = Field(default_factory=PersonalityData)
    emotional_intelligence: EmotionalIntelligenceData = Field(default_factory=EmotionalIntelligenceData)
    physical_context: PhysicalContextData = Field(default_factory=PhysicalContextData)
    strengths_weaknesses: StrengthsWeaknessesData = Field(default_factory=StrengthsWeaknessesData)
    skills: SkillsData = Field(default_factory=SkillsData)
    constraints: ConstraintsData = Field(default_factory=ConstraintsData)
    interests: InterestsData = Field(default_factory=InterestsData)
    motivations_values: MotivationsValuesData = Field(default_factory=MotivationsValuesData)
    aspirations: AspirationsData = Field(default_factory=AspirationsData)
    track_record: TrackRecordData = Field(default_factory=TrackRecordData)
    learning_preferences: LearningPreferencesData = Field(default_factory=LearningPreferencesData)
    
    def get_completion_percentage(self) -> float:
        """Calculate overall profile completion percentage"""
        total_assessments = 12
        completed_assessments = sum(1 for assessment in [
            self.cognitive_abilities, self.personality, self.emotional_intelligence,
            self.physical_context, self.strengths_weaknesses, self.skills,
            self.constraints, self.interests, self.motivations_values,
            self.aspirations, self.track_record, self.learning_preferences
        ] if assessment.status == AssessmentStatus.COMPLETED)
        
        return (completed_assessments / total_assessments) * 100
    
    def get_next_assessment(self) -> Optional[AgentType]:
        """Get the next assessment that needs to be completed"""
        assessment_order = [
            (AgentType.COGNITIVE_ABILITIES, self.cognitive_abilities),
            (AgentType.PERSONALITY, self.personality),
            (AgentType.EMOTIONAL_INTELLIGENCE, self.emotional_intelligence),
            (AgentType.PHYSICAL_CONTEXT, self.physical_context),
            (AgentType.STRENGTHS_WEAKNESSES, self.strengths_weaknesses),
            (AgentType.SKILLS, self.skills),
            (AgentType.CONSTRAINTS, self.constraints),
            (AgentType.INTERESTS, self.interests),
            (AgentType.MOTIVATIONS_VALUES, self.motivations_values),
            (AgentType.ASPIRATIONS, self.aspirations),
            (AgentType.TRACK_RECORD, self.track_record),
            (AgentType.LEARNING_PREFERENCES, self.learning_preferences),
        ]
        
        for agent_type, assessment in assessment_order:
            if assessment.status != AssessmentStatus.COMPLETED:
                return agent_type
        
        return None

class ConversationState(BaseModel):
    """Current state of the conversation"""
    user_profile: UserProfile
    current_agent: AgentType = AgentType.MASTER
    conversation_history: List[ConversationMessage] = Field(default_factory=list)
    session_id: str
    active_assessment: Optional[AgentType] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    
    def add_message(self, role: str, content: str, agent_type: Optional[AgentType] = None):
        """Add a message to the conversation history"""
        message = ConversationMessage(
            role=role,
            content=content,
            agent_type=agent_type or self.current_agent
        )
        self.conversation_history.append(message)
    
    def get_recent_messages(self, count: int = 10) -> List[ConversationMessage]:
        """Get recent messages from conversation history"""
        return self.conversation_history[-count:] if self.conversation_history else []

class WorkflowState(TypedDict):
    """State for LangGraph workflow - using TypedDict for LangGraph compatibility"""
    conversation_state: ConversationState
    next_action: Optional[str]
    should_route_to_agent: bool
    target_agent: Optional[str]  # Changed to string for JSON serialization
    assessment_complete: bool
    career_recommendations: Optional[str]
    last_agent_response: Optional[Dict[str, Any]]
