"""
Test script to verify the conversation flow transitions properly to assessments
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

def test_conversation_flow():
    """Test that conversation transitions to assessment after a few exchanges"""
    
    # Initialize the master agent
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    master_agent = EnhancedMasterAgent(llm)
    
    # Simulate user profile
    user_profile = {
        'name': 'Test User',
        'background': '',
        'assessments': {}
    }
    
    # Test conversation history progression
    test_cases = [
        # Stage 1: Initial chat
        {
            'conversation_history': [],
            'expected_stage': ConversationStage.INITIAL_CHAT
        },
        # Stage 2: Rapport building (1-2 exchanges)
        {
            'conversation_history': [
                {'role': 'user', 'content': 'I need help with my career'},
                {'role': 'assistant', 'content': 'I understand. How are you feeling about it?'}
            ],
            'expected_stage': ConversationStage.RAPPORT_BUILDING
        },
        # Stage 3: Should transition to assessment prep after 3+ exchanges
        {
            'conversation_history': [
                {'role': 'user', 'content': 'I need help with my career'},
                {'role': 'assistant', 'content': 'I understand. How are you feeling about it?'},
                {'role': 'user', 'content': 'I feel confused and lost'},
                {'role': 'assistant', 'content': 'That sounds really tough. Tell me more about that.'},
                {'role': 'user', 'content': 'I just graduated and don\'t know what to do next'},
                {'role': 'assistant', 'content': 'Thank you for sharing that with me.'}
            ],
            'expected_stage': ConversationStage.ASSESSMENT_PREP
        }
    ]
    
    print("🧪 Testing Conversation Flow Transitions\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: Conversation with {len(test_case['conversation_history'])} exchanges")
        
        # Determine stage
        actual_stage = master_agent._determine_conversation_stage(
            user_profile, 
            test_case['conversation_history']
        )
        
        expected_stage = test_case['expected_stage']
        
        print(f"  Expected: {expected_stage.value}")
        print(f"  Actual: {actual_stage.value}")
        
        if actual_stage == expected_stage:
            print("  ✅ PASS\n")
        else:
            print("  ❌ FAIL\n")
            
    print("🎯 Key Point: After 3+ conversation exchanges, the system should suggest starting assessments!")

if __name__ == "__main__":
    test_conversation_flow()
