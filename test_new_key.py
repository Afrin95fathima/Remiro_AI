"""
Test new API key and master agent functionality
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.abspath('.'))

from agents.master_agent import EnhancedMasterAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_new_api_key():
    """Test that the new API key works"""
    
    print("🔑 TESTING NEW API KEY")
    print("=" * 30)
    
    try:
        # Initialize with new API key
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.3,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            max_retries=2
        )
        
        master_agent = EnhancedMasterAgent(llm)
        
        # Simple test
        user_profile = {
            'name': 'TestUser',
            'background': '',
            'assessments': {}
        }
        
        print("📡 Testing API connection...")
        response = master_agent.process_conversation_sync(
            "Hello, I need career guidance",
            user_profile,
            []
        )
        
        if response.get('success', True):
            print("✅ SUCCESS: New API key is working!")
            print(f"   Response: {response.get('message', '')[:100]}...")
            return True
        else:
            print("❌ FAILED: Master Agent returned error")
            print(f"   Error: {response.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_new_api_key()
