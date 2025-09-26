#!/usr/bin/env python3
"""
Quick test script to debug the Master Agent issue
"""

import os
from dotenv import load_dotenv
load_dotenv()

# Test the Master Agent directly
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.master_agent import EnhancedMasterAgent

def test_master_agent():
    print("=== MASTER AGENT TEST ===")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✅ API Key: {api_key[:10]}...")
    
    try:
        # Initialize LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Using Gemini 2.0 Flash
            google_api_key=api_key,
            temperature=0.7,
            max_retries=2,
            request_timeout=30
        )
        print("✅ LLM initialized")
        
        # Initialize Master Agent
        master_agent = EnhancedMasterAgent(llm)
        print("✅ Master Agent initialized")
        
        # Test conversation
        user_profile = {'name': 'Afrin'}
        test_input = "I want career guidance as an AI engineer"
        
        print(f"\n🧪 Testing input: '{test_input}'")
        
        result = master_agent.process_conversation_sync(
            test_input, 
            user_profile, 
            []
        )
        
        print(f"✅ Result: {result.get('message', 'No message')[:100]}...")
        print(f"✅ Success: {result.get('success', False)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_master_agent()
