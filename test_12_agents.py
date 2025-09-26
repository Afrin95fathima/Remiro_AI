"""
Test Script for 12-Agent Interactive Assessment System
Verifies that all agents are properly initialized and can provide responses
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_agent_integration_system():
    """Test the agent integration system with all 12 agents"""
    
    print("🧪 Testing Remiro AI 12-Agent Integration System")
    print("=" * 60)
    
    try:
        # Initialize LLM
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        print("✅ LLM initialized successfully")
        
        # Initialize Agent Integration System
        from ui.agent_integration import AgentIntegrationSystem
        
        agent_system = AgentIntegrationSystem(llm)
        print(f"✅ Agent Integration System initialized with {len(agent_system.agents)} agents")
        
        # List all agents
        print("\n📋 Available Agents:")
        for i, agent_type in enumerate(agent_system.agents.keys(), 1):
            print(f"  {i:2d}. {agent_type.replace('_', ' ').title()}")
        
        print("\n🧪 Testing Agent Responses:")
        print("-" * 40)
        
        # Test data
        user_profile = {
            "background": "Professional",
            "context": {"experience_level": "mid-level", "industry": "technology"}
        }
        
        # Test sample responses for each agent
        test_responses = {
            'interests': ['technology', 'creative', 'analytical'],
            'skills': ['programming', 'problem_solving', 'communication'],
            'personality': ['analytical', 'creative', 'collaborative'],
            'aspirations': ['leadership', 'innovation', 'growth'],
            'motivations_values': ['achievement', 'creativity', 'helping_others'],
            'cognitive_abilities': ['analytical_thinking', 'creative_problem_solving'],
            'strengths_weaknesses': ['technical_skills', 'communication'],
            'learning_preferences': ['visual', 'hands_on', 'collaborative'],
            'track_record': ['projects', 'leadership_experience'],
            'emotional_intelligence': ['empathy', 'self_awareness'],
            'constraints': ['time_availability', 'location_flexibility'],
            'physical_context': ['remote_work', 'collaborative_environment']
        }
        
        successful_agents = 0
        failed_agents = []
        
        # Test each agent
        for agent_type, test_data in test_responses.items():
            print(f"\n🔬 Testing {agent_type.replace('_', ' ').title()} Agent...")
            
            try:
                response = agent_system.get_agent_response(agent_type, test_data, user_profile)
                
                if "error" in response:
                    print(f"   ❌ Error: {response['error']}")
                    failed_agents.append(agent_type)
                else:
                    print(f"   ✅ Success: Got response with message length {len(response.get('message', ''))}")
                    if response.get('assessment_data'):
                        print(f"   📊 Assessment data included")
                    successful_agents += 1
                    
            except Exception as e:
                print(f"   ❌ Exception: {str(e)}")
                failed_agents.append(agent_type)
        
        print(f"\n📊 Test Results:")
        print(f"   ✅ Successful agents: {successful_agents}/12")
        print(f"   ❌ Failed agents: {len(failed_agents)}/12")
        
        if failed_agents:
            print(f"   Failed agents: {', '.join(failed_agents)}")
        
        # Test comprehensive analysis
        print(f"\n🧠 Testing Comprehensive Analysis...")
        try:
            analysis = agent_system.get_comprehensive_analysis(test_responses)
            
            if "error" in analysis:
                print(f"   ❌ Analysis Error: {analysis['error']}")
            else:
                print(f"   ✅ Analysis Success:")
                print(f"      - Insights: {len(analysis.get('comprehensive_insights', []))}")
                print(f"      - Recommendations: {len(analysis.get('key_recommendations', []))}")
                print(f"      - Career matches: {len(analysis.get('career_matches', []))}")
                
        except Exception as e:
            print(f"   ❌ Analysis Exception: {str(e)}")
        
        # Summary
        print(f"\n🎯 System Status:")
        if successful_agents == 12:
            print("   🎉 ALL 12 AGENTS ARE WORKING PERFECTLY!")
            print("   🚀 Interactive assessment system is ready for users")
        elif successful_agents >= 10:
            print("   ✅ Most agents working - system functional with minor issues")
        elif successful_agents >= 6:
            print("   ⚠️  Some agents working - partial functionality available")
        else:
            print("   ❌ Major issues detected - system needs debugging")
        
        return successful_agents == 12
        
    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_agent_integration_system()
    
    if success:
        print("\n🎉 ALL SYSTEMS GO! Your 12-agent interactive assessment is ready!")
    else:
        print("\n⚠️  System needs attention before full deployment.")