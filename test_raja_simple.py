#!/usr/bin/env python3
"""
Simple test script to load Raja's data and test generation functions
"""
import json
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment
load_dotenv()

# Simple LLM initialization for testing
def get_llm_for_test():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return None
    
    try:
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_key,
            temperature=0.7,
            max_retries=3,
            request_timeout=60
        )
    except Exception as e:
        print(f"❌ Error initializing LLM: {str(e)}")
        return None

# Initialize LLM
llm = get_llm_for_test()
if not llm:
    print("❌ Cannot initialize LLM, exiting")
    exit(1)

print("✅ LLM initialized successfully")

# Define MasterCareerAgent class (copied from app.py)
class MasterCareerAgent:
    """Master agent for orchestrating the career counseling process"""
    
    def __init__(self, llm):
        self.llm = llm
        self.agent_name = "Master Career Counselor"

    async def generate_insights(self, user_profile):
        """Generate personalized career insights"""
        try:
            # Check if user has completed assessments
            data = user_profile.get('data', {})
            username = data.get('username', user_profile.get('name', 'User'))
            
            # Count completed assessments (exclude username key)
            completed_assessments = sum(1 for key, value in data.items() 
                                     if key != 'username' and isinstance(value, dict) and value.get('summary'))
            
            if completed_assessments < 12:
                return "I don't have enough information about you yet to provide personalized insights."
            
            # Create comprehensive prompt for insights
            insights_prompt = f"""
            As an expert career counselor, provide comprehensive career insights for {username} based on their completed assessments.

            Assessment Data Summary:
            {json.dumps(data, indent=2)}

            Please provide detailed, personalized career insights that include:
            1. **Career Strengths & Unique Value**: What makes them stand out professionally
            2. **Optimal Work Environments**: Where they'll thrive based on their preferences and personality
            3. **Growth Opportunities**: Areas where they can develop and excel
            4. **Potential Career Paths**: Specific roles and industries that align with their profile
            5. **Success Strategies**: Personalized approaches to achieve their career goals

            Make this personal, actionable, and forward-looking. Use their name throughout and reference specific aspects of their assessments.
            
            Format as clear, engaging text with sections and bullet points where helpful.
            """
            
            # Generate insights
            response = await self.llm.ainvoke(insights_prompt)
            insights_text = response.content.strip()
            
            if insights_text and len(insights_text) > 100:
                return insights_text
            else:
                return "I don't have enough information about you yet to provide personalized insights."
                
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return "I don't have enough information about you yet to provide personalized insights."

    async def generate_action_plan(self, user_profile):
        """Generate personalized career action plan"""
        try:
            # Check if user has completed assessments
            data = user_profile.get('data', {})
            username = data.get('username', user_profile.get('name', 'User'))
            
            # Count completed assessments
            completed_assessments = sum(1 for key, value in data.items() 
                                     if key != 'username' and isinstance(value, dict) and value.get('summary'))
            
            if completed_assessments < 12:
                return "Complete more assessments to unlock your personalized action plan."
            
            # Create comprehensive prompt for action plan with simplified structure
            action_plan_prompt = f"""
            Create a comprehensive, personalized career action plan for {username} based on their assessment data.

            Assessment Data:
            {json.dumps(data, indent=2)}

            Generate a JSON response with this EXACT structure (arrays of strings only):

            {{
                "career_objectives": ["objective1", "objective2", "objective3"],
                "immediate_actions": ["action1", "action2", "action3", "action4"],
                "skill_development": ["skill1", "skill2", "skill3"],
                "networking_strategy": ["strategy1", "strategy2", "strategy3"],
                "personalized_strategies": ["strategy1", "strategy2", "strategy3"],
                "next_steps": ["step1", "step2", "step3", "step4"],
                "success_metrics": ["metric1", "metric2", "metric3"]
            }}

            Keep each item concise but actionable. Make it specific to their profile and assessments.
            Respond with ONLY the JSON, no additional text.
            """
            
            # Generate action plan
            response = await self.llm.ainvoke(action_plan_prompt)
            action_plan_text = response.content.strip()
            
            # Clean JSON response
            if action_plan_text.startswith("```json"):
                action_plan_text = action_plan_text.replace("```json", "").replace("```", "").strip()
            
            try:
                parsed_plan = json.loads(action_plan_text)
                return json.dumps(parsed_plan)  # Return as JSON string
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print(f"Raw response: {action_plan_text[:200]}...")
                return "Complete more assessments to unlock your personalized action plan."
                
        except Exception as e:
            print(f"Error generating action plan: {str(e)}")
            return "Complete more assessments to unlock your personalized action plan."

# Initialize agent
master_agent = MasterCareerAgent(llm)

print("\n" + "="*50)
print("LOADING RAJA'S DATA")
print("="*50)

# Load Raja's profile directly
profile_path = Path("data/users/raja_d92db087/profile.json")

if not profile_path.exists():
    print(f"❌ Profile not found at {profile_path}")
    exit(1)

try:
    with open(profile_path, 'r', encoding='utf-8') as f:
        user_data = json.load(f)
    print("✅ Successfully loaded Raja's profile data")
    print(f"📊 Profile keys: {list(user_data.keys())}")
    
    # Check data structure
    if 'data' in user_data:
        data_keys = list(user_data['data'].keys())
        print(f"📋 Data keys: {data_keys}")
        
        # Count assessments
        completed_count = sum(1 for key, value in user_data['data'].items() 
                             if key != 'username' and isinstance(value, dict) and value.get('summary'))
        print(f"✅ Completed assessments: {completed_count}/12")
    else:
        print("❌ No 'data' key found in profile")
        print(f"Available keys: {list(user_data.keys())}")
        
except Exception as e:
    print(f"❌ Error loading profile: {str(e)}")
    exit(1)

print("\n" + "="*50)
print("TESTING CAREER INSIGHTS")
print("="*50)

try:
    insights = asyncio.run(master_agent.generate_insights(user_data))
    if insights and insights != "I don't have enough information about you yet to provide personalized insights.":
        print("✅ SUCCESS: Career insights generated")
        print(f"📊 Insights length: {len(insights)} characters")
        print(f"📝 Preview: {insights[:200]}...")
        insights_success = True
    else:
        print("❌ FAILED: Got fallback message for insights")
        print(f"Response: {insights}")
        insights_success = False
except Exception as e:
    print(f"❌ ERROR generating insights: {str(e)}")
    insights_success = False

print("\n" + "="*50)
print("TESTING ACTION PLAN")
print("="*50)

try:
    action_plan = asyncio.run(master_agent.generate_action_plan(user_data))
    if action_plan and action_plan != "Complete more assessments to unlock your personalized action plan.":
        print("✅ SUCCESS: Action plan generated")
        print(f"📊 Action plan type: {type(action_plan)}")
        
        # Try to parse as JSON if it's a string
        if isinstance(action_plan, str):
            try:
                parsed_plan = json.loads(action_plan)
                print(f"📋 Action plan structure: {list(parsed_plan.keys())}")
                print(f"📝 JSON length: {len(action_plan)} characters")
                action_plan_success = True
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {str(e)}")
                print(f"📝 Raw response preview: {action_plan[:300]}...")
                action_plan_success = False
        else:
            print(f"📋 Action plan keys: {list(action_plan.keys()) if isinstance(action_plan, dict) else 'Not a dict'}")
            action_plan_success = True
    else:
        print("❌ FAILED: Got fallback message for action plan")
        print(f"Response: {action_plan}")
        action_plan_success = False
except Exception as e:
    print(f"❌ ERROR generating action plan: {str(e)}")
    action_plan_success = False

print("\n" + "="*50)
print("FINAL RESULTS")
print("="*50)

print(f"Career Insights: {'✅ SUCCESS' if insights_success else '❌ FAILED'}")
print(f"Action Plan: {'✅ SUCCESS' if action_plan_success else '❌ FAILED'}")

if insights_success and action_plan_success:
    print("\n🎉 COMPLETE SUCCESS: Both features working!")
elif insights_success or action_plan_success:
    print("\n⚠️ PARTIAL SUCCESS: One feature working")
else:
    print("\n❌ COMPLETE FAILURE: Both features failed")

print("="*50)
