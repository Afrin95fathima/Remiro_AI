"""
Simple test to verify career insights and action plan work with real user data
"""

import json
from pathlib import Path

def check_user_profiles():
    """Check user profiles to find one with completed assessments"""
    
    users_dir = Path("data/users")
    completed_users = []
    
    for user_dir in users_dir.iterdir():
        if user_dir.is_dir():
            profile_path = user_dir / "profile.json"
            if profile_path.exists():
                try:
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                    
                    # Check for assessments
                    assessments = profile.get('assessments', {})
                    completed_count = len([dim for dim, data in assessments.items() if data.get('completed', False)])
                    
                    if completed_count > 0:
                        completed_users.append({
                            'name': profile.get('name', 'Unknown'),
                            'user_id': user_dir.name,
                            'completed_assessments': completed_count,
                            'has_assessment_data': any(
                                data.get('assessment_data') or data.get('data') 
                                for data in assessments.values() 
                                if data.get('completed')
                            )
                        })
                        
                except Exception as e:
                    print(f"Error reading {profile_path}: {e}")
    
    print("🔍 Users with completed assessments:")
    print("="*50)
    
    for user in sorted(completed_users, key=lambda x: x['completed_assessments'], reverse=True):
        print(f"👤 {user['name']} ({user['user_id']})")
        print(f"   ✅ {user['completed_assessments']} assessments completed")
        print(f"   📊 Has assessment data: {user['has_assessment_data']}")
        print()
    
    return completed_users

if __name__ == "__main__":
    users = check_user_profiles()
    
    if users:
        best_user = max(users, key=lambda x: x['completed_assessments'])
        print(f"🎯 Best test candidate: {best_user['name']} with {best_user['completed_assessments']} assessments")
        print(f"   Use this user to test career insights and action plan generation")
    else:
        print("❌ No users found with completed assessments")
        print("💡 Run some assessments first to test the career insights/action plan features")
