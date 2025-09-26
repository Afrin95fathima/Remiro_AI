"""
Simple test for action plan generation to see raw response
"""

import json
import asyncio
import sys
import os
from pathlib import Path

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_action_plan_raw():
    """Test action plan with raw response capture"""
    
    print("🎯 Testing Action Plan Generation - Raw Response Analysis")
    print("=" * 60)
    
    # Load Raja's profile
    raja_profile_path = Path("data/users/raja_d92db087/profile.json")
    
    with open(raja_profile_path, 'r') as f:
        raja_profile = json.load(f)
    
    try:
        from app import MasterCareerAgent, get_llm
        
        llm = get_llm()
        master_agent = MasterCareerAgent(llm)
        
        # Create a simpler prompt first to test JSON structure
        simple_prompt = """Generate a simple career action plan in JSON format:

{
    "success": true,
    "message": "Simple test message",
    "career_summary": {
        "primary_direction": "Test direction"
    },
    "immediate_actions": [
        {"action": "Test action", "timeline": "30 days", "why": "Test reason"}
    ]
}"""

        print("🧪 Testing with simple prompt...")
        response = await llm.ainvoke(simple_prompt)
        print(f"✅ Raw response length: {len(response.content)}")
        print(f"📝 Response preview: {response.content[:200]}")
        print(f"📝 Response end: {response.content[-100:]}")
        
        # Try to parse it
        try:
            cleaned = response.content.strip().replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            print("✅ Simple JSON parsing successful!")
            print(f"Keys: {list(parsed.keys())}")
        except Exception as e:
            print(f"❌ Simple JSON parsing failed: {e}")
            
            # Try to find where JSON might start/end
            content = response.content
            start_brace = content.find('{')
            end_brace = content.rfind('}')
            
            if start_brace != -1 and end_brace != -1:
                json_part = content[start_brace:end_brace+1]
                print(f"🔍 Extracted JSON part: {json_part[:100]}...")
                try:
                    parsed = json.loads(json_part)
                    print("✅ Extracted JSON parsing successful!")
                except Exception as e2:
                    print(f"❌ Even extracted JSON failed: {e2}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_action_plan_raw())
