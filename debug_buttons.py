"""
Debug script to test the insights and action plan functionality
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app and required modules
from app import MasterCareerAgent, UserManager

def test_insights_and_action_plan():
    """Test the insights and action plan generation"""
    print("🔍 Testing Insights and Action Plan Generation")
    print("=" * 50)
    
    # Initialize components
    master_agent = MasterCareerAgent()
    user_manager = UserManager()
    
    # Find a user with completed assessments
    users_dir = "data/users"
    if not os.path.exists(users_dir):
        print("❌ No users directory found!")
        return
    
    user_folders = [f for f in os.listdir(users_dir) if os.path.isdir(os.path.join(users_dir, f))]
    
    if not user_folders:
        print("❌ No user folders found!")
        return
    
    # Test with the first user folder
    test_user_folder = user_folders[0]
    print(f"📂 Testing with user folder: {test_user_folder}")
    
    # Load user profile
    try:
        user_profile = user_manager.load_user_profile(test_user_folder)
        print(f"✅ Loaded profile for: {user_profile.get('name', 'Unknown')}")
        
        # Check assessment progress
        progress = master_agent.get_assessment_progress(user_profile)
        print(f"📊 Assessment Progress: {len(progress['completed'])}/12 completed")
        print(f"   Completed: {progress['completed']}")
        print(f"   Remaining: {progress['remaining']}")
        
        # Test get_available_options
        print("\n🎯 Testing get_available_options:")
        options = master_agent.get_available_options(user_profile)
        print(f"   Available options: {len(options)}")
        for i, option in enumerate(options, 1):
            print(f"   {i}. {option['title']} (agent: {option['agent']})")
        
        # Check if insights option is available
        insights_available = any(option['agent'] == 'insights' for option in options)
        action_plan_available = any(option['agent'] == 'action_plan' for option in options)
        
        print(f"\n📊 Insights available: {insights_available}")
        print(f"🎯 Action Plan available: {action_plan_available}")
        
        # Test insights generation
        if len(progress['completed']) > 0:
            print("\n🔍 Testing Insights Generation:")
            try:
                insights_result = asyncio.run(master_agent.generate_insights(user_profile))
                print(f"   Success: {insights_result.get('success', False)}")
                if insights_result.get('success'):
                    print(f"   Message length: {len(insights_result.get('message', ''))}")
                    print(f"   Key patterns: {len(insights_result.get('key_patterns', []))}")
                    print(f"   Career directions: {len(insights_result.get('career_directions', []))}")
                    print(f"   Personalized insights: {len(insights_result.get('personalized_insights', []))}")
                else:
                    print(f"   Error: {insights_result.get('message', 'Unknown error')}")
            except Exception as e:
                print(f"   ❌ Exception during insights generation: {e}")
        
        # Test action plan generation
        if len(progress['completed']) >= 12:
            print("\n🎯 Testing Action Plan Generation:")
            try:
                action_plan_result = asyncio.run(master_agent.generate_action_plan(user_profile))
                print(f"   Success: {action_plan_result.get('success', False)}")
                if action_plan_result.get('success'):
                    print(f"   Message length: {len(action_plan_result.get('message', ''))}")
                    print(f"   Action plan keys: {list(action_plan_result.keys())}")
                else:
                    print(f"   Error: {action_plan_result.get('message', 'Unknown error')}")
            except Exception as e:
                print(f"   ❌ Exception during action plan generation: {e}")
        else:
            print(f"\n⏳ Need {12 - len(progress['completed'])} more assessments for action plan")
        
    except Exception as e:
        print(f"❌ Error loading user profile: {e}")

def test_specific_user_profiles():
    """Test multiple user profiles to find one with enough data"""
    print("\n🔍 Testing Multiple User Profiles")
    print("=" * 50)
    
    user_manager = UserManager()
    users_dir = "data/users"
    
    if not os.path.exists(users_dir):
        print("❌ No users directory found!")
        return
    
    user_folders = [f for f in os.listdir(users_dir) if os.path.isdir(os.path.join(users_dir, f))]
    
    for user_folder in user_folders[:5]:  # Test first 5 users
        try:
            print(f"\n📂 Testing: {user_folder}")
            user_profile = user_manager.load_user_profile(user_folder)
            
            master_agent = MasterCareerAgent()
            progress = master_agent.get_assessment_progress(user_profile)
            
            print(f"   Name: {user_profile.get('name', 'Unknown')}")
            print(f"   Completed: {len(progress['completed'])}/12")
            
            if len(progress['completed']) >= 8:
                print(f"   ✅ Good candidate for testing (8+ assessments)")
                
                # Test options generation
                options = master_agent.get_available_options(user_profile)
                insights_available = any(option['agent'] == 'insights' for option in options)
                action_plan_available = any(option['agent'] == 'action_plan' for option in options)
                
                print(f"   📊 Insights option: {insights_available}")
                print(f"   🎯 Action plan option: {action_plan_available}")
                
                break
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Debug Tests")
    print(f"⏰ Time: {datetime.now()}")
    print()
    
    test_insights_and_action_plan()
    test_specific_user_profiles()
    
    print("\n✅ Debug tests completed!")
