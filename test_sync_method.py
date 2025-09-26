#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.master_agent import EnhancedMasterAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

def test_sync_fallback():
    load_dotenv()
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.7,
        max_tokens=500
    )
    
    # Initialize Master Agent
    master = EnhancedMasterAgent(llm)
    
    # Test user profile
    user_profile = {
        'name': 'Afrin',
        'user_id': 'test_afrin',
        'interests': {},
        'skills': {},
        'personality': {},
        'aspirations': {},
        'motivations_values': {}
    }
    
    # Test the sync method directly
    print("Testing synchronous response generation...")
    
    try:
        result = master.generate_synchronous_response(
            "i want to start my career as an AI engineer", 
            user_profile, 
            []
        )
        
        print(f"✅ SUCCESS: {result.get('success', False)}")
        print(f"Action: {result.get('action_type', 'unknown')}")
        print(f"Message: {result.get('message', 'No message')[:300]}...")
        print(f"Needs Assessment: {result.get('needs_assessment', False)}")
        
    except Exception as e:
        print(f"❌ ERROR in sync method: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sync_fallback()
