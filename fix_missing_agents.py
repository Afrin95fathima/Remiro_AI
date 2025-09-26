"""
Debug script to fix the missing agents issue in dashboard
"""

import json
import os
from pathlib import Path

def fix_missing_agents():
    """Fix missing agents in user profiles and ensure all 12 dimensions are available"""
    
    # Find the latest user directory
    data_dir = Path('data/users')
    if not data_dir.exists():
        print("No users data directory found")
        return
    
    user_dirs = [d for d in data_dir.iterdir() if d.is_dir() and d.name.startswith('afrin_')]
    if not user_dirs:
        print("No user directories found")
        return
    
    latest_user_dir = sorted(user_dirs, key=lambda x: x.stat().st_mtime)[-1]
    profile_path = latest_user_dir / 'profile.json'
    
    print(f"Working with user directory: {latest_user_dir.name}")
    
    if not profile_path.exists():
        print("Profile file not found")
        return
    
    # Load current profile
    with open(profile_path, 'r') as f:
        profile = json.load(f)
    
    print(f"Current profile loaded")
    
    # All 12 dimensions that should be available
    all_dimensions = [
        'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
        'cognitive_abilities', 'learning_preferences', 'physical_context',
        'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
    ]
    
    # Current assessments
    assessments = profile.get('assessments', {})
    
    print("Current assessment status:")
    completed_count = 0
    for dim in all_dimensions:
        if dim in assessments and assessments[dim].get('completed', False):
            print(f"  ✅ {dim}: COMPLETED")
            completed_count += 1
        else:
            print(f"  ❌ {dim}: MISSING")
    
    print(f"\\nTotal completed: {completed_count}/12")
    
    # Check if we need to add missing dimensions as available but not started
    missing_dimensions = [dim for dim in all_dimensions if dim not in assessments]
    
    if missing_dimensions:
        print(f"\\nAdding missing dimensions as available but not started:")
        for dim in missing_dimensions:
            assessments[dim] = {
                'completed': False,
                'data': {},
                'started_at': None
            }
            print(f"  + Added {dim}")
        
        # Update profile
        profile['assessments'] = assessments
        
        # Save updated profile
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2)
        
        print(f"\\n✅ Profile updated successfully!")
    else:
        print(f"\\n✅ All dimensions already present in profile")
    
    print(f"\\n📊 Final status: {completed_count} completed, {12-completed_count} remaining")

if __name__ == "__main__":
    fix_missing_agents()
