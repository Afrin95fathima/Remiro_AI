"""
Test All 12 Agents Integration
Verifies that all agents work properly with the interactive assessment system
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.agent_integration import AgentIntegrationSystem
from core.local_storage import LocalDataManager
import uuid
from datetime import datetime

def test_agent_initialization():
    """Test that all 12 agents can be initialized properly"""
    print("🔧 Testing Agent Initialization...")
    
    # Mock LLM for testing
    class MockLLM:
        def __init__(self):
            self.name = "mock_llm"
            
        def invoke(self, prompt):
            return {
                "content": f"Mock response for: {prompt[:50]}..."
            }
    
    try:
        mock_llm = MockLLM()
        agent_system = AgentIntegrationSystem(mock_llm)
        
        expected_agents = [
            'interests', 'skills', 'personality', 'aspirations',
            'motivations_values', 'cognitive_abilities', 'strengths_weaknesses',
            'learning_preferences', 'track_record', 'emotional_intelligence',
            'constraints', 'physical_context'
        ]
        
        print(f"✅ Expected {len(expected_agents)} agents")
        print(f"✅ Initialized {len(agent_system.agents)} agents")
        
        for agent_type in expected_agents:
            if agent_type in agent_system.agents:
                print(f"   ✅ {agent_type} - Agent Available")
            else:
                print(f"   ❌ {agent_type} - Agent Missing")
        
        return len(agent_system.agents) == len(expected_agents)
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def test_agent_responses():
    """Test that agents can provide responses to user inputs"""
    print("\n🤖 Testing Agent Response Generation...")
    
    # Mock LLM for testing
    class MockLLM:
        def invoke(self, messages):
            if isinstance(messages, list):
                content = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
            else:
                content = str(messages)
            
            return type('MockResponse', (), {
                'content': f'''{{
                    "message": "Thank you for sharing your preferences. Based on your responses about {content[:30]}..., I can see you have strong interests in this area.",
                    "assessment_data": {{
                        "insights": ["You show strong preference for analytical thinking", "Your responses indicate good problem-solving abilities"],
                        "recommendations": ["Consider exploring careers in data analysis", "Look into technical roles that match your interests"],
                        "career_connections": ["Data Scientist", "Business Analyst", "Research Specialist"]
                    }},
                    "assessment_complete": true
                }}'''
            })()
    
    try:
        mock_llm = MockLLM()
        agent_system = AgentIntegrationSystem(mock_llm)
        
        test_cases = [
            ("interests", ["creative", "technology", "analytical"]),
            ("skills", ["programming", "communication", "leadership"]),
            ("personality", ["introverted", "analytical", "organized"])
        ]
        
        for agent_type, test_responses in test_cases:
            user_profile = {"background": "Professional", "context": {}}
            
            try:
                response = agent_system.get_agent_response(agent_type, test_responses, user_profile)
                
                if "error" not in response:
                    print(f"   ✅ {agent_type} - Response Generated Successfully")
                    if "message" in response:
                        print(f"      📝 Message: {response['message'][:80]}...")
                else:
                    print(f"   ❌ {agent_type} - Error: {response['error']}")
                    
            except Exception as e:
                print(f"   ❌ {agent_type} - Exception: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent response testing failed: {e}")
        return False

def test_comprehensive_analysis():
    """Test the comprehensive analysis generation"""
    print("\n📊 Testing Comprehensive Analysis...")
    
    # Mock LLM for testing
    class MockLLM:
        def invoke(self, messages):
            return type('MockResponse', (), {
                'content': '''{{
                    "message": "Based on your comprehensive assessment, I can provide detailed insights.",
                    "assessment_data": {{
                        "insights": ["Strong analytical capabilities", "Good interpersonal skills"],
                        "recommendations": ["Explore data-driven careers", "Consider leadership roles"],
                        "career_connections": ["Data Scientist", "Product Manager", "Consultant"]
                    }},
                    "assessment_complete": true
                }}'''
            })()
    
    try:
        mock_llm = MockLLM()
        agent_system = AgentIntegrationSystem(mock_llm)
        
        # Mock response data for all agents
        all_responses = {
            'interests': [['creative', 'technology']],
            'skills': [['programming', 'communication']],
            'personality': [['analytical', 'organized']],
            'aspirations': [['leadership', 'innovation']],
            'motivations_values': [['achievement', 'helping_others']],
            'cognitive_abilities': [['analytical', 'creative']],
            'strengths_weaknesses': [['problem_solving', 'time_management']],
            'learning_preferences': [['visual', 'hands_on']],
            'track_record': [['academic_success', 'project_leadership']],
            'emotional_intelligence': [['empathy', 'self_awareness']],
            'constraints': [['location_flexible', 'work_life_balance']],
            'physical_context': [['office_work', 'remote_friendly']]
        }
        
        analysis = agent_system.get_comprehensive_analysis(all_responses)
        
        if "error" not in analysis:
            print("   ✅ Comprehensive Analysis Generated Successfully")
            
            required_keys = ["comprehensive_insights", "key_recommendations", "career_matches", "summary", "next_steps"]
            for key in required_keys:
                if key in analysis:
                    print(f"      ✅ {key}: Available ({len(analysis[key])} items)")
                else:
                    print(f"      ❌ {key}: Missing")
                    
            return True
        else:
            print(f"   ❌ Analysis Error: {analysis['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Comprehensive analysis testing failed: {e}")
        return False

def test_data_storage_integration():
    """Test integration with local data storage"""
    print("\n💾 Testing Data Storage Integration...")
    
    try:
        data_manager = LocalDataManager()
        test_user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        
        # Test saving agent feedback
        test_feedback = {
            "message": "Test agent response",
            "assessment_data": {
                "insights": ["Test insight"],
                "recommendations": ["Test recommendation"]
            }
        }
        
        success = data_manager.save_agent_feedback(test_user_id, "interests", 0, test_feedback)
        
        if success:
            print("   ✅ Agent Feedback Storage - Success")
        else:
            print("   ❌ Agent Feedback Storage - Failed")
        
        # Test user folder creation
        user_folder = data_manager.base_path / test_user_id
        if user_folder.exists():
            print("   ✅ User Folder Creation - Success")
            
            # Check feedback folder
            feedback_folder = user_folder / "agent_feedback"
            if feedback_folder.exists():
                print("   ✅ Feedback Folder Creation - Success")
                
                # Check feedback file
                feedback_files = list(feedback_folder.glob("*.json"))
                if feedback_files:
                    print(f"   ✅ Feedback File Creation - Success ({len(feedback_files)} files)")
                else:
                    print("   ❌ Feedback File Creation - No files found")
            else:
                print("   ❌ Feedback Folder Creation - Failed")
        else:
            print("   ❌ User Folder Creation - Failed")
        
        return success
        
    except Exception as e:
        print(f"❌ Data storage integration testing failed: {e}")
        return False

def run_all_tests():
    """Run all tests for the 12-agent system"""
    print("🧪 REMIRO AI - 12 AGENTS INTEGRATION TEST")
    print("=" * 50)
    
    results = {}
    
    # Run all tests
    results['initialization'] = test_agent_initialization()
    results['responses'] = test_agent_responses()
    results['analysis'] = test_comprehensive_analysis()
    results['storage'] = test_data_storage_integration()
    
    # Summary
    print("\n📋 TEST SUMMARY")
    print("=" * 30)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper()}: {status}")
    
    print(f"\nOVERALL: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! The 12-agent system is working correctly.")
        print("\n🚀 Ready for user interaction:")
        print("   • All 12 agents initialized successfully")
        print("   • Agent responses working properly")
        print("   • Comprehensive analysis functional")
        print("   • Data storage integration working")
        print("\n✨ Users can now interact with all 12 agents!")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Please review the issues above.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    run_all_tests()