#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.master_agent import EnhancedMasterAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

def test_master_agent():
    load_dotenv()
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.7,
        max_tokens=500  # Reduced to save quota
    )
    
    # Initialize Master Agent
    master = EnhancedMasterAgent(llm)
    
    # Test user profile
    user_profile = {
        'name': 'TestUser',
        'user_id': 'test_123',
        'interests': {},
        'skills': {},
        'personality': {},
        'aspirations': {},
        'motivations_values': {}
    }
    
    # Test conversations
    test_inputs = [
        "Hello",
        "I want career guidance",
        "What about AI engineering?",
        "Tell me about interview prep"
    ]
    
    conversation_history = []
    
    for i, user_input in enumerate(test_inputs):
        print(f"\n{'='*50}")
        print(f"TEST {i+1}: {user_input}")
        print('='*50)
        
        try:
            # Test the sync method with fallback
            result = master.process_conversation_sync(
                user_input, 
                user_profile, 
                conversation_history
            )
            
            print(f"✅ SUCCESS: {result.get('success', False)}")
            print(f"Action: {result.get('action_type', 'unknown')}")
            print(f"Message: {result.get('message', 'No message')[:200]}...")
            
            # Add to conversation history
            conversation_history.extend([
                {'role': 'user', 'content': user_input},
                {'role': 'assistant', 'content': result.get('message', '')}
            ])
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("SYNC TEST COMPLETE - Master Agent Reliability Check")
    print('='*50)

if __name__ == "__main__":
    test_master_agent()
