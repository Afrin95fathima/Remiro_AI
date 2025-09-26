import sys
import os
import json
sys.path.append(r'c:\Users\afrin\OneDrive\Desktop\Remiro AI')

# Debug script to check user profiles and fix assessment data
def debug_user_profiles():
    """Debug user profiles to see why only 4 agents show"""
    
    from core.user_manager import UserManager
    
    user_manager = UserManager()
    
    # List all user folders
    users_dir = r"c:\Users\afrin\OneDrive\Desktop\Remiro AI\data\users"
    
    print("=== CHECKING USER PROFILES ===")
    
    for folder in os.listdir(users_dir):
        if folder.startswith("afrin") and "_" in folder:
            folder_path = os.path.join(users_dir, folder)
            profile_path = os.path.join(folder_path, "profile.json")
            
            if os.path.exists(profile_path):
                print(f"\n📁 {folder}")
                
                try:
                    with open(profile_path, 'r') as f:
                        profile = json.load(f)
                    
                    # Check assessments structure
                    assessments = profile.get('assessments', {})
                    
                    if not assessments:
                        print("   ❌ No assessments structure found")
                        continue
                    
                    # Check how many assessments have proper structure
                    all_dimensions = [
                        'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
                        'cognitive_abilities', 'learning_preferences', 'physical_context',
                        'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
                    ]
                    
                    print(f"   📊 Assessments found: {len(assessments.keys())}")
                    
                    completed_new_format = []
                    completed_old_format = []
                    
                    for dim in all_dimensions:
                        if dim in assessments:
                            # Check if it has new format (completed: true)
                            if assessments[dim].get('completed', False):
                                completed_new_format.append(dim)
                            # Check if it has old format (status: completed)
                            elif assessments[dim].get('status') == 'completed':
                                completed_old_format.append(dim)
                    
                    print(f"   ✅ New format completed: {len(completed_new_format)} - {completed_new_format}")
                    print(f"   🔄 Old format completed: {len(completed_old_format)} - {completed_old_format}")
                    
                    remaining_new = [dim for dim in all_dimensions if dim not in completed_new_format]
                    print(f"   ⏳ Would show remaining: {len(remaining_new)} - {remaining_new}")
                    
                    # If this is the most recent profile, show more details
                    if "fe8fe9b2" in folder:
                        print("\n   🔍 DETAILED ANALYSIS (Most Recent Profile):")
                        print(f"   Profile structure keys: {profile.keys()}")
                        print(f"   Assessments structure: {assessments}")
                        
                        # Show what get_next_options would return
                        if len(completed_new_format) >= 8:
                            print("   📋 Would show: Generate Career Action Plan")
                        else:
                            print(f"   📋 Would show {len(remaining_new)} remaining assessments")
                            if len(completed_new_format) >= 3:
                                print("   💡 Plus: Get Career Insights option")
                    
                except Exception as e:
                    print(f"   ❌ Error reading profile: {e}")

def fix_user_profiles():
    """Fix user profiles by ensuring all 12 assessments are initialized"""
    
    users_dir = r"c:\Users\afrin\OneDrive\Desktop\Remiro AI\data\users"
    
    # Target the most recent afrin profile
    target_profile = "afrin_fe8fe9b2"
    profile_path = os.path.join(users_dir, target_profile, "profile.json")
    
    if not os.path.exists(profile_path):
        print(f"❌ Profile not found: {profile_path}")
        return
    
    print(f"🔧 Fixing profile: {target_profile}")
    
    # Read current profile
    with open(profile_path, 'r') as f:
        profile = json.load(f)
    
    # Ensure assessments structure exists
    if 'assessments' not in profile:
        profile['assessments'] = {}
    
    # Initialize all 12 assessments if they don't exist
    all_dimensions = [
        'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
        'cognitive_abilities', 'learning_preferences', 'physical_context',
        'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
    ]
    
    for dim in all_dimensions:
        if dim not in profile['assessments']:
            profile['assessments'][dim] = {
                "completed": False,
                "data": None,
                "completed_at": None
            }
            print(f"   ✅ Initialized {dim}")
        else:
            print(f"   ✓ {dim} already exists")
    
    # Save the fixed profile
    with open(profile_path, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print(f"💾 Profile fixed and saved!")
    
    # Verify the fix
    print("\n🔍 Verifying fix...")
    debug_user_profiles()

if __name__ == "__main__":
    print("1. Debugging user profiles...")
    debug_user_profiles()
    
    print("\n" + "="*50)
    print("2. Fixing user profiles...")
    fix_user_profiles()
