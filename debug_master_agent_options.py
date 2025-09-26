#!/usr/bin/env python3
"""
Debug Script to Check Master Agent Options Logic
This will test exactly what options are being returned when 8+ assessments are completed.
"""

import json
import os
from pathlib import Path

def test_master_agent_logic():
    """Test the Master Agent logic for options display"""
    print("🔍 Testing Master Agent Options Logic...")
    print("=" * 60)
    
    # Simulate the progress calculation logic
    all_dimensions = [
        'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
        'cognitive_abilities', 'learning_preferences', 'physical_context',
        'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
    ]
    
    # Test scenarios
    scenarios = [
        {"name": "0 completed", "completed": []},
        {"name": "3 completed", "completed": ['personality', 'interests', 'aspirations']},
        {"name": "8 completed", "completed": ['personality', 'interests', 'aspirations', 'skills', 'motivations_values', 'cognitive_abilities', 'learning_preferences', 'physical_context']},
        {"name": "10 completed", "completed": ['personality', 'interests', 'aspirations', 'skills', 'motivations_values', 'cognitive_abilities', 'learning_preferences', 'physical_context', 'strengths_weaknesses', 'emotional_intelligence']},
        {"name": "12 completed", "completed": all_dimensions}
    ]
    
    # Options map (same as in the code)
    options_map = {
        "personality": {"title": "🧠 Personality Assessment", "description": "Discover your natural work style and preferences"},
        "interests": {"title": "💡 Career Interests", "description": "Explore what truly engages and motivates you"},
        "aspirations": {"title": "🎯 Career Aspirations", "description": "Define your career goals and future vision"},
        "skills": {"title": "🛠️ Skills Assessment", "description": "Evaluate your current abilities and strengths"},
        "motivations_values": {"title": "⭐ Values & Motivations", "description": "Identify your core values and what drives you"},
        "cognitive_abilities": {"title": "🧩 Cognitive Abilities", "description": "Understand your thinking and problem-solving style"},
        "learning_preferences": {"title": "📚 Learning Preferences", "description": "Discover how you learn and process information best"},
        "physical_context": {"title": "🌍 Work Environment", "description": "Identify your ideal work setting and conditions"},
        "strengths_weaknesses": {"title": "💪 Strengths & Growth Areas", "description": "Honest assessment of abilities and development areas"},
        "emotional_intelligence": {"title": "❤️ Emotional Intelligence", "description": "Assess your interpersonal and emotional skills"},
        "track_record": {"title": "🏆 Track Record", "description": "Review your achievements and success patterns"},
        "constraints": {"title": "⚖️ Practical Considerations", "description": "Identify factors that influence your career choices"}
    }
    
    for scenario in scenarios:
        print(f"\n🧪 Testing Scenario: {scenario['name']}")
        print("-" * 40)
        
        completed = scenario['completed']
        remaining = [dim for dim in all_dimensions if dim not in completed]
        
        print(f"✅ Completed ({len(completed)}): {completed}")
        print(f"⏳ Remaining ({len(remaining)}): {remaining}")
        
        # Simulate the get_next_options logic
        options = []
        
        # Add remaining assessments
        for dim in remaining:
            if dim in options_map:
                option_info = options_map[dim]
                options.append({
                    "agent": dim,
                    "title": option_info["title"],
                    "description": option_info["description"]
                })
        
        # Add insights option if some assessments completed
        if len(completed) >= 3:
            options.append({
                "agent": "insights",
                "title": "📊 Get Career Insights",
                "description": "Review your progress and get preliminary insights"
            })
        
        # Add action plan option if 8+ assessments completed
        if len(completed) >= 8:
            options.append({
                "agent": "action_plan",
                "title": "🎯 Generate Career Action Plan",
                "description": "Create your personalized career development roadmap"
            })
        
        print(f"🎯 Options returned ({len(options)}):")
        for i, option in enumerate(options, 1):
            print(f"   {i}. {option['title']} (agent: {option['agent']})")
        
        # Check for the bug
        if len(completed) >= 8 and len(remaining) > 0:
            assessment_options = [opt for opt in options if opt['agent'] in remaining]
            action_plan_option = [opt for opt in options if opt['agent'] == 'action_plan']
            
            print(f"   📊 Assessment options: {len(assessment_options)}")
            print(f"   🎯 Action plan option: {len(action_plan_option)}")
            
            if len(assessment_options) == 0:
                print("   ❌ BUG DETECTED: No remaining assessment options shown!")
            else:
                print("   ✅ Remaining assessments properly included")

def check_real_user_data():
    """Check real user data to see what's happening"""
    print("\n" + "=" * 60)
    print("🔍 Checking Real User Data...")
    print("=" * 60)
    
    users_dir = Path("data/users")
    if not users_dir.exists():
        print("❌ Users directory not found!")
        return
    
    # Find users with 8+ completed assessments
    users_with_8_plus = []
    
    for user_folder in users_dir.iterdir():
        if user_folder.is_dir():
            profile_path = user_folder / "profile.json"
            if profile_path.exists():
                try:
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                    
                    assessments = profile.get('assessments', {})
                    completed = [k for k, v in assessments.items() if v.get('completed', False)]
                    
                    if len(completed) >= 8:
                        users_with_8_plus.append({
                            'name': profile.get('name', 'Unknown'),
                            'folder': user_folder.name,
                            'completed': completed,
                            'completed_count': len(completed)
                        })
                        
                except Exception as e:
                    continue
    
    print(f"📊 Found {len(users_with_8_plus)} users with 8+ completed assessments:")
    
    if users_with_8_plus:
        for user in users_with_8_plus:
            print(f"\n👤 User: {user['name']} ({user['folder']})")
            print(f"   ✅ Completed: {user['completed_count']}/12")
            print(f"   📝 Assessments: {user['completed']}")
            
            # Calculate what should be remaining
            all_dimensions = [
                'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
                'cognitive_abilities', 'learning_preferences', 'physical_context',
                'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
            ]
            remaining = [dim for dim in all_dimensions if dim not in user['completed']]
            print(f"   ⏳ Should show remaining: {remaining}")
            print(f"   🎯 Should show action plan: YES")
    else:
        print("📭 No users found with 8+ completed assessments")

def main():
    """Run comprehensive debugging"""
    print("🚀 Master Agent Options Debug Script")
    print("=" * 60)
    
    test_master_agent_logic()
    check_real_user_data()
    
    print("\n" + "=" * 60)
    print("🔍 DEBUGGING SUMMARY:")
    print("=" * 60)
    print("The Master Agent logic SHOULD work correctly.")
    print("If 4 agents aren't showing after 8 completed, the issue is likely:")
    print("1. 🔄 Caching problems in Streamlit")
    print("2. 📱 UI rendering issues") 
    print("3. 🔧 State management problems")
    print("4. 🚫 Early returns in the display flow")
    print("\n💡 Try clearing Streamlit cache and restarting the app!")

if __name__ == "__main__":
    main()
