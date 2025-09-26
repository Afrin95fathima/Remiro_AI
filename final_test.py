"""
Final comprehensive test to ensure career insights and action plan generation work
"""

import asyncio
import json
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_complete_user():
    """Test with a user who has 12/12 assessments completed"""
    
    # Import here to avoid streamlit warnings
    import sys
    sys.path.append(str(Path(__file__).parent))
    
    from app import get_llm, MasterCareerAgent
    
    # Initialize components
    llm = get_llm()
    master_agent = MasterCareerAgent(llm)
    
    # Use a user with complete assessments
    test_user_id = "raja_80d22318"  # Raja with 12/12 assessments
    profile_path = Path(f"data/users/{test_user_id}/profile.json")
    
    if not profile_path.exists():
        print(f"❌ Profile not found: {profile_path}")
        return
    
    # Load user profile
    with open(profile_path, 'r', encoding='utf-8') as f:
        user_profile = json.load(f)
    
    user_name = user_profile.get('name', 'Unknown')
    assessments = user_profile.get('assessments', {})
    completed = [dim for dim, data in assessments.items() if data.get('completed', False)]
    
    print(f"🎯 Testing with: {user_name}")
    print(f"📊 Completed assessments: {len(completed)}/12")
    
    # Test Career Insights
    print("\n" + "="*60)
    print("🧠 TESTING CAREER INSIGHTS")
    print("="*60)
    
    try:
        insights_result = await master_agent.generate_insights(user_profile)
        
        if insights_result.get('success'):
            print("✅ SUCCESS: Career insights generated!")
            print(f"📝 Message: {insights_result.get('message', '')[:200]}...")
            
            if insights_result.get('key_patterns'):
                print(f"🔍 Key patterns: {len(insights_result['key_patterns'])} found")
            
            if insights_result.get('career_directions'):
                print(f"🎯 Career directions: {len(insights_result['career_directions'])} found")
                
        else:
            print("❌ FAILED: Career insights generation failed")
            print(f"Error: {insights_result.get('message', 'Unknown error')}")
            if insights_result.get('debug_info'):
                print(f"Debug: {insights_result['debug_info']}")
                
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
    
    # Test Action Plan
    print("\n" + "="*60)
    print("🎯 TESTING CAREER ACTION PLAN")
    print("="*60)
    
    try:
        action_plan_result = await master_agent.generate_action_plan(user_profile)
        
        if action_plan_result.get('success'):
            print("✅ SUCCESS: Career action plan generated!")
            print(f"📝 Message: {action_plan_result.get('message', '')[:200]}...")
            
            if action_plan_result.get('key_strengths'):
                print(f"💪 Key strengths: {len(action_plan_result['key_strengths'])} identified")
            
            if action_plan_result.get('immediate_actions'):
                print(f"⚡ Immediate actions: {len(action_plan_result['immediate_actions'])} planned")
                
        else:
            print("❌ FAILED: Career action plan generation failed")
            print(f"Error: {action_plan_result.get('message', 'Unknown error')}")
            if action_plan_result.get('debug_info'):
                print(f"Debug: {action_plan_result['debug_info']}")
                
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
    
    print("\n" + "="*60)
    print("🎉 TESTING COMPLETE")
    print("="*60)
    print(f"✅ User: {user_name} ({len(completed)}/12 assessments)")
    print("✅ Both career insights and action plan generation tested")
    print("🌐 Application running at: http://localhost:8501")
    print("💡 Use the web interface to test with real interactions!")

if __name__ == "__main__":
    asyncio.run(test_complete_user())
