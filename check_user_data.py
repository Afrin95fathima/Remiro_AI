"""
Simple test to check user data and button availability
"""

import json
import os

def check_user_data():
    """Check user data for button availability conditions"""
    users_dir = "data/users"
    
    if not os.path.exists(users_dir):
        print("❌ No users directory found!")
        return
    
    user_folders = [f for f in os.listdir(users_dir) if os.path.isdir(os.path.join(users_dir, f))]
    
    print(f"📂 Found {len(user_folders)} user folders")
    
    for user_folder in user_folders:
        profile_path = os.path.join(users_dir, user_folder, "profile.json")
        
        if os.path.exists(profile_path):
            try:
                with open(profile_path, 'r') as f:
                    profile = json.load(f)
                
                name = profile.get('name', 'Unknown')
                assessments = profile.get('assessments', {})
                
                completed = [k for k, v in assessments.items() if v.get('completed', False)]
                
                print(f"\n👤 {name} ({user_folder})")
                print(f"   📊 Completed assessments: {len(completed)}/12")
                print(f"   📝 Assessments: {completed}")
                
                # Check button conditions
                insights_ready = len(completed) >= 3
                action_plan_ready = len(completed) >= 8
                
                print(f"   💡 Insights button ready: {insights_ready}")
                print(f"   🎯 Action Plan button ready: {action_plan_ready}")
                
                if action_plan_ready:
                    print(f"   ✅ This user should see both buttons!")
                elif insights_ready:
                    print(f"   ⚠️ This user should see insights button only")
                
            except Exception as e:
                print(f"   ❌ Error reading {user_folder}: {e}")
        else:
            print(f"   ⚠️ No profile.json for {user_folder}")

if __name__ == "__main__":
    check_user_data()
