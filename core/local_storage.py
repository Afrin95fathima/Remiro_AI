"""
Local Data Storage System for Remiro AI
Handles user data, responses, and assessment results
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import uuid

class LocalDataManager:
    """Manages local data storage for user assessments and responses"""
    
    def __init__(self, base_path: str = "data/users"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def create_user_id(self, user_name: str) -> str:
        """Create a unique user ID based on name and timestamp"""
        # Create a hash of the name and current timestamp
        name_clean = user_name.lower().replace(' ', '_').replace('-', '_')
        timestamp = str(int(datetime.now().timestamp()))
        unique_hash = hashlib.md5(f"{name_clean}_{timestamp}".encode()).hexdigest()[:8]
        return f"{name_clean}_{unique_hash}"
    
    def create_user_folder(self, user_id: str) -> Path:
        """Create user folder for storing data"""
        user_folder = self.base_path / user_id
        user_folder.mkdir(exist_ok=True)
        return user_folder
    
    def save_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Save user profile information"""
        try:
            user_folder = self.create_user_folder(user_id)
            profile_file = user_folder / "profile.json"
            
            profile_data['created_at'] = datetime.now().isoformat()
            profile_data['last_updated'] = datetime.now().isoformat()
            profile_data['user_id'] = user_id
            
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving user profile: {e}")
            return False
    
    def load_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load user profile information"""
        try:
            user_folder = self.base_path / user_id
            profile_file = user_folder / "profile.json"
            
            if profile_file.exists():
                with open(profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading user profile: {e}")
            return None
    
    def save_assessment_config(self, user_id: str, config: Dict[str, Any]) -> bool:
        """Save assessment configuration (time preference, etc.)"""
        try:
            user_folder = self.create_user_folder(user_id)
            config_file = user_folder / "assessment_config.json"
            
            config['saved_at'] = datetime.now().isoformat()
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving assessment config: {e}")
            return False
    
    def save_question_response(self, user_id: str, agent_type: str, question_index: int, 
                              question_data: Dict[str, Any], response: List[str]) -> bool:
        """Save individual question response"""
        try:
            user_folder = self.create_user_folder(user_id)
            responses_folder = user_folder / "responses"
            responses_folder.mkdir(exist_ok=True)
            
            # Create filename based on agent and question
            response_file = responses_folder / f"{agent_type}_q{question_index}.json"
            
            response_data = {
                'user_id': user_id,
                'agent_type': agent_type,
                'question_index': question_index,
                'question': question_data['question'],
                'options_selected': response,
                'timestamp': datetime.now().isoformat(),
                'question_data': question_data
            }
            
            with open(response_file, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving question response: {e}")
            return False
    
    def save_agent_feedback(self, user_id: str, agent_type: str, question_index: int, 
                           agent_response: Dict[str, Any]) -> bool:
        """Save AI agent's feedback response"""
        try:
            user_folder = self.create_user_folder(user_id)
            feedback_folder = user_folder / "agent_feedback"
            feedback_folder.mkdir(exist_ok=True)
            
            # Create filename based on agent and question
            feedback_file = feedback_folder / f"{agent_type}_q{question_index}_feedback.json"
            
            feedback_data = {
                'user_id': user_id,
                'agent_type': agent_type,
                'question_index': question_index,
                'agent_response': agent_response,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(feedback_file, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving agent feedback: {e}")
            return False
    
    def load_agent_responses(self, user_id: str, agent_type: str) -> List[Dict[str, Any]]:
        """Load all responses for a specific agent"""
        try:
            user_folder = self.base_path / user_id
            responses_folder = user_folder / "responses"
            
            if not responses_folder.exists():
                return []
            
            responses = []
            for response_file in responses_folder.glob(f"{agent_type}_q*.json"):
                with open(response_file, 'r', encoding='utf-8') as f:
                    responses.append(json.load(f))
            
            # Sort by question index
            responses.sort(key=lambda x: x.get('question_index', 0))
            return responses
            
        except Exception as e:
            print(f"Error loading agent responses: {e}")
            return []
    
    def save_assessment_summary(self, user_id: str, summary_data: Dict[str, Any]) -> bool:
        """Save complete assessment summary and analysis"""
        try:
            user_folder = self.create_user_folder(user_id)
            summary_file = user_folder / "assessment_summary.json"
            
            summary_data['user_id'] = user_id
            summary_data['completed_at'] = datetime.now().isoformat()
            summary_data['summary_version'] = "1.0"
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving assessment summary: {e}")
            return False
    
    def load_assessment_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load assessment summary"""
        try:
            user_folder = self.base_path / user_id
            summary_file = user_folder / "assessment_summary.json"
            
            if summary_file.exists():
                with open(summary_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading assessment summary: {e}")
            return None
    
    def get_user_assessment_status(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive status of user's assessment progress"""
        try:
            user_folder = self.base_path / user_id
            
            if not user_folder.exists():
                return {"exists": False}
            
            # Check profile
            profile = self.load_user_profile(user_id)
            
            # Check responses
            responses_folder = user_folder / "responses"
            response_count = len(list(responses_folder.glob("*.json"))) if responses_folder.exists() else 0
            
            # Check summary
            summary = self.load_assessment_summary(user_id)
            
            # Check config
            config_file = user_folder / "assessment_config.json"
            has_config = config_file.exists()
            
            return {
                "exists": True,
                "has_profile": profile is not None,
                "response_count": response_count,
                "has_summary": summary is not None,
                "has_config": has_config,
                "profile": profile,
                "summary": summary
            }
            
        except Exception as e:
            print(f"Error getting user status: {e}")
            return {"exists": False, "error": str(e)}
    
    def list_all_users(self) -> List[Dict[str, Any]]:
        """List all users with basic info"""
        users = []
        try:
            for user_folder in self.base_path.iterdir():
                if user_folder.is_dir():
                    profile = self.load_user_profile(user_folder.name)
                    status = self.get_user_assessment_status(user_folder.name)
                    
                    users.append({
                        "user_id": user_folder.name,
                        "name": profile.get('name', 'Unknown') if profile else 'Unknown',
                        "created_at": profile.get('created_at', 'Unknown') if profile else 'Unknown',
                        "response_count": status.get('response_count', 0),
                        "completed": status.get('has_summary', False)
                    })
            
            return sorted(users, key=lambda x: x.get('created_at', ''), reverse=True)
            
        except Exception as e:
            print(f"Error listing users: {e}")
            return []
    
    def export_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Export all user data as a single JSON object"""
        try:
            user_folder = self.base_path / user_id
            
            if not user_folder.exists():
                return None
            
            # Collect all data
            export_data = {
                "user_id": user_id,
                "export_timestamp": datetime.now().isoformat(),
                "profile": self.load_user_profile(user_id),
                "summary": self.load_assessment_summary(user_id),
                "responses": {}
            }
            
            # Load config if exists
            config_file = user_folder / "assessment_config.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    export_data["assessment_config"] = json.load(f)
            
            # Load all responses
            responses_folder = user_folder / "responses"
            if responses_folder.exists():
                for response_file in responses_folder.glob("*.json"):
                    with open(response_file, 'r', encoding='utf-8') as f:
                        response_data = json.load(f)
                        agent_type = response_data.get('agent_type', 'unknown')
                        question_index = response_data.get('question_index', 0)
                        
                        if agent_type not in export_data["responses"]:
                            export_data["responses"][agent_type] = {}
                        
                        export_data["responses"][agent_type][f"question_{question_index}"] = response_data
            
            return export_data
            
        except Exception as e:
            print(f"Error exporting user data: {e}")
            return None

# Global instance
local_data_manager = LocalDataManager()