"""
Test the Master Agent with the new Gemini model after quota fix
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

def test_master_agent_fix():
    """Test that Master Agent works after switching models"""
    
    print("🔧 TESTING MASTER AGENT AFTER QUOTA FIX")
    print("=" * 50)
    
    try:
        # Initialize with new model
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",  # Switched from gemini-2.0-flash-exp
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
        
        print("📡 Testing API connection with new model...")
        response = master_agent.process_conversation_sync(
            "Hi, I need help with my career",
            user_profile,
            []
        )
        
        if response.get('success', True):
            print("✅ SUCCESS: Master Agent is working!")
            print(f"   Response: {response.get('message', '')[:80]}...")
            print(f"   Stage: {response.get('stage', 'unknown')}")
            return True
        else:
            print("❌ FAILED: Master Agent returned error")
            print(f"   Error: {response.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        if "quota" in str(e).lower() or "429" in str(e):
            print("❌ QUOTA STILL EXCEEDED")
            print("   The API key has reached daily limits")
            print("   Solutions:")
            print("   1. Wait until tomorrow for quota reset")
            print("   2. Upgrade to paid Google AI Studio plan")
            print("   3. Use a different API key")
        else:
            print(f"❌ OTHER ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_master_agent_fix()
    if success:
        print("\n🎉 Master Agent is working! The app should be functional now.")
    else:
        print("\n⚠️  Master Agent still has issues. Check the solutions above.")
