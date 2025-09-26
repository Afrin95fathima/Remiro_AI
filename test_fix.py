#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.master_agent import EnhancedMasterAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

def test_fixed_agent():
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
    
    print("Testing fixed Master Agent...")
    
    try:
        # Test the conversation that should trigger fallback
        result = master.process_conversation_sync(
            "i want to know about the 12D agents", 
            user_profile, 
            [
                {'role': 'user', 'content': 'hello'},
                {'role': 'assistant', 'content': 'Hi there!'},
                {'role': 'user', 'content': 'i want to know about the 12D agents'}
            ]
        )
        
        print(f"✅ Success: {result.get('success', False)}")
        print(f"📝 Message Preview: {result.get('message', 'No message')[:150]}...")
        print(f"🎯 Action: {result.get('action_type', 'unknown')}")
        print(f"🔍 Needs Assessment: {result.get('needs_assessment', False)}")
        
        if "technical difficulties" in result.get('message', ''):
            print("❌ Still showing old error!")
        elif "12D analysis" in result.get('message', '') or "12 Dimensions" in result.get('message', ''):
            print("✅ Perfect! Responding to 12D query correctly!")
        else:
            print("✅ Fixed error, but could improve 12D response!")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fixed_agent()
