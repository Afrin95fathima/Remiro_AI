
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
