"""
Debug script to check what the dashboard is actually receiving
"""

import json
import os
from pathlib import Path
import sys
sys.path.append('.')

# Import the app components
from core.user_manager import UserManager

def debug_dashboard_data():
    """Debug what data the dashboard is receiving"""
    print("🔍 Debugging dashboard data...")
    
    # Initialize user manager
    user_manager = UserManager()
    
    # Find the latest user
    data_dir = Path('data/users')
    user_dirs = [d for d in data_dir.iterdir() if d.is_dir() and d.name.startswith('afrin_')]
    if user_dirs:
        latest_user_dir = sorted(user_dirs, key=lambda x: x.stat().st_mtime)[-1]
        profile_path = latest_user_dir / 'profile.json'
        
        print(f"Latest user: {latest_user_dir.name}")
        
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                user_profile = json.load(f)
            
            print(f"Profile loaded: {user_profile.get('name', 'Unknown')}")
            
            # Simulate what the master agent progress calculation does
            assessments = user_profile.get('assessments', {})
            all_dimensions = [
                'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
                'cognitive_abilities', 'learning_preferences', 'physical_context',
                'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
            ]
            
            print(f"\\n📋 Raw assessments data:")
            for dim in all_dimensions:
                if dim in assessments:
                    completed = assessments[dim].get('completed', False)
                    print(f"  {dim}: {completed}")
                else:
                    print(f"  {dim}: MISSING")
            
            # Calculate progress like MasterCareerAgent does
            completed = [dim for dim in all_dimensions if assessments.get(dim, {}).get('completed', False)]
            remaining = [dim for dim in all_dimensions if dim not in completed]
            
            progress = {
                "completed": completed,
                "remaining": remaining,
                "progress_percentage": round((len(completed) / len(all_dimensions)) * 100, 1),
                "total_dimensions": len(all_dimensions)
            }
            
            print(f"\\n📊 Dashboard Progress Data:")
            print(f"  Completed ({len(progress['completed'])}): {progress['completed']}")
            print(f"  Remaining ({len(progress['remaining'])}): {progress['remaining']}")
            print(f"  Progress: {progress['progress_percentage']}%")
            
            return progress
        else:
            print("❌ Profile file not found")
    else:
        print("❌ No user directories found")
    
    return None

if __name__ == "__main__":
    debug_dashboard_data()
