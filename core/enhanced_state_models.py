"""
Enhanced State Models for Remiro AI Advanced Career Assessment System

Updated state models to support the new 12D assessment architecture with
empathetic conversations, comprehensive analysis, and career roadmaps.
"""

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class AssessmentStatus(str, Enum):
    """Assessment status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ConversationRole(str, Enum):
    """Conversation participant roles"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ResponseType(str, Enum):
    """Types of responses from the system"""
    GENERAL_RESPONSE = "general_response"
    ASSESSMENT_QUESTION = "assessment_question"
    ASSESSMENT_COMPLETE = "assessment_complete"
    CAREER_ANALYSIS = "career_analysis"
    ERROR_RESPONSE = "error_response"

class EmotionalTone(str, Enum):
    """Detected emotional tones"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

# Enhanced Conversation Models
class ConversationMessage(BaseModel):
    """Individual conversation message"""
    role: ConversationRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    emotional_tone: Optional[EmotionalTone] = None
    intent: Optional[str] = None

class ConversationHistory(BaseModel):
    """Complete conversation history"""
    messages: List[ConversationMessage] = []
    session_start: datetime = Field(default_factory=datetime.now)
    session_id: str
    user_id: str

# Enhanced Assessment Models
class AssessmentResponse(BaseModel):
    """Individual assessment response"""
    question_id: str
    question_text: str
    response_text: str
    emotional_tone: EmotionalTone
    timestamp: datetime = Field(default_factory=datetime.now)
    followup_generated: bool = False

class AgentProgress(BaseModel):
    """Progress tracking for individual agent"""
    agent_type: str
    agent_name: str
    status: AssessmentStatus = AssessmentStatus.NOT_STARTED
    responses: List[AssessmentResponse] = []
    current_question_index: int = 0
    analysis: Optional[Dict[str, Any]] = None
    completion_time: Optional[datetime] = None

class AssessmentProgress(BaseModel):
    """Overall assessment progress tracking"""
    user_id: str
    session_id: str
    current_agent: Optional[str] = None
    agents_progress: Dict[str, AgentProgress] = {}
    overall_status: AssessmentStatus = AssessmentStatus.NOT_STARTED
    completion_percentage: float = 0.0
    start_time: datetime = Field(default_factory=datetime.now)
    completion_time: Optional[datetime] = None

# Career Analysis Models
class RoleRecommendation(BaseModel):
    """Individual role recommendation"""
    title: str
    match_score: float = Field(ge=0, le=100)
    reasons: List[str]
    companies: List[str] = []
    salary_range: Optional[Dict[str, Union[str, int]]] = None
    growth_potential: Optional[str] = None

class SkillDevelopment(BaseModel):
    """Skill development recommendation"""
    skill: str
    priority: str  # Removed validation to avoid Pydantic issues
    timeline: str
    resources: List[str] = []
    current_level: Optional[str] = None
    target_level: Optional[str] = None

class CareerRoadmap(BaseModel):
    """Career development roadmap"""
    six_months: List[str] = []
    one_year: List[str] = []
    three_years: List[str] = []

class IndustryInsights(BaseModel):
    """Industry and market insights"""
    best_industries: List[str] = []
    company_types: List[str] = []
    growth_sectors: List[str] = []
    market_trends: List[str] = []

class ComprehensiveAnalysis(BaseModel):
    """Complete career analysis results"""
    user_id: str
    analysis_date: datetime = Field(default_factory=datetime.now)
    role_recommendations: List[RoleRecommendation] = []
    skill_development_plan: List[SkillDevelopment] = []
    career_roadmap: CareerRoadmap = CareerRoadmap()
    industry_insights: IndustryInsights = IndustryInsights()
    personality_summary: Optional[str] = None
    key_strengths: List[str] = []
    development_areas: List[str] = []
    career_fit_score: Optional[float] = None
    summary: str = ""

# Enhanced User Profile Models
class UserDemographics(BaseModel):
    """User demographic information"""
    age_range: Optional[str] = None
    location: Optional[str] = None
    education_level: Optional[str] = None
    experience_years: Optional[int] = None
    current_role: Optional[str] = None
    industry: Optional[str] = None

class UserProfile(BaseModel):
    """Enhanced user profile with comprehensive data"""
    user_id: str
    name: str
    email: Optional[str] = None
    demographics: UserDemographics = UserDemographics()
    
    # 12D Assessment Results
    interests_analysis: Optional[Dict[str, Any]] = None
    skills_analysis: Optional[Dict[str, Any]] = None
    personality_analysis: Optional[Dict[str, Any]] = None
    aspirations_analysis: Optional[Dict[str, Any]] = None
    motivations_values_analysis: Optional[Dict[str, Any]] = None
    cognitive_abilities_analysis: Optional[Dict[str, Any]] = None
    strengths_weaknesses_analysis: Optional[Dict[str, Any]] = None
    learning_preferences_analysis: Optional[Dict[str, Any]] = None
    track_record_analysis: Optional[Dict[str, Any]] = None
    emotional_intelligence_analysis: Optional[Dict[str, Any]] = None
    constraints_analysis: Optional[Dict[str, Any]] = None
    physical_context_analysis: Optional[Dict[str, Any]] = None
    
    # Career Analysis
    career_analysis: Optional[ComprehensiveAnalysis] = None
    
    # Metadata
    created_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    assessment_completion_date: Optional[datetime] = None

# Response Models for API/UI
class AssessmentQuestionResponse(BaseModel):
    """Response containing an assessment question"""
    type: ResponseType = ResponseType.ASSESSMENT_QUESTION
    message: str
    current_agent: str
    question_index: int
    progress: str
    suggestions: List[str] = []

class GeneralResponse(BaseModel):
    """Response for general conversation"""
    type: ResponseType = ResponseType.GENERAL_RESPONSE
    message: str
    intent: Optional[str] = None
    suggestions: List[str] = []

class AssessmentCompleteResponse(BaseModel):
    """Response when assessment is completed"""
    type: ResponseType = ResponseType.ASSESSMENT_COMPLETE
    message: str
    analysis: ComprehensiveAnalysis
    completion_time: datetime

class ErrorResponse(BaseModel):
    """Error response"""
    type: ResponseType = ResponseType.ERROR_RESPONSE
    message: str
    error_code: Optional[str] = None
    suggestions: List[str] = []

# System State Model
class SystemState(BaseModel):
    """Overall system state"""
    active_users: Dict[str, UserProfile] = {}
    active_sessions: Dict[str, ConversationHistory] = {}
    assessment_progress: Dict[str, AssessmentProgress] = {}
    system_start_time: datetime = Field(default_factory=datetime.now)
    total_assessments_completed: int = 0
    system_status: str = "operational"

# Workflow State for LangGraph (if needed)
class WorkflowState(BaseModel):
    """State for workflow processing"""
    user_id: str
    session_id: str
    current_message: str
    conversation_history: List[Dict[str, Any]] = []
    current_agent: Optional[str] = None
    assessment_data: Dict[str, Any] = {}
    user_profile: Optional[UserProfile] = None
    response: Optional[Dict[str, Any]] = None
    next_action: Optional[str] = None

# Configuration Models
class AgentConfig(BaseModel):
    """Configuration for individual agents"""
    agent_type: str
    agent_name: str
    max_questions: int = 3
    enable_followups: bool = True
    emotional_response: bool = True

class SystemConfig(BaseModel):
    """System-wide configuration"""
    max_session_duration: int = 3600  # seconds
    max_conversation_history: int = 100  # messages
    enable_analytics: bool = True
    auto_save_interval: int = 30  # seconds
    agents: Dict[str, AgentConfig] = {}

# Utility functions for state management
def create_user_profile(user_id: str, name: str, **kwargs) -> UserProfile:
    """Create a new user profile"""
    return UserProfile(
        user_id=user_id,
        name=name,
        **kwargs
    )

def update_assessment_progress(progress: AssessmentProgress, agent_type: str, 
                             response: AssessmentResponse) -> AssessmentProgress:
    """Update assessment progress with new response"""
    if agent_type not in progress.agents_progress:
        progress.agents_progress[agent_type] = AgentProgress(
            agent_type=agent_type,
            agent_name=f"{agent_type.title()} Agent"
        )
    
    agent_progress = progress.agents_progress[agent_type]
    agent_progress.responses.append(response)
    
    # Update completion percentage
    total_agents = 12
    completed_agents = sum(1 for ap in progress.agents_progress.values() 
                          if ap.status == AssessmentStatus.COMPLETED)
    progress.completion_percentage = (completed_agents / total_agents) * 100
    
    return progress