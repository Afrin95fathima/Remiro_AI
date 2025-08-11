"""
Test the WorkflowState TypedDict implementation
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from core.langgraph_workflow import RemiroWorkflow
from core.state_models import UserProfile, ConversationState, AgentType
from core.user_manager import UserManager

def test_workflow():
    """Test the workflow with TypedDict state"""
    
    try:
        # Initialize components
        user_manager = UserManager()
        workflow = RemiroWorkflow()
        
        # Create test user
        test_user = {
            'user_id': 'test_workflow',
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        # Get or create user profile
        user_profile = user_manager.get_user_profile(test_user['user_id'])
        if not user_profile:
            # Create user first, then get profile
            user_manager.create_user(test_user['name'])
            user_profile = user_manager.get_user_profile(test_user['user_id'])
            
        if not user_profile:
            # Create a basic user profile manually for testing
            user_profile = UserProfile(
                user_id=test_user['user_id'],
                name=test_user['name'],
                email=test_user['email']
            )
        
        # Create conversation state
        conversation_state = ConversationState(
            user_profile=user_profile,
            session_id="test_session",
            current_agent=AgentType.MASTER
        )
        
        # Test message processing
        print("🧪 Testing workflow with TypedDict state...")
        result = workflow.process_message_sync(
            conversation_state, 
            "I want to understand my problem solving abilities"
        )
        
        print(f"✅ Workflow Result: {result}")
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        print(f"Agent Type: {result.get('agent_type')}")
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_workflow()
    print(f"\n🎯 Test Result: {'PASSED' if success else 'FAILED'}")
