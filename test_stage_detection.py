"""
Quick test to verify conversation count and stage transitions work properly
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.abspath('.'))

from agents.master_agent import EnhancedMasterAgent, ConversationStage

def test_conversation_stages():
    """Test conversation stage detection"""
    
    master_agent = EnhancedMasterAgent(None)  # We don't need the LLM for this test
    
    user_profile = {'name': 'Aadhi', 'assessments': {}}
    
    # Test case: conversation with 6 exchanges (like the example you showed)
    conversation_history = [
        {'role': 'user', 'content': 'i want to get a plan for my career path as a AI engineer'},
        {'role': 'assistant', 'content': 'That\'s a fantastic goal! What sparked your interest in AI engineering?'},
        {'role': 'user', 'content': 'personal assistants made me think about AI'},
        {'role': 'assistant', 'content': 'I see! What aspects of personal assistants interest you most?'},
        {'role': 'user', 'content': 'professional assistant like jarvis'},
        {'role': 'assistant', 'content': 'What aspects of Jarvis are most interesting to you?'},
        {'role': 'user', 'content': 'it\'s ability to automate the task for the person'},
        {'role': 'assistant', 'content': 'What kind of tasks do you find yourself wishing you could automate?'},
        {'role': 'user', 'content': 'tracking my daily tasks and making me remind to work'},
        {'role': 'assistant', 'content': 'What\'s been the most challenging part about keeping track of everything?'},
        {'role': 'user', 'content': 'my tasks'},
        {'role': 'assistant', 'content': 'What kind of system have you tried using to manage your tasks?'}
    ]
    
    stage = master_agent._determine_conversation_stage(user_profile, conversation_history)
    conversation_count = len(conversation_history)
    
    print(f"🧪 Testing Conversation Stage Detection")
    print(f"Conversation exchanges: {conversation_count}")
    print(f"Current stage: {stage.value}")
    print(f"Should be in: ASSESSMENT_PREP (since count >= 4)")
    
    if stage == ConversationStage.ASSESSMENT_PREP:
        print("✅ CORRECT: Should transition to assessment now")
    else:
        print("❌ PROBLEM: Still not transitioning to assessment")
    
    return stage == ConversationStage.ASSESSMENT_PREP

if __name__ == "__main__":
    test_conversation_stages()
