"""
Comprehensive test for all Remiro AI agents
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from core.state_models import UserProfile, ConversationMessage, AgentType
from agents.master_agent import MasterAgent
from agents.cognitive_abilities import CognitiveAbilitiesAgent

def test_agents():
    """Test all agents functionality"""
    
    try:
        # Initialize LLM
        api_key = os.getenv("GOOGLE_API_KEY")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            max_tokens=2048
        )
        
        # Test Master Agent
        print("🤖 Testing Master Agent...")
        master_agent = MasterAgent(llm)
        
        # Create test user profile
        user_profile = UserProfile(
            user_id="test_user",
            name="Test User",
            email="test@example.com"
        )
        
        # Test routing decision
        routing_result = master_agent.route_conversation(
            "I want to explore my problem-solving abilities",
            user_profile,
            []
        )
        print(f"Routing Result: {routing_result}")
        
        # Test master response
        master_response = master_agent.generate_response(
            "Hello, I'm looking for career guidance",
            user_profile,
            []
        )
        print(f"Master Response: {master_response}")
        
        # Test Cognitive Abilities Agent
        print("\n🧠 Testing Cognitive Abilities Agent...")
        cognitive_agent = CognitiveAbilitiesAgent(llm)
        
        cognitive_response = cognitive_agent.process_interaction(
            "I like breaking down complex problems step by step",
            user_profile,
            []
        )
        print(f"Cognitive Response: {cognitive_response}")
        
        print("\n✅ All agents tested successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_agents()
