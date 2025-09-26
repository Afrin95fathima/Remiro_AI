"""
Test script to verify insights and action plan generation for Raja
"""

import json
import asyncio
import sys
import os
from pathlib import Path

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_raja_insights_and_action_plan():
    """Test insights and action plan for Raja specifically"""
    
    print("🧪 Testing Raja's Insights and Action Plan Generation")
    print("=" * 60)
    
    # Load Raja's profile
    raja_profile_path = Path("data/users/raja_d92db087/profile.json")
    
    if not raja_profile_path.exists():
        print("❌ Raja's profile not found!")
        return False
    
    with open(raja_profile_path, 'r') as f:
        raja_profile = json.load(f)
    
    print(f"👤 User: {raja_profile.get('name', 'Unknown')}")
    print(f"🎓 Background: {raja_profile.get('background', 'Unknown')}")
    
    # Count completed assessments
    assessments = raja_profile.get('assessments', {})
    completed = [k for k, v in assessments.items() if v.get('completed', False)]
    print(f"📊 Completed assessments: {len(completed)}/12")
    print(f"✅ Assessments: {completed}")
    
    # Test data structure access
    print("\n🔍 Testing Data Structure Access:")
    for dim in completed[:3]:  # Test first 3
        data = assessments[dim].get('data', {})
        if data:
            print(f"✅ {dim}: Has data structure")
            print(f"   Summary: {data.get('summary', 'No summary')[:50]}...")
            print(f"   Strengths: {len(data.get('strengths', []))} items")
        else:
            print(f"❌ {dim}: No data found")
    
    # Import and test the MasterCareerAgent
    try:
        from app import MasterCareerAgent, get_llm
        
        print("\n🤖 Initializing Master Agent...")
        llm = get_llm()
        master_agent = MasterCareerAgent(llm)
        
        # Test insights generation
        print("\n📊 Testing Insights Generation...")
        try:
            insights = await master_agent.generate_insights(raja_profile)
            print(f"Success: {insights.get('success', False)}")
            
            if insights.get('success'):
                print("✅ Insights generated successfully!")
                print(f"Message preview: {insights.get('message', '')[:100]}...")
                print(f"Key patterns: {len(insights.get('key_patterns', []))}")
                print(f"Career directions: {len(insights.get('career_directions', []))}")
            else:
                print(f"❌ Insights failed: {insights.get('message', 'Unknown error')}")
                if insights.get('technical_error'):
                    print(f"Technical error: {insights['technical_error']}")
                    
        except Exception as e:
            print(f"❌ Exception during insights: {e}")
        
        # Test action plan generation
        print("\n🎯 Testing Action Plan Generation...")
        try:
            action_plan = await master_agent.generate_action_plan(raja_profile)
            print(f"Success: {action_plan.get('success', False)}")
            
            if action_plan.get('success'):
                print("✅ Action plan generated successfully!")
                print(f"Message preview: {action_plan.get('message', '')[:100]}...")
                print(f"Career summary: {bool(action_plan.get('career_summary'))}")
                print(f"Immediate actions: {len(action_plan.get('immediate_actions', []))}")
                print(f"Career paths: {len(action_plan.get('career_paths', []))}")
            else:
                print(f"❌ Action plan failed: {action_plan.get('message', 'Unknown error')}")
                if action_plan.get('technical_error'):
                    print(f"Technical error: {action_plan['technical_error']}")
                    
        except Exception as e:
            print(f"❌ Exception during action plan: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing or initializing: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_raja_insights_and_action_plan())
