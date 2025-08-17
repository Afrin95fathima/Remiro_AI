"""
User Manager for Remiro AI

Handles user profile creation, data persistence, and conversation management.
All user data is stored locally in organized folder structures.
"""

import os
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import re

from core.state_models import (
    UserProfile, ConversationMessage, AgentType, AssessmentStatus
)

class UserManager:
    """Manages user profiles and conversation data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.users_dir = self.data_dir / "users"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure data directories exist"""
        self.data_dir.mkdir(exist_ok=True)
        self.users_dir.mkdir(exist_ok=True)
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize user name for folder creation"""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9\s]', '', name.strip())
        sanitized = re.sub(r'\s+', '_', sanitized)
        return sanitized.lower()
    
    def create_user(self, name: str) -> Dict[str, Any]:
        """Create a new user profile"""
        user_id = str(uuid.uuid4())
        sanitized_name = self._sanitize_name(name)
        
        # Create user folder
        user_folder_name = f"{sanitized_name}_{user_id[:8]}"
        user_dir = self.users_dir / user_folder_name
        user_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (user_dir / "sessions").mkdir(exist_ok=True)
        (user_dir / "assessments").mkdir(exist_ok=True)
        
        # Create user profile
        profile = UserProfile(
            user_id=user_id,
            name=name
        )
        
        # Save profile
        profile_path = user_dir / "profile.json"
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile.model_dump(), f, indent=2, default=str)
        
        return {
            "user_id": user_id,
            "name": name,
            "folder_path": str(user_dir),
            "message": f"Welcome {name}! I'm Remiro AI, your career counsellor. I'm here to help you discover your ideal career path through a comprehensive 12-dimensional assessment. Let's begin this journey together."
        }
    
    def get_or_create_user(self, name: str, additional_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get existing user or create new one - simplified version for enhanced app"""
        # For the enhanced app, we'll create a simple profile structure
        # that's compatible with the new application design
        
        sanitized_name = self._sanitize_name(name)
        user_id = str(uuid.uuid4())
        
        # Create user folder
        user_folder_name = f"{sanitized_name}_{user_id[:8]}"
        user_dir = self.users_dir / user_folder_name
        user_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (user_dir / "sessions").mkdir(exist_ok=True)
        (user_dir / "assessments").mkdir(exist_ok=True)
        
        # Create simple profile structure compatible with enhanced app
        profile = {
            "user_id": user_id,
            "name": name,
            "folder_path": str(user_dir),
            "created_at": datetime.now().isoformat(),
            "assessments": {},
            "background": additional_info.get("background", "Professional") if additional_info else "Professional"
        }
        
        # Add any additional info
        if additional_info:
            profile.update(additional_info)
        
        # Save profile
        profile_path = user_dir / "profile.json"
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, default=str)
        
        return profile
    
    def save_user_profile(self, user_profile: Dict[str, Any]) -> bool:
        """Save user profile - simplified version for enhanced app"""
        try:
            if "folder_path" in user_profile:
                profile_path = Path(user_profile["folder_path"]) / "profile.json"
            else:
                # Find user directory by user_id
                user_dir = self._find_user_directory(user_profile["user_id"])
                if not user_dir:
                    return False
                profile_path = user_dir / "profile.json"
            
            user_profile["updated_at"] = datetime.now().isoformat()
            
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(user_profile, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error saving user profile: {e}")
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID"""
        user_dir = self._find_user_directory(user_id)
        if not user_dir:
            return None
        
        profile_path = user_dir / "profile.json"
        if not profile_path.exists():
            return None
        
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            return UserProfile(**profile_data)
        except Exception as e:
            print(f"Error loading user profile: {e}")
            return None
    
    def update_user_profile(self, user_profile: UserProfile) -> bool:
        """Update user profile"""
        user_dir = self._find_user_directory(user_profile.user_id)
        if not user_dir:
            return False
        
        try:
            # Update timestamp
            user_profile.updated_at = datetime.now()
            
            profile_path = user_dir / "profile.json"
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(user_profile.model_dump(), f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False
    
    def save_conversation(self, user_id: str, session_id: str, messages: List[ConversationMessage]) -> bool:
        """Save conversation to session file"""
        user_dir = self._find_user_directory(user_id)
        if not user_dir:
            return False
        
        try:
            sessions_dir = user_dir / "sessions"
            session_file = sessions_dir / f"{session_id}.json"
            
            # Convert messages to dict format
            messages_data = [msg.model_dump() for msg in messages]
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "session_id": session_id,
                    "created_at": datetime.now().isoformat(),
                    "messages": messages_data
                }, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def load_conversation(self, user_id: str, session_id: str) -> Optional[List[ConversationMessage]]:
        """Load conversation from session file"""
        user_dir = self._find_user_directory(user_id)
        if not user_dir:
            return None
        
        try:
            sessions_dir = user_dir / "sessions"
            session_file = sessions_dir / f"{session_id}.json"
            
            if not session_file.exists():
                return []
            
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            messages = []
            for msg_data in session_data.get("messages", []):
                messages.append(ConversationMessage(**msg_data))
            
            return messages
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return None
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a user"""
        user_dir = self._find_user_directory(user_id)
        if not user_dir:
            return []
        
        sessions_dir = user_dir / "sessions"
        if not sessions_dir.exists():
            return []
        
        sessions = []
        for session_file in sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                sessions.append({
                    "session_id": session_data.get("session_id"),
                    "created_at": session_data.get("created_at"),
                    "message_count": len(session_data.get("messages", []))
                })
            except Exception as e:
                print(f"Error reading session file {session_file}: {e}")
        
        return sorted(sessions, key=lambda x: x["created_at"], reverse=True)
    
    def get_user_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Generate comprehensive user summary"""
        profile = self.get_user_profile(user_id)
        if not profile:
            return None
        
        sessions = self.get_user_sessions(user_id)
        user_dir = self._find_user_directory(user_id)
        
        # Calculate assessment progress
        completion_percentage = profile.get_completion_percentage()
        next_assessment = profile.get_next_assessment()
        
        # Get completed assessments
        completed_assessments = []
        assessment_mapping = {
            AgentType.COGNITIVE_ABILITIES: profile.cognitive_abilities,
            AgentType.PERSONALITY: profile.personality,
            AgentType.EMOTIONAL_INTELLIGENCE: profile.emotional_intelligence,
            AgentType.PHYSICAL_CONTEXT: profile.physical_context,
            AgentType.STRENGTHS_WEAKNESSES: profile.strengths_weaknesses,
            AgentType.SKILLS: profile.skills,
            AgentType.CONSTRAINTS: profile.constraints,
            AgentType.INTERESTS: profile.interests,
            AgentType.MOTIVATIONS_VALUES: profile.motivations_values,
            AgentType.ASPIRATIONS: profile.aspirations,
            AgentType.TRACK_RECORD: profile.track_record,
            AgentType.LEARNING_PREFERENCES: profile.learning_preferences,
        }
        
        for agent_type, assessment in assessment_mapping.items():
            if assessment.status == AssessmentStatus.COMPLETED:
                completed_assessments.append({
                    "dimension": agent_type.value.replace('_', ' ').title(),
                    "completed_at": assessment.completed_at,
                    "score": assessment.score,
                    "insights": assessment.insights
                })
        
        return {
            "user_info": {
                "name": profile.name,
                "user_id": profile.user_id,
                "created_at": profile.created_at,
                "folder_path": str(user_dir) if user_dir else None
            },
            "assessment_progress": {
                "completion_percentage": completion_percentage,
                "completed_count": len(completed_assessments),
                "total_count": 12,
                "next_assessment": next_assessment.value if next_assessment else None,
                "completed_assessments": completed_assessments
            },
            "conversation_stats": {
                "total_sessions": len(sessions),
                "total_messages": sum(s["message_count"] for s in sessions),
                "last_activity": sessions[0]["created_at"] if sessions else None
            },
            "recommendations": self._generate_recommendations(profile)
        }
    
    def _generate_recommendations(self, profile: UserProfile) -> List[str]:
        """Generate recommendations based on current profile state"""
        recommendations = []
        
        # Check incomplete assessments
        assessment_names = {
            AgentType.COGNITIVE_ABILITIES: "Cognitive Abilities",
            AgentType.PERSONALITY: "Personality",
            AgentType.EMOTIONAL_INTELLIGENCE: "Emotional Intelligence",
            AgentType.PHYSICAL_CONTEXT: "Work Environment Preferences",
            AgentType.STRENGTHS_WEAKNESSES: "Strengths & Weaknesses",
            AgentType.SKILLS: "Skills Inventory",
            AgentType.CONSTRAINTS: "Life Constraints",
            AgentType.INTERESTS: "Interests & Passions",
            AgentType.MOTIVATIONS_VALUES: "Motivations & Values",
            AgentType.ASPIRATIONS: "Future Aspirations",
            AgentType.TRACK_RECORD: "Background & Experience",
            AgentType.LEARNING_PREFERENCES: "Learning Preferences",
        }
        
        assessment_mapping = {
            AgentType.COGNITIVE_ABILITIES: profile.cognitive_abilities,
            AgentType.PERSONALITY: profile.personality,
            AgentType.EMOTIONAL_INTELLIGENCE: profile.emotional_intelligence,
            AgentType.PHYSICAL_CONTEXT: profile.physical_context,
            AgentType.STRENGTHS_WEAKNESSES: profile.strengths_weaknesses,
            AgentType.SKILLS: profile.skills,
            AgentType.CONSTRAINTS: profile.constraints,
            AgentType.INTERESTS: profile.interests,
            AgentType.MOTIVATIONS_VALUES: profile.motivations_values,
            AgentType.ASPIRATIONS: profile.aspirations,
            AgentType.TRACK_RECORD: profile.track_record,
            AgentType.LEARNING_PREFERENCES: profile.learning_preferences,
        }
        
        incomplete_assessments = []
        for agent_type, assessment in assessment_mapping.items():
            if assessment.status != AssessmentStatus.COMPLETED:
                incomplete_assessments.append(assessment_names[agent_type])
        
        if incomplete_assessments:
            if len(incomplete_assessments) == 12:
                recommendations.append("Begin your career assessment journey by exploring your cognitive abilities")
            elif len(incomplete_assessments) > 6:
                recommendations.append(f"Continue your assessment by completing: {incomplete_assessments[0]}")
            else:
                recommendations.append(f"You're making great progress! Complete these remaining assessments: {', '.join(incomplete_assessments[:3])}")
        else:
            recommendations.append("Excellent! Your profile is complete. Ready for comprehensive career recommendations.")
            recommendations.append("Schedule a follow-up session to explore specific career paths in detail.")
        
        return recommendations
    
    def _find_user_directory(self, user_id: str) -> Optional[Path]:
        """Find user directory by user ID"""
        for user_dir in self.users_dir.iterdir():
            if user_dir.is_dir() and user_id[:8] in user_dir.name:
                return user_dir
        return None
    
    def list_all_users(self) -> List[Dict[str, str]]:
        """List all users in the system"""
        users = []
        for user_dir in self.users_dir.iterdir():
            if user_dir.is_dir():
                profile_path = user_dir / "profile.json"
                if profile_path.exists():
                    try:
                        with open(profile_path, 'r', encoding='utf-8') as f:
                            profile_data = json.load(f)
                        
                        users.append({
                            "user_id": profile_data.get("user_id"),
                            "name": profile_data.get("name"),
                            "folder_name": user_dir.name,
                            "created_at": profile_data.get("created_at")
                        })
                    except Exception as e:
                        print(f"Error reading profile in {user_dir}: {e}")
        
        return sorted(users, key=lambda x: x["created_at"], reverse=True)
