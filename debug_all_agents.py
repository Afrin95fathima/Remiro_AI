import sys
import os
sys.path.append(r'c:\Users\afrin\OneDrive\Desktop\Remiro AI')

# Debug script to check all 12 agents question data
def debug_agent_questions():
    """Debug all agent question configurations"""
    
    # Create mock LLM for testing
    class MockLLM:
        pass
    
    # Import the EnhancedAgent class
    from app import EnhancedAgent
    
    llm = MockLLM()
    
    # All 12 agent types
    agent_types = [
        'personality', 'interests', 'aspirations', 'skills', 'motivations_values',
        'cognitive_abilities', 'learning_preferences', 'physical_context',
        'strengths_weaknesses', 'emotional_intelligence', 'track_record', 'constraints'
    ]
    
    agent_names = {
        'personality': "Personality & Work Style Counselor",
        'interests': "Career Interests Counselor", 
        'aspirations': "Career Aspirations Counselor",
        'skills': "Skills Assessment Counselor",
        'motivations_values': "Values & Motivations Counselor",
        'cognitive_abilities': "Cognitive Abilities Counselor",
        'learning_preferences': "Learning Preferences Counselor",
        'physical_context': "Work Environment Counselor",
        'strengths_weaknesses': "Strengths & Development Counselor",
        'emotional_intelligence': "Emotional Intelligence Counselor",
        'track_record': "Achievement & Experience Counselor",
        'constraints': "Practical Considerations Counselor"
    }
    
    print("=== DEBUGGING ALL 12 AGENTS ===")
    print()
    
    working_agents = []
    broken_agents = []
    
    for agent_type in agent_types:
        try:
            print(f"Testing {agent_type}...")
            agent = EnhancedAgent(llm, agent_names[agent_type], agent_type)
            
            # Check if questions loaded properly
            questions_data = agent.questions_data
            
            if questions_data and 'questions' in questions_data:
                question_count = len(questions_data['questions'])
                print(f"✅ {agent_type}: {question_count} questions loaded")
                
                # Check if has proper structure
                if question_count == 3:  # Should have exactly 3 questions
                    working_agents.append(agent_type)
                    print(f"   - Has proper 3-question structure")
                else:
                    broken_agents.append(f"{agent_type} (wrong question count: {question_count})")
                    print(f"   ⚠️ Wrong question count: {question_count}")
                    
                # Show first question for verification
                if questions_data['questions']:
                    first_q = questions_data['questions'][0]['question']
                    print(f"   - First question: {first_q[:60]}...")
                    
            else:
                broken_agents.append(f"{agent_type} (no questions data)")
                print(f"❌ {agent_type}: No questions data found!")
                print(f"   - Questions data: {questions_data}")
                
        except Exception as e:
            broken_agents.append(f"{agent_type} (error: {str(e)})")
            print(f"❌ {agent_type}: Error - {str(e)}")
        
        print()
    
    print("=== SUMMARY ===")
    print(f"Working agents ({len(working_agents)}): {working_agents}")
    print(f"Broken agents ({len(broken_agents)}): {broken_agents}")
    
    if len(working_agents) == 12:
        print("🎉 All 12 agents are working properly!")
    else:
        print(f"⚠️ Only {len(working_agents)} out of 12 agents are working!")
        
    return working_agents, broken_agents

if __name__ == "__main__":
    debug_agent_questions()
