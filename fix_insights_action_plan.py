#!/usr/bin/env python3
"""
Complete Fix for Missing Agents and Non-Working Insights/Action Plan
This script will fix both issues:
1. Missing 4 agents after 8+ completed assessments  
2. Non-functioning insights and action plan generation
"""

import json
import asyncio
from datetime import datetime

def create_enhanced_prompts():
    """Create enhanced prompts for better insights and action plans"""
    
    enhanced_insights_prompt = '''
As an expert Master Career Counselor, analyze {user_name}'s comprehensive assessment data to provide deep, personalized career insights:

ASSESSMENT DATA ANALYSIS:
{assessment_data_formatted}

COMPLETED ASSESSMENTS: {completed_count}/12

Generate highly personalized insights based on their specific responses, not generic advice:

{{
    "success": true,
    "message": "🌟 {user_name}, based on your {completed_count} completed assessments, I've identified some fascinating patterns about your career potential that are uniquely yours...",
    "key_patterns": [
        "Specific patterns from their actual responses - not generic",
        "Unique combinations of their strengths and interests", 
        "How their values align with their aspirations",
        "Distinctive thinking styles and preferences they showed"
    ],
    "career_directions": [
        "Specific career paths that match their exact profile",
        "Industries that align with their values and interests",
        "Roles that leverage their unique strengths combination",
        "Growth opportunities based on their learning preferences"
    ],
    "personalized_insights": [
        "What makes them unique in the marketplace",
        "Their natural leadership or collaboration style",
        "How they solve problems differently than others",
        "Their ideal work environment and culture fit"
    ],
    "next_priorities": [
        "Which remaining assessments would provide the most valuable insights",
        "Areas that would unlock their biggest potential",
        "Skills that would amplify their natural strengths"
    ],
    "confidence_level": "Based on {completed_count} assessments, I'm confident about these insights. Complete {remaining_count} more for a complete picture."
}}
'''
    
    enhanced_action_plan_prompt = '''
As a Master Career Counselor, create a highly personalized, actionable career roadmap for {user_name} based on their complete 12D assessment profile:

USER PROFILE:
Name: {user_name}
Background: {background}
Assessments Completed: {completed_count}/12

COMPLETE ASSESSMENT DATA:
{complete_assessment_data}

Create a detailed, personalized action plan that reflects their unique combination of traits, not generic career advice:

{{
    "success": true,
    "message": "🎯 {user_name}, congratulations on completing your comprehensive career assessment! Based on your unique profile, I've created a personalized roadmap that's specifically designed for someone with your exact combination of strengths, interests, and aspirations...",
    "career_summary": {{
        "primary_direction": "Specific career recommendation based on their exact assessment results",
        "key_strengths": ["Top 4-5 strengths identified from their responses"],
        "unique_value": "What makes them uniquely valuable in the marketplace based on their specific profile",
        "personality_type": "Their work style and collaboration preferences",
        "core_motivators": "What truly drives them based on their values assessment"
    }},
    "immediate_actions": [
        {{"action": "Specific first step based on their career direction", "timeline": "Next 30 days", "why": "Why this matters for their unique profile"}},
        {{"action": "Skill development action matching their learning style", "timeline": "Next 60 days", "why": "How this leverages their strengths"}},
        {{"action": "Network building strategy fitting their personality", "timeline": "Next 90 days", "why": "Tailored to their communication style"}}
    ],
    "skill_development": [
        {{"skill": "Primary skill to develop based on their aspirations", "approach": "Learning method matching their preferences", "timeline": "3-6 months"}},
        {{"skill": "Secondary skill complementing their strengths", "approach": "Development path fitting their schedule", "timeline": "6-12 months"}}
    ],
    "career_paths": [
        {{"path": "Primary career option matching their complete profile", "fit_score": "95%", "why": "Exact reasoning based on their assessments"}},
        {{"path": "Secondary career option leveraging different strengths", "fit_score": "88%", "why": "Alternative path reasoning"}},
        {{"path": "Growth/stretch career option", "fit_score": "82%", "why": "Future potential reasoning"}}
    ],
    "industry_recommendations": [
        "Specific industries matching their interests and values",
        "Sectors that need their unique skill combination",
        "Emerging fields aligned with their future aspirations"
    ],
    "work_environment_match": {{
        "ideal_culture": "Culture type based on their personality and values",
        "team_dynamics": "How they work best with others",
        "management_style": "Leadership approach they respond to best",
        "physical_workspace": "Environment that maximizes their productivity"
    }},
    "personalized_strategies": [
        "Job search approach tailored to their personality",
        "Interview preparation focusing on their strengths",
        "Networking strategy matching their communication style",
        "Personal branding that highlights their unique value"
    ],
    "next_steps": [
        "Immediate action for this week",
        "Key milestone for next month", 
        "Strategic goal for next quarter",
        "Long-term vision for next year"
    ],
    "success_metrics": [
        "How they'll know they're on the right path",
        "Key indicators of career satisfaction for their profile",
        "Milestones that matter most to their values"
    ]
}}
'''
    
    return enhanced_insights_prompt, enhanced_action_plan_prompt

def create_action_plan_display():
    """Create enhanced action plan display function"""
    
    action_plan_display = '''
def display_action_plan(action_plan: Dict[str, Any]):
    """Display comprehensive action plan with better formatting"""
    if not action_plan.get('success'):
        st.error("❌ Unable to generate action plan. Please try again.")
        return
    
    # Welcome message
    st.markdown("## 🎯 Your Personalized Career Action Plan")
    st.success(action_plan.get('message', 'Your personalized career roadmap is ready!'))
    
    # Career Summary
    career_summary = action_plan.get('career_summary', {})
    if career_summary:
        st.markdown("### 🌟 Your Career Profile Summary")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎯 Primary Direction:**")
            st.info(career_summary.get('primary_direction', 'Not specified'))
            
            st.markdown("**💪 Key Strengths:**")
            for strength in career_summary.get('key_strengths', []):
                st.write(f"• {strength}")
        
        with col2:
            st.markdown("**✨ Unique Value:**")
            st.info(career_summary.get('unique_value', 'Not specified'))
            
            if career_summary.get('core_motivators'):
                st.markdown("**⭐ Core Motivators:**")
                st.write(career_summary['core_motivators'])
    
    # Immediate Actions
    immediate_actions = action_plan.get('immediate_actions', [])
    if immediate_actions:
        st.markdown("### 🚀 Immediate Action Steps")
        for i, action in enumerate(immediate_actions, 1):
            with st.expander(f"Action {i}: {action.get('action', 'Action step')}"):
                st.markdown(f"**Timeline:** {action.get('timeline', 'Not specified')}")
                st.markdown(f"**Why this matters:** {action.get('why', 'Important for your development')}")
    
    # Career Paths
    career_paths = action_plan.get('career_paths', [])
    if career_paths:
        st.markdown("### 🛤️ Recommended Career Paths")
        for path in career_paths:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{path.get('path', 'Career Path')}**")
                st.write(path.get('why', 'Great fit for your profile'))
            with col2:
                fit_score = path.get('fit_score', '0%')
                st.metric("Fit Score", fit_score)
    
    # Skill Development
    skill_development = action_plan.get('skill_development', [])
    if skill_development:
        st.markdown("### 📈 Skill Development Plan")
        for skill in skill_development:
            st.markdown(f"**🎯 {skill.get('skill', 'Skill to develop')}**")
            st.write(f"Approach: {skill.get('approach', 'Standard learning approach')}")
            st.write(f"Timeline: {skill.get('timeline', 'Flexible timeline')}")
    
    # Industry Recommendations
    industry_recs = action_plan.get('industry_recommendations', [])
    if industry_recs:
        st.markdown("### 🏢 Industry Recommendations")
        for industry in industry_recs:
            st.write(f"• {industry}")
    
    # Work Environment Match
    work_env = action_plan.get('work_environment_match', {})
    if work_env:
        st.markdown("### 🌍 Your Ideal Work Environment")
        col1, col2 = st.columns(2)
        with col1:
            if work_env.get('ideal_culture'):
                st.markdown("**🏢 Ideal Culture:**")
                st.write(work_env['ideal_culture'])
            if work_env.get('team_dynamics'):
                st.markdown("**👥 Team Dynamics:**")
                st.write(work_env['team_dynamics'])
        with col2:
            if work_env.get('management_style'):
                st.markdown("**👔 Management Style:**")
                st.write(work_env['management_style'])
            if work_env.get('physical_workspace'):
                st.markdown("**🏠 Physical Workspace:**")
                st.write(work_env['physical_workspace'])
    
    # Personalized Strategies
    strategies = action_plan.get('personalized_strategies', [])
    if strategies:
        st.markdown("### 🎯 Personalized Success Strategies")
        for strategy in strategies:
            st.write(f"• {strategy}")
    
    # Next Steps
    next_steps = action_plan.get('next_steps', [])
    if next_steps:
        st.markdown("### 📋 Your Next Steps")
        for i, step in enumerate(next_steps, 1):
            st.write(f"{i}. {step}")
    
    # Success Metrics
    metrics = action_plan.get('success_metrics', [])
    if metrics:
        st.markdown("### 📊 Success Metrics")
        st.info("Track these indicators to measure your career progress:")
        for metric in metrics:
            st.write(f"• {metric}")
    
    # Download option
    if st.button("📥 Download Action Plan as PDF"):
        st.info("PDF download feature coming soon!")
'''
    
    with open("ENHANCED_ACTION_PLAN_DISPLAY.py", "w", encoding="utf-8") as f:
        f.write(action_plan_display)

def main():
    """Run the comprehensive fix"""
    print("🚀 Comprehensive Fix for Insights & Action Plan Issues")
    print("=" * 70)
    
    print("\n🔍 ISSUES IDENTIFIED:")
    print("1. ❌ 4 agents missing after 8+ completed assessments")
    print("2. ❌ Insights generation not working properly") 
    print("3. ❌ Action plan generation not personalized enough")
    print("4. ❌ Action plan display needs enhancement")
    
    print("\n🔧 CREATING FIXES:")
    
    # Create enhanced prompts
    insights_prompt, action_plan_prompt = create_enhanced_prompts()
    
    with open("ENHANCED_INSIGHTS_PROMPT.txt", "w", encoding="utf-8") as f:
        f.write(insights_prompt)
    
    with open("ENHANCED_ACTION_PLAN_PROMPT.txt", "w", encoding="utf-8") as f:
        f.write(action_plan_prompt)
    
    # Create enhanced display
    create_action_plan_display()
    
    print("✅ Created ENHANCED_INSIGHTS_PROMPT.txt")
    print("✅ Created ENHANCED_ACTION_PLAN_PROMPT.txt") 
    print("✅ Created ENHANCED_ACTION_PLAN_DISPLAY.py")
    
    print("\n🎯 MANUAL FIXES NEEDED:")
    print("1. Replace insights prompt in app.py with enhanced version")
    print("2. Replace action plan prompt in app.py with enhanced version")
    print("3. Add action_plan handling to selected_agent logic")
    print("4. Update display_action_plan function")
    print("5. Fix the missing 4 agents issue (check debug mode)")
    
    print("\n💡 PRIORITY: Check debug mode checkbox to see if all 6 options appear!")
    
if __name__ == "__main__":
    main()
