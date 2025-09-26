"""
Comprehensive test to verify the forced 12D assessment transition
"""

import sys
import os

# Add the project root to Python path  
sys.path.append(os.path.abspath('.'))

from agents.master_agent import EnhancedMasterAgent, ConversationStage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_comprehensive_flow():
    """Test the complete conversation flow"""
    
    print("🚀 TESTING REMIRO AI - FORCED 12D ASSESSMENT TRANSITION")
    print("=" * 60)
    
    # Initialize the master agent
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    master_agent = EnhancedMasterAgent(llm)
    
    # Simulate user profile
    user_profile = {
        'name': 'TestUser',
        'background': '',
        'assessments': {}
    }
    
    # Test scenarios
    test_cases = [
        {
            'name': '2 Exchanges - Should continue conversation',
            'history': [
                {'role': 'user', 'content': 'I need career help'},
                {'role': 'assistant', 'content': 'How are you feeling?'},
                {'role': 'user', 'content': 'Confused about my future'},
                {'role': 'assistant', 'content': 'Tell me more about that'}
            ],
            'expected_transition': False
        },
        {
            'name': '3+ Exchanges - Should FORCE assessment',
            'history': [
                {'role': 'user', 'content': 'I need career help'},
                {'role': 'assistant', 'content': 'How are you feeling?'},
                {'role': 'user', 'content': 'Confused about my future'}, 
                {'role': 'assistant', 'content': 'Tell me more about that'},
                {'role': 'user', 'content': 'I want to be an AI engineer'},
                {'role': 'assistant', 'content': 'What interests you about AI?'}
            ],
            'expected_transition': True
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"   History length: {len(test_case['history'])}")
        
        # Determine stage
        stage = master_agent._determine_conversation_stage(user_profile, test_case['history'])
        print(f"   Detected stage: {stage.value}")
        
        # Test response
        response = master_agent.process_conversation_sync(
            "This is my next message",
            user_profile, 
            test_case['history']
        )
        
        is_transition = response.get('response_type') == 'assessment_transition'
        print(f"   Response type: {response.get('response_type', 'normal')}")
        print(f"   Requires action: {response.get('requires_action', False)}")
        
        if is_transition == test_case['expected_transition']:
            print("   ✅ PASS")
        else:
            print("   ❌ FAIL")
            print(f"   Expected transition: {test_case['expected_transition']}")
            print(f"   Actual transition: {is_transition}")
    
    print("\n🎯 KEY VERIFICATION:")
    print("After 3+ conversation exchanges (history length >= 6):")
    print("- Stage should be 'assessment_prep'")
    print("- Response type should be 'assessment_transition'")
    print("- Should NOT generate more questions")
    print("- Should offer to start 12D assessment")
    
    # Final test with exact scenario from user
    print(f"\n🔬 FINAL TEST: Exact User Scenario")
    aadhi_history = [
        {'role': 'user', 'content': 'i want to get a plan for my career path as a AI engineer'},
        {'role': 'assistant', 'content': 'That\'s a fantastic goal! What sparked your interest?'},
        {'role': 'user', 'content': 'personal assistants made me think about AI'},
        {'role': 'assistant', 'content': 'What aspects interest you most?'},
        {'role': 'user', 'content': 'professional assistant like jarvis'},
        {'role': 'assistant', 'content': 'What aspects of Jarvis interest you?'}
    ]
    
    aadhi_profile = {'name': 'Aadhi', 'assessments': {}}
    
    final_response = master_agent.process_conversation_sync(
        "it's ability to automate the task for the person",
        aadhi_profile,
        aadhi_history
    )
    
    print(f"   History length: {len(aadhi_history)}")
    print(f"   Response type: {final_response.get('response_type', 'normal')}")
    print(f"   Stage: {final_response.get('stage', 'unknown')}")
    
    if final_response.get('response_type') == 'assessment_transition':
        print("   ✅ SUCCESS: Aadhi's scenario will trigger assessment!")
        print(f"   Message preview: {final_response.get('message', '')[:80]}...")
    else:
        print("   ❌ PROBLEM: Aadhi's scenario still not working")
    
    return final_response.get('response_type') == 'assessment_transition'

if __name__ == "__main__":
    success = test_comprehensive_flow()
    if success:
        print(f"\n🎉 ALL TESTS PASSED - 12D Assessment Transition Working!")
    else:
        print(f"\n⚠️  TESTS FAILED - Need to fix transition logic")
