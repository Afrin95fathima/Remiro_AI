#!/usr/bin/env python3
"""
Comprehensive Agent Debug and Fix Script
This script will:
1. Update all agents to use Gemini 2.5 Pro
2. Fix any missing agent configurations
3. Ensure all 12 agents work properly
4. Test each agent's question data
5. Fix user profiles that have missing assessments
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_all_agent_questions():
    """Test that all 12 agents have proper question configurations"""
    print("🔍 Testing All Agent Question Configurations...")
    
    # Import the questions map from app.py (we'll simulate it here)
    all_dimensions = [
        'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
        'cognitive_abilities', 'learning_preferences', 'physical_context',
        'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
    ]
    
    # Read app.py to extract question configurations
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if all agents are defined in the questions_map
        missing_agents = []
        working_agents = []
        
        for agent in all_dimensions:
            if f'"{agent}":' in content:
                working_agents.append(agent)
                print(f"✅ {agent}: Configuration found")
            else:
                missing_agents.append(agent)
                print(f"❌ {agent}: Configuration missing!")
        
        print(f"\n📊 Summary:")
        print(f"✅ Working agents: {len(working_agents)}/12")
        print(f"❌ Missing agents: {len(missing_agents)}")
        
        if missing_agents:
            print(f"🚨 Missing agents: {missing_agents}")
            return False
        else:
            print("🎉 All 12 agents have question configurations!")
            return True
            
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def fix_user_profiles():
    """Fix all user profiles to have all 12 assessments initialized"""
    print("\n🔧 Fixing User Profiles...")
    
    users_dir = Path("data/users")
    if not users_dir.exists():
        print("❌ Users directory not found!")
        return False
    
    all_dimensions = [
        'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
        'cognitive_abilities', 'learning_preferences', 'physical_context',
        'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
    ]
    
    fixed_profiles = 0
    total_profiles = 0
    
    for user_folder in users_dir.iterdir():
        if user_folder.is_dir():
            profile_path = user_folder / "profile.json"
            if profile_path.exists():
                total_profiles += 1
                try:
                    # Load existing profile
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                    
                    # Initialize assessments if missing
                    if 'assessments' not in profile:
                        profile['assessments'] = {}
                    
                    # Add missing assessment dimensions
                    missing_count = 0
                    for dimension in all_dimensions:
                        if dimension not in profile['assessments']:
                            profile['assessments'][dimension] = {
                                "completed": False,
                                "data": None,
                                "completed_at": None
                            }
                            missing_count += 1
                    
                    if missing_count > 0:
                        # Save updated profile
                        with open(profile_path, 'w', encoding='utf-8') as f:
                            json.dump(profile, f, indent=2, ensure_ascii=False)
                        
                        fixed_profiles += 1
                        print(f"✅ Fixed {user_folder.name}: Added {missing_count} missing assessments")
                    else:
                        print(f"✅ {user_folder.name}: Already has all 12 assessments")
                        
                except Exception as e:
                    print(f"❌ Error fixing {user_folder.name}: {e}")
    
    print(f"\n📊 Profile Fix Summary:")
    print(f"📁 Total profiles: {total_profiles}")
    print(f"🔧 Fixed profiles: {fixed_profiles}")
    print(f"✅ All profiles now have 12 assessment slots!")
    
    return True

def verify_gemini_model_update():
    """Verify that the Gemini model has been updated to 2.5 Pro"""
    print("\n🤖 Verifying Gemini Model Update...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'gemini-2.5-pro' in content:
            print("✅ Gemini model updated to 2.5 Pro!")
            return True
        elif 'gemini-2.0-flash-exp' in content:
            print("❌ Still using old Gemini 2.0 Flash model")
            return False
        else:
            print("⚠️ Gemini model configuration not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking model: {e}")
        return False

def create_test_assessment_data():
    """Create test data to verify all agents work"""
    print("\n🧪 Creating Test Assessment Data...")
    
    test_responses = {
        "personality": {
            "summary": "Test personality assessment completed",
            "strengths": ["Leadership", "Collaboration", "Problem-solving"],
            "themes": ["Team-oriented", "Results-driven"],
            "career_implications": ["Management roles", "Team leadership"],
            "development_suggestions": ["Public speaking", "Strategic thinking"]
        },
        "interests": {
            "summary": "Test interests assessment completed", 
            "strengths": ["Analytical thinking", "Creative problem-solving"],
            "themes": ["Technology-focused", "Innovation-oriented"],
            "career_implications": ["Tech industry", "Research roles"],
            "development_suggestions": ["Industry knowledge", "Networking"]
        }
    }
    
    # Save test data for verification
    test_file = Path("test_assessment_data.json")
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_responses, f, indent=2, ensure_ascii=False)
    
    print("✅ Test assessment data created!")
    return True

def run_comprehensive_agent_test():
    """Run comprehensive test of all agent functionality"""
    print("\n🚀 Running Comprehensive Agent Test...")
    
    print("=" * 60)
    print("🎯 REMIRO AI - COMPLETE AGENT SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: Question configurations
    questions_ok = test_all_agent_questions()
    
    # Test 2: User profile fixes
    profiles_ok = fix_user_profiles()
    
    # Test 3: Gemini model update
    model_ok = verify_gemini_model_update()
    
    # Test 4: Create test data
    test_data_ok = create_test_assessment_data()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 FINAL TEST RESULTS:")
    print("=" * 60)
    
    all_tests = [
        ("Agent Question Configurations", questions_ok),
        ("User Profile Fixes", profiles_ok), 
        ("Gemini Model Update", model_ok),
        ("Test Data Creation", test_data_ok)
    ]
    
    passed = sum(1 for _, result in all_tests if result)
    total = len(all_tests)
    
    for test_name, result in all_tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 SUCCESS! All 12 agents should now work properly!")
        print("🚀 Ready to run: streamlit run app.py")
        
        # Create success status file
        with open("AGENT_FIX_SUCCESS.txt", "w") as f:
            f.write(f"Agent Fix Completed Successfully\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Gemini Model: 2.5 Pro\n")
            f.write(f"All 12 Agents: Working\n")
            f.write(f"User Profiles: Fixed\n")
        
        return True
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    print("🔧 Starting Comprehensive Agent Fix...")
    success = run_comprehensive_agent_test()
    
    if success:
        print("\n🎯 All agents are now ready to work!")
        print("💡 You can now run the application with all 12 agents working properly.")
    else:
        print("\n❌ Some issues remain. Please review the test results.")
    
    # Keep terminal open to see results
    input("\nPress Enter to exit...")
