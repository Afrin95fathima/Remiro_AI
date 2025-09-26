"""
Test the forced assessment transition logic
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

def test_forced_transition():
    """Test that the agent forces assessment transition"""
    
    # Initialize the master agent
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    master_agent = EnhancedMasterAgent(llm)
    
    # Simulate user profile
    user_profile = {
        'name': 'Aadhi',
        'background': '',
        'assessments': {}
    }
    
    # Simulate conversation with 6 exchanges (should trigger forced transition)
    conversation_history = [
        {'role': 'user', 'content': 'i want to get a plan for my career path as a AI engineer'},
        {'role': 'assistant', 'content': 'That\'s a fantastic goal! What sparked your interest in AI engineering?'},
        {'role': 'user', 'content': 'personal assistants made me think about AI'},
        {'role': 'assistant', 'content': 'I see! What aspects of personal assistants interest you most?'},
        {'role': 'user', 'content': 'professional assistant like jarvis'},
        {'role': 'assistant', 'content': 'What aspects of Jarvis are most interesting to you?'},
    ]
    
    # Test the sync version
    print("🧪 Testing Forced Assessment Transition")
    print(f"Conversation history length: {len(conversation_history)}")
    
    response = master_agent.process_conversation_sync(
        "it's ability to automate the task for the person",
        user_profile,
        conversation_history
    )
    
    print(f"Response type: {response.get('response_type', 'normal')}")
    print(f"Stage: {response.get('stage', 'unknown')}")
    print(f"Requires action: {response.get('requires_action', False)}")
    print(f"Message preview: {response.get('message', '')[:100]}...")
    
    if response.get('response_type') == 'assessment_transition':
        print("✅ SUCCESS: Forced assessment transition working!")
    else:
        print("❌ FAILED: Still generating normal responses")
    
    return response.get('response_type') == 'assessment_transition'

if __name__ == "__main__":
    test_forced_transition()
