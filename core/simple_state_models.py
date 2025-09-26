"""
Simple State Models - Compatibility Version

Basic state models without complex validations for maximum compatibility.
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime

# Simple data classes instead of Pydantic models
class SimpleUserProfile:
    """Simple user profile"""
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.created_date = datetime.now()

class SimpleConversationHistory:
    """Simple conversation history"""
    def __init__(self, session_id: str, user_id: str):
        self.session_id = session_id
        self.user_id = user_id
        self.messages = []

class SimpleAssessmentProgress:
    """Simple assessment progress"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.agents_progress = {}
        self.completion_percentage = 0.0

class SimpleSystemState:
    """Simple system state"""
    def __init__(self):
        self.active_users = {}
        self.active_sessions = {}
        self.system_start_time = datetime.now()

# For backward compatibility, create aliases
UserProfile = SimpleUserProfile
ConversationHistory = SimpleConversationHistory
AssessmentProgress = SimpleAssessmentProgress
SystemState = SimpleSystemState
ConversationMessage = dict  # Simple dict instead of complex model