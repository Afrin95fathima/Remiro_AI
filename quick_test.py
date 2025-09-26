#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.master_agent import EnhancedMasterAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

def quick_test():
    load_dotenv()
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.7
    )
    
    # Initialize Master Agent
    master = EnhancedMasterAgent(llm)
    
    # Test user profile
    user_profile = {
        'name': 'Afrin',
        'user_id': 'test_afrin'
    }
    
    print("Testing sync fallback with '12 D analysis'...")
    
    try:
        # Test the full sync method (this should trigger the fallback)
        result = master.process_conversation_sync(
            "i want to start the 12 D analysis", 
            user_profile, 
            [
                {'role': 'user', 'content': 'hello'},
                {'role': 'assistant', 'content': 'Hi there!'},
                {'role': 'user', 'content': 'i want to start the 12 D analysis'}
            ]
        )
        
        print(f"✅ Result: {result.get('success', False)}")
        print(f"📝 Message: {result.get('message', 'No message')[:200]}...")
        print(f"🎯 Action: {result.get('action_type', 'unknown')}")
        
        if "technical difficulties" in result.get('message', ''):
            print("❌ Still showing old error message!")
        else:
            print("✅ New sync fallback working!")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()
