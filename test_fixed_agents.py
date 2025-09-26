"""
Quick test to verify all agents are working properly after fixes
"""

import os
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_llm_initialization():
    """Test LLM initialization"""
    print("🔍 Testing LLM initialization...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "YOUR_GOOGLE_API_KEY_HERE":
            print("❌ No valid Google API key found")
            return False
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        print("✅ LLM initialized successfully")
        return llm
        
    except Exception as e:
        print(f"❌ LLM initialization failed: {e}")
        return False

def test_master_agent(llm):
    """Test advanced master agent"""
    print("\n🤖 Testing Advanced Master Agent...")
    
    try:
        from agents.advanced_master_agent import AdvancedMasterAgent
        
        master_agent = AdvancedMasterAgent(llm)
        print(f"✅ Master Agent initialized with {len(master_agent.agents)} agents")
        
        # Test a simple interaction
        response = master_agent.process_conversation("Hi there!", "test_user_123")
        
        if response and 'message' in response:
            print("✅ Master Agent conversation test successful")
            print(f"📝 Response preview: {response['message'][:100]}...")
            return True
        else:
            print("❌ Master Agent conversation test failed")
            return False
            
    except Exception as e:
        print(f"❌ Master Agent test failed: {e}")
        return False

def test_individual_agents(llm):
    """Test individual agents"""
    print("\n🔧 Testing Individual Agents...")
    
    agent_status = {}
    
    try:
        from agents.enhanced_interests import InterestsAgent
        from agents.enhanced_skills import SkillsAgent
        from agents.enhanced_personality import PersonalityAgent
        from agents.enhanced_aspirations import AspirationsAgent
        
        # Test core agents
        agents_to_test = [
            ('interests', InterestsAgent),
            ('skills', SkillsAgent),
            ('personality', PersonalityAgent),
            ('aspirations', AspirationsAgent)
        ]
        
        for agent_name, agent_class in agents_to_test:
            try:
                agent = agent_class(llm)
                test_response = agent.process_interaction("I love reading books", "test_user")
                
                if test_response and isinstance(test_response, dict):
                    agent_status[agent_name] = "✅ Working"
                else:
                    agent_status[agent_name] = "❌ Response issue"
                    
            except Exception as e:
                agent_status[agent_name] = f"❌ Error: {str(e)[:50]}..."
        
        # Test remaining agents
        try:
            from agents.enhanced_remaining_agents import (
                MotivationsValuesAgent, CognitiveAbilitiesAgent,
                StrengthsWeaknessesAgent, LearningPreferencesAgent,
                TrackRecordAgent, EmotionalIntelligenceAgent,
                ConstraintsAgent, PhysicalContextAgent
            )
            
            remaining_agents = [
                ('motivations_values', MotivationsValuesAgent),
                ('cognitive_abilities', CognitiveAbilitiesAgent),
                ('strengths_weaknesses', StrengthsWeaknessesAgent),
                ('learning_preferences', LearningPreferencesAgent),
                ('track_record', TrackRecordAgent),
                ('emotional_intelligence', EmotionalIntelligenceAgent),
                ('constraints', ConstraintsAgent),
                ('physical_context', PhysicalContextAgent)
            ]
            
            for agent_name, agent_class in remaining_agents:
                try:
                    agent = agent_class(llm)
                    agent_status[agent_name] = "✅ Working"
                except Exception as e:
                    agent_status[agent_name] = f"❌ Error: {str(e)[:50]}..."
                    
        except Exception as e:
            print(f"❌ Could not import remaining agents: {e}")
    
    except Exception as e:
        print(f"❌ Core agents import failed: {e}")
    
    # Print results
    print("\n📊 Agent Status Report:")
    for agent_name, status in agent_status.items():
        print(f"   {agent_name}: {status}")
    
    working_count = sum(1 for status in agent_status.values() if "✅" in status)
    total_count = len(agent_status)
    
    print(f"\n📈 Summary: {working_count}/{total_count} agents working properly")
    
    return working_count == total_count

def main():
    """Run all tests"""
    print("🚀 Starting Remiro AI Agent Tests\n")
    
    # Test LLM
    llm = test_llm_initialization()
    if not llm:
        print("\n❌ Tests failed: No LLM available")
        return
    
    # Test Master Agent
    master_working = test_master_agent(llm)
    
    # Test Individual Agents  
    agents_working = test_individual_agents(llm)
    
    # Final summary
    print("\n" + "="*50)
    print("📋 FINAL TEST SUMMARY")
    print("="*50)
    print(f"LLM: ✅ Working")
    print(f"Master Agent: {'✅ Working' if master_working else '❌ Issues'}")
    print(f"Individual Agents: {'✅ All Working' if agents_working else '❌ Some Issues'}")
    
    if master_working and agents_working:
        print("\n🎉 All systems operational! Chat interface should work perfectly.")
    else:
        print("\n⚠️  Some issues detected. Check individual agent status above.")

if __name__ == "__main__":
    main()