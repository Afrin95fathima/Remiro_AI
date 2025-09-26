"""
Test script to verify career insights and action plan generation fixes
"""

import asyncio
import json
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import required classes
import sys
sys.path.append(str(Path(__file__).parent))

from app import get_llm, MasterCareerAgent
from core.user_manager import UserManager

async def test_insights_and_action_plan():
    """Test both insights and action plan generation"""
    
    # Initialize components
    llm = get_llm()
    master_agent = MasterCareerAgent(llm)
    user_manager = UserManager()
    
    # Find a user with completed assessments
    test_user = "test_validation_12345"
    profile_path = Path(f"data/users/{test_user}/profile.json")
    
    if not profile_path.exists():
        print(f"❌ Test user profile not found: {profile_path}")
        return
    
    # Load user profile
    with open(profile_path, 'r', encoding='utf-8') as f:
        user_profile = json.load(f)
    
    print(f"📊 Testing with user: {user_profile.get('name', 'Unknown')}")
    
    # Check assessment structure
    assessments = user_profile.get('assessments', {})
    completed_assessments = [dim for dim, data in assessments.items() if data.get('completed', False)]
    
    print(f"📋 Completed assessments: {len(completed_assessments)}")
    print(f"   Dimensions: {completed_assessments}")
    
    # Check data structure for first assessment
    if completed_assessments:
        first_dim = completed_assessments[0]
        first_assessment = assessments[first_dim]
        print(f"\n🔍 Sample assessment structure ({first_dim}):")
        print(f"   Has 'data': {'data' in first_assessment}")
        print(f"   Has 'assessment_data': {'assessment_data' in first_assessment}")
        if 'assessment_data' in first_assessment:
            assessment_data = first_assessment['assessment_data']
            print(f"   Assessment data keys: {list(assessment_data.keys())}")
    
    print("\n" + "="*60)
    print("🧠 Testing Career Insights Generation")
    print("="*60)
    
    try:
        insights = await master_agent.generate_insights(user_profile)
        
        if insights.get('success'):
            print("✅ SUCCESS: Career insights generated successfully!")
            print(f"📝 Message length: {len(insights.get('message', ''))}")
            
            if insights.get('key_patterns'):
                print(f"🔍 Key patterns found: {len(insights['key_patterns'])}")
                for i, pattern in enumerate(insights['key_patterns'][:2], 1):  # Show first 2
                    print(f"   {i}. {pattern}")
            
            if insights.get('career_directions'):
                print(f"🎯 Career directions: {len(insights['career_directions'])}")
                for i, direction in enumerate(insights['career_directions'][:2], 1):
                    print(f"   {i}. {direction}")
                    
        else:
            print("❌ FAILED: Career insights generation failed")
            print(f"   Error: {insights.get('message', 'Unknown error')}")
            if insights.get('debug_info'):
                print(f"   Debug: {insights['debug_info']}")
                
    except Exception as e:
        print(f"❌ EXCEPTION during insights generation: {e}")
    
    print("\n" + "="*60)
    print("🎯 Testing Career Action Plan Generation")
    print("="*60)
    
    try:
        action_plan = await master_agent.generate_action_plan(user_profile)
        
        if action_plan.get('success'):
            print("✅ SUCCESS: Career action plan generated successfully!")
            print(f"📝 Message length: {len(action_plan.get('message', ''))}")
            
            if action_plan.get('key_strengths'):
                print(f"💪 Key strengths: {len(action_plan['key_strengths'])}")
                for i, strength in enumerate(action_plan['key_strengths'][:2], 1):
                    print(f"   {i}. {strength}")
            
            if action_plan.get('immediate_actions'):
                print(f"⚡ Immediate actions: {len(action_plan['immediate_actions'])}")
                for i, action in enumerate(action_plan['immediate_actions'][:2], 1):
                    print(f"   {i}. {action}")
                    
        else:
            print("❌ FAILED: Career action plan generation failed")
            print(f"   Error: {action_plan.get('message', 'Unknown error')}")
            if action_plan.get('debug_info'):
                print(f"   Debug: {action_plan['debug_info']}")
                
    except Exception as e:
        print(f"❌ EXCEPTION during action plan generation: {e}")

if __name__ == "__main__":
    asyncio.run(test_insights_and_action_plan())
