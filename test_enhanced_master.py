"""
Test the Enhanced Master Agent functionality
"""

import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from app import get_llm
from agents.master_agent import EnhancedMasterAgent

async def test_enhanced_master_agent():
    """Test the Enhanced Master Agent capabilities"""
    
    print("🧪 Testing Enhanced Master Agent")
    print("=" * 50)
    
    # Initialize
    llm = get_llm()
    enhanced_master = EnhancedMasterAgent(llm)
    
    # Test profile
    test_profile = {
        'name': 'Alex',
        'background': 'Professional',
        'assessments': {}
    }
    
    # Test conversation history
    conversation_history = [
        {'role': 'user', 'content': 'What is the gold rate in India today?'},
        {'role': 'assistant', 'content': 'I need to understand more about your interest in gold rates to give you the most helpful information.'}
    ]
    
    print("📋 Test 1: General Question with Follow-up")
    print("-" * 30)
    
    try:
        response = await enhanced_master.process_conversation(
            "What is the gold rate in India today?",
            test_profile,
            []
        )
        
        print(f"✅ Success: {response.get('success', True)}")
        print(f"📝 Message: {response.get('message', 'No message')[:200]}...")
        print(f"🎯 Stage: {response.get('stage', 'Unknown')}")
        print(f"❓ Follow-up questions: {len(response.get('follow_up_questions', []))}")
        
        if response.get('follow_up_questions'):
            print("Follow-up questions:")
            for i, q in enumerate(response['follow_up_questions'][:2], 1):
                print(f"  {i}. {q}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n📋 Test 2: Career Question")
    print("-" * 30)
    
    try:
        response = await enhanced_master.process_conversation(
            "I'm confused about my career direction and need guidance",
            test_profile,
            []
        )
        
        print(f"✅ Success: {response.get('success', True)}")
        print(f"📝 Message: {response.get('message', 'No message')[:200]}...")
        print(f"🎯 Stage: {response.get('stage', 'Unknown')}")
        print(f"🔄 Requires action: {response.get('requires_action', False)}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n📋 Test 3: Assessment Orchestration")
    print("-" * 30)
    
    try:
        assessment_flow = await enhanced_master.orchestrate_assessment_flow(test_profile)
        
        print(f"📊 Status: {assessment_flow.get('status', 'Unknown')}")
        print(f"📈 Progress: {assessment_flow.get('completed_count', 0)}/{assessment_flow.get('total_count', 12)}")
        print(f"🎯 Next dimension: {assessment_flow.get('next_dimension', 'None')}")
        print(f"💬 Message: {assessment_flow.get('message', 'No message')[:150]}...")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Enhanced Master Agent Test Complete!")
    print("🌐 Check the web interface at: http://localhost:8502")

if __name__ == "__main__":
    asyncio.run(test_enhanced_master_agent())
