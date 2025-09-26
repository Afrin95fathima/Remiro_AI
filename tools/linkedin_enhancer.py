"""
LinkedIn Profile Enhancer for Remiro AI
======================================

Provides comprehensive LinkedIn profile optimization, content strategy,
and professional networking guidance with AI-powered recommendations.
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import streamlit as st

class LinkedInEnhancer:
    """LinkedIn profile optimization and networking strategy tool"""
    
    def __init__(self, llm):
        self.llm = llm
        
        # LinkedIn profile sections and best practices
        self.profile_sections = {
            "headline": {
                "max_length": 220,
                "best_practices": [
                    "Include target keywords",
                    "Show value proposition",
                    "Be specific about role/industry",
                    "Use action words",
                    "Avoid buzzwords like 'guru' or 'ninja'"
                ]
            },
            "summary": {
                "max_length": 2600,
                "best_practices": [
                    "Write in first person",
                    "Tell your story",
                    "Include achievements with numbers",
                    "Add call-to-action",
                    "Use keywords naturally"
                ]
            },
            "experience": {
                "best_practices": [
                    "Use action verbs",
                    "Quantify achievements",
                    "Include relevant keywords",
                    "Focus on impact, not duties",
                    "Use bullet points"
                ]
            }
        }
        
        # Content strategy templates
        self.content_templates = {
            "industry_insights": [
                "5 trends shaping {industry} in 2024",
                "What I learned from {recent_experience}",
                "The biggest challenge in {field} right now",
                "Why {skill} is crucial for {role_type}",
                "My take on {industry_news}"
            ],
            "career_updates": [
                "Excited to share my latest project on {topic}",
                "Reflecting on {time_period} in {role}",
                "Key takeaways from {event/course}",
                "Milestone achieved: {accomplishment}",
                "Looking forward to {future_goal}"
            ],
            "thought_leadership": [
                "The future of {industry}: my predictions",
                "Why {conventional_wisdom} might be wrong",
                "Lessons from {failure/success}",
                "How to approach {common_problem}",
                "The overlooked aspect of {trending_topic}"
            ]
        }
        
        # Networking strategies
        self.networking_strategies = {
            "cold_outreach": {
                "templates": [
                    "Hi {name}, I noticed your work on {specific_project}. I'm particularly interested in {shared_interest}. Would you be open to a brief chat about {topic}?",
                    "Hello {name}, I'm impressed by your journey from {previous_role} to {current_role}. As someone looking to make a similar transition, I'd love to hear your insights.",
                    "Hi {name}, I saw your post about {recent_post}. Your point about {specific_point} resonated with me. I'd love to connect and share some thoughts."
                ]
            },
            "engagement_strategy": [
                "Comment meaningfully on 5 posts daily",
                "Share industry news with your insights",
                "Congratulate connections on achievements",
                "Ask thoughtful questions in posts",
                "Share others' content with added perspective"
            ]
        }
    
    def display_linkedin_enhancer(self, user_profile: Dict[str, Any]):
        """Display the LinkedIn enhancement interface"""
        
        st.header("💼 LinkedIn Profile Enhancer")
        st.markdown("Optimize your LinkedIn presence for maximum professional impact")
        
        # Main tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📝 Profile Optimization",
            "📊 Content Strategy", 
            "🤝 Networking Plan",
            "🔍 Keyword Research",
            "📈 Analytics & Tracking"
        ])
        
        with tab1:
            self._display_profile_optimizer(user_profile)
        
        with tab2:
            self._display_content_strategy(user_profile)
        
        with tab3:
            self._display_networking_plan(user_profile)
        
        with tab4:
            self._display_keyword_research(user_profile)
        
        with tab5:
            self._display_analytics_tracking()
    
    def _display_profile_optimizer(self, user_profile: Dict[str, Any]):
        """Display LinkedIn profile optimization tools"""
        
        st.subheader("📝 Profile Optimization")
        st.markdown("Enhance each section of your LinkedIn profile for maximum impact")
        
        # Profile section selector
        section = st.selectbox(
            "Select Profile Section to Optimize:",
            ["Headline", "Summary/About", "Experience", "Skills", "Complete Profile Review"],
            help="Choose which part of your profile to focus on"
        )
        
        if section == "Headline":
            self._optimize_headline(user_profile)
        
        elif section == "Summary/About":
            self._optimize_summary(user_profile)
        
        elif section == "Experience":
            self._optimize_experience(user_profile)
        
        elif section == "Skills":
            self._optimize_skills(user_profile)
        
        elif section == "Complete Profile Review":
            self._complete_profile_review(user_profile)
    
    def _optimize_headline(self, user_profile: Dict[str, Any]):
        """Optimize LinkedIn headline"""
        
        st.markdown("### 🎯 Headline Optimization")
        st.markdown("Your headline is the first thing people see - make it count!")
        
        # Current headline input
        current_headline = st.text_area(
            "Current Headline:",
            placeholder="e.g., Software Developer at XYZ Company",
            help="Enter your current LinkedIn headline (or leave blank if you don't have one)",
            max_chars=220
        )
        
        # Target information
        col1, col2 = st.columns(2)
        
        with col1:
            target_role = st.text_input(
                "Target Role:",
                placeholder="e.g., Senior Software Engineer",
                help="What role are you targeting?"
            )
            
            industry = st.selectbox(
                "Industry:",
                ["Technology", "Finance", "Healthcare", "Marketing", "Consulting", "Other"]
            )
        
        with col2:
            key_skills = st.text_input(
                "Key Skills (comma-separated):",
                placeholder="Python, React, AWS, Machine Learning",
                help="Top 3-5 skills you want to highlight"
            )
            
            unique_value = st.text_input(
                "What makes you unique?",
                placeholder="e.g., Full-stack developer with AI expertise",
                help="Your unique value proposition"
            )
        
        if st.button("✨ Generate Optimized Headlines", type="primary"):
            with st.spinner("Generating headline suggestions..."):
                headlines = self._generate_headlines(
                    user_profile, current_headline, target_role, industry, key_skills, unique_value
                )
                
                self._display_headline_suggestions(headlines, current_headline)
    
    def _generate_headlines(self, user_profile: Dict[str, Any], current_headline: str,
                           target_role: str, industry: str, key_skills: str, unique_value: str) -> List[Dict[str, Any]]:
        """Generate optimized headline suggestions"""
        
        user_strengths = self._extract_user_strengths(user_profile)
        
        prompt = f"""Generate 5 optimized LinkedIn headlines for this professional profile:

CURRENT PROFILE:
- Current Headline: {current_headline}
- Target Role: {target_role}
- Industry: {industry}
- Key Skills: {key_skills}
- Unique Value: {unique_value}
- User Strengths: {', '.join(user_strengths[:5])}
- Assessment Summary: {self._get_assessment_summary(user_profile)}

HEADLINE REQUIREMENTS:
- Maximum 220 characters
- Include target keywords for the role
- Show clear value proposition
- Be specific and compelling
- Avoid overused buzzwords

Generate 5 different headline styles in JSON format:
{{
    "headlines": [
        {{
            "headline": "Senior Software Engineer | Python & React Expert | Building Scalable Web Applications at Tech Startups",
            "style": "Role + Skills + Value",
            "character_count": 95,
            "keywords": ["Senior Software Engineer", "Python", "React", "Scalable Web Applications"],
            "strengths": ["Clear role positioning", "Specific technical skills", "Value proposition"],
            "target_audience": "Hiring managers and recruiters in tech"
        }},
        {{
            "headline": "Full-Stack Developer → AI/ML Specialist | Transforming Ideas into Intelligent Applications | Open to Senior Roles",
            "style": "Career Progression + Specialty",
            "character_count": 115,
            "keywords": ["Full-Stack Developer", "AI/ML Specialist", "Senior Roles"],
            "strengths": ["Shows career growth", "Trending technology focus", "Call to action"],
            "target_audience": "Tech companies looking for AI talent"
        }}
    ]
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            result = json.loads(response.content)
            return result.get('headlines', [])
        
        except Exception:
            return self._generate_fallback_headlines(target_role, key_skills, unique_value)
    
    def _generate_fallback_headlines(self, target_role: str, key_skills: str, unique_value: str) -> List[Dict[str, Any]]:
        """Generate fallback headlines if AI fails"""
        skills_list = [skill.strip() for skill in key_skills.split(',') if skill.strip()][:3]
        
        return [
            {
                "headline": f"{target_role} | {' & '.join(skills_list[:2])} Specialist | {unique_value}",
                "style": "Role + Skills + Value",
                "character_count": len(f"{target_role} | {' & '.join(skills_list[:2])} Specialist | {unique_value}"),
                "keywords": [target_role] + skills_list[:2],
                "strengths": ["Clear positioning", "Skill focus"],
                "target_audience": "Industry professionals"
            },
            {
                "headline": f"{unique_value} | Experienced in {', '.join(skills_list[:3])} | Seeking {target_role} Opportunities",
                "style": "Value + Skills + Goal",
                "character_count": len(f"{unique_value} | Experienced in {', '.join(skills_list[:3])} | Seeking {target_role} Opportunities"),
                "keywords": skills_list + [target_role],
                "strengths": ["Value-first approach", "Clear job search signal"],
                "target_audience": "Recruiters and hiring managers"
            }
        ]
    
    def _display_headline_suggestions(self, headlines: List[Dict[str, Any]], current_headline: str):
        """Display headline suggestions with analysis"""
        
        st.subheader("💡 Headline Suggestions")
        
        if current_headline:
            st.markdown("### 📊 Current Headline Analysis")
            current_analysis = self._analyze_headline(current_headline)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Character Count", f"{len(current_headline)}/220")
            with col2:
                st.metric("Keyword Score", f"{current_analysis.get('keyword_score', 0)}/10")
            with col3:
                st.metric("Impact Score", f"{current_analysis.get('impact_score', 0)}/10")
            
            if current_analysis.get('issues'):
                st.markdown("**⚠️ Issues to Address:**")
                for issue in current_analysis['issues']:
                    st.markdown(f"• {issue}")
        
        st.markdown("### ✨ Optimized Headlines")
        
        for i, headline_data in enumerate(headlines, 1):
            headline = headline_data.get('headline', '')
            style = headline_data.get('style', 'Unknown')
            char_count = headline_data.get('character_count', len(headline))
            keywords = headline_data.get('keywords', [])
            strengths = headline_data.get('strengths', [])
            
            with st.expander(f"📝 Option {i}: {style}", expanded=(i == 1)):
                # The headline itself
                st.markdown(f"**Headline:**")
                st.markdown(f"`{headline}`")
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    color = "🟢" if char_count <= 220 else "🔴"
                    st.markdown(f"**Length:** {color} {char_count}/220")
                
                with col2:
                    st.markdown(f"**Keywords:** {len(keywords)}")
                
                with col3:
                    st.markdown(f"**Style:** {style}")
                
                # Analysis
                if keywords:
                    st.markdown("**🔍 Keywords included:**")
                    for keyword in keywords:
                        st.markdown(f"• {keyword}")
                
                if strengths:
                    st.markdown("**💪 Strengths:**")
                    for strength in strengths:
                        st.markdown(f"• {strength}")
                
                # Copy button
                if st.button(f"📋 Copy Option {i}", key=f"copy_headline_{i}"):
                    st.code(headline, language="text")
                    st.success("Headline copied! You can paste it directly to LinkedIn.")
    
    def _optimize_summary(self, user_profile: Dict[str, Any]):
        """Optimize LinkedIn summary/about section"""
        
        st.markdown("### 📄 About Section Optimization")
        st.markdown("Your About section is your elevator pitch - tell your professional story compellingly!")
        
        current_summary = st.text_area(
            "Current About/Summary:",
            placeholder="Paste your current LinkedIn About section here...",
            help="Your current About section (or leave blank if you don't have one)",
            height=200,
            max_chars=2600
        )
        
        # Profile information
        col1, col2 = st.columns(2)
        
        with col1:
            career_stage = st.selectbox(
                "Career Stage:",
                ["Recent Graduate", "Early Career (1-3 years)", "Mid-Career (4-8 years)", 
                 "Senior (8+ years)", "Executive", "Career Changer"]
            )
            
            target_audience = st.multiselect(
                "Target Audience:",
                ["Recruiters", "Hiring Managers", "Industry Peers", "Potential Clients", 
                 "Investors", "Collaborators"]
            )
        
        with col2:
            key_achievements = st.text_area(
                "Key Achievements (one per line):",
                placeholder="• Increased sales by 25%\n• Led team of 8 developers\n• Published 3 research papers",
                help="List your top 3-5 achievements with numbers when possible"
            )
            
            call_to_action = st.text_input(
                "Desired Action:",
                placeholder="e.g., Connect for collaboration opportunities",
                help="What do you want people to do after reading your profile?"
            )
        
        if st.button("✨ Generate Optimized Summary", type="primary"):
            with st.spinner("Crafting your optimized About section..."):
                summary_options = self._generate_summary_options(
                    user_profile, current_summary, career_stage, target_audience,
                    key_achievements, call_to_action
                )
                
                self._display_summary_options(summary_options, current_summary)
    
    def _generate_summary_options(self, user_profile: Dict[str, Any], current_summary: str,
                                 career_stage: str, target_audience: List[str], 
                                 key_achievements: str, call_to_action: str) -> List[Dict[str, Any]]:
        """Generate optimized summary options"""
        
        achievements_list = [ach.strip().lstrip('•').strip() for ach in key_achievements.split('\n') if ach.strip()]
        user_strengths = self._extract_user_strengths(user_profile)
        
        prompt = f"""Generate 3 optimized LinkedIn About section options for this professional:

CURRENT PROFILE:
- Current Summary: {current_summary[:1000]}
- Career Stage: {career_stage}
- Target Audience: {', '.join(target_audience)}
- Key Achievements: {', '.join(achievements_list[:5])}
- Call to Action: {call_to_action}
- User Strengths: {', '.join(user_strengths[:5])}
- Assessment Insights: {self._get_assessment_summary(user_profile)}

SUMMARY REQUIREMENTS:
- Maximum 2,600 characters
- Write in first person
- Include story/journey
- Quantified achievements
- Target keywords naturally
- End with call-to-action
- Professional yet personable tone

Generate 3 different summary styles in JSON format:
{{
    "summaries": [
        {{
            "summary": "Full optimized about section text...",
            "style": "Storytelling Approach",
            "character_count": 1500,
            "structure": ["Hook", "Journey", "Achievements", "Values", "Call-to-action"],
            "strengths": ["Engaging narrative", "Clear value proposition"],
            "keywords": ["keyword1", "keyword2"],
            "target_fit": "Best for career changers and creative professionals"
        }}
    ]
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            result = json.loads(response.content)
            return result.get('summaries', [])
        
        except Exception:
            return self._generate_fallback_summaries(career_stage, achievements_list, call_to_action)
    
    def _generate_fallback_summaries(self, career_stage: str, achievements: List[str], cta: str) -> List[Dict[str, Any]]:
        """Generate fallback summaries"""
        
        base_summary = f"""I'm a {career_stage.lower()} professional passionate about driving results and continuous learning.

Throughout my career, I've focused on delivering value through:
{chr(10).join([f'• {ach}' for ach in achievements[:3]])}

I believe in the power of collaboration and innovation to solve complex challenges. My approach combines analytical thinking with creative problem-solving to achieve sustainable growth.

{cta if cta else 'Let\'s connect to explore opportunities for collaboration!'}"""
        
        return [{
            "summary": base_summary,
            "style": "Achievement-Focused",
            "character_count": len(base_summary),
            "structure": ["Introduction", "Achievements", "Philosophy", "Call-to-action"],
            "strengths": ["Clear structure", "Achievement focus"],
            "keywords": ["professional", "results", "collaboration"],
            "target_fit": "General professional audience"
        }]
    
    def _display_summary_options(self, summaries: List[Dict[str, Any]], current_summary: str):
        """Display summary options with analysis"""
        
        if current_summary:
            st.markdown("### 📊 Current Summary Analysis")
            current_analysis = self._analyze_summary(current_summary)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Length", f"{len(current_summary)}/2600")
            with col2:
                st.metric("Readability", f"{current_analysis.get('readability', 7)}/10")
            with col3:
                st.metric("Keyword Score", f"{current_analysis.get('keyword_score', 5)}/10")
            with col4:
                st.metric("Engagement", f"{current_analysis.get('engagement', 6)}/10")
        
        st.markdown("### ✨ Optimized About Sections")
        
        for i, summary_data in enumerate(summaries, 1):
            summary_text = summary_data.get('summary', '')
            style = summary_data.get('style', 'Unknown')
            char_count = summary_data.get('character_count', len(summary_text))
            structure = summary_data.get('structure', [])
            strengths = summary_data.get('strengths', [])
            target_fit = summary_data.get('target_fit', '')
            
            with st.expander(f"📝 Option {i}: {style}", expanded=(i == 1)):
                # The summary text
                st.markdown("**Optimized About Section:**")
                st.text_area(
                    "",
                    value=summary_text,
                    height=200,
                    key=f"summary_display_{i}",
                    help="This is your optimized About section"
                )
                
                # Metrics and analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    color = "🟢" if char_count <= 2600 else "🔴"
                    st.markdown(f"**Length:** {color} {char_count}/2600")
                    
                    if structure:
                        st.markdown("**📋 Structure:**")
                        for section in structure:
                            st.markdown(f"• {section}")
                
                with col2:
                    if strengths:
                        st.markdown("**💪 Key Strengths:**")
                        for strength in strengths:
                            st.markdown(f"• {strength}")
                    
                    if target_fit:
                        st.markdown(f"**🎯 Best for:** {target_fit}")
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📋 Copy Option {i}", key=f"copy_summary_{i}"):
                        st.code(summary_text, language="text")
                        st.success("Summary copied! Ready to paste to LinkedIn.")
                
                with col2:
                    if st.button(f"✏️ Customize Option {i}", key=f"customize_summary_{i}"):
                        st.info("Customization feature would allow editing specific sections")
    
    def _display_content_strategy(self, user_profile: Dict[str, Any]):
        """Display LinkedIn content strategy tools"""
        
        st.subheader("📊 Content Strategy & Planning")
        st.markdown("Build your professional brand through strategic content sharing")
        
        # Content planning approach
        approach = st.selectbox(
            "Content Strategy Focus:",
            ["Thought Leadership", "Career Updates", "Industry Insights", "Personal Brand", "Job Search Content"],
            help="Choose your primary content strategy focus"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.selectbox(
                "Your Industry:",
                ["Technology", "Finance", "Healthcare", "Marketing", "Sales", "Consulting", "Other"]
            )
            
            post_frequency = st.selectbox(
                "Posting Frequency:",
                ["Daily", "3x per week", "Weekly", "Bi-weekly"]
            )
        
        with col2:
            expertise_areas = st.multiselect(
                "Areas of Expertise:",
                ["Leadership", "Data Analysis", "Product Management", "Software Development", 
                 "Digital Marketing", "Sales", "Strategy", "Innovation"],
                help="Select 2-4 areas you want to be known for"
            )
            
            content_types = st.multiselect(
                "Preferred Content Types:",
                ["Text Posts", "Articles", "Videos", "Polls", "Document Carousels", "Images with Quotes"],
                default=["Text Posts", "Articles"]
            )
        
        if st.button("📅 Generate Content Calendar", type="primary"):
            with st.spinner("Creating your personalized content strategy..."):
                content_strategy = self._generate_content_strategy(
                    user_profile, approach, industry, expertise_areas, 
                    post_frequency, content_types
                )
                
                self._display_content_strategy_results(content_strategy)
    
    def _generate_content_strategy(self, user_profile: Dict[str, Any], approach: str,
                                  industry: str, expertise_areas: List[str], 
                                  frequency: str, content_types: List[str]) -> Dict[str, Any]:
        """Generate comprehensive content strategy"""
        
        user_strengths = self._extract_user_strengths(user_profile)
        
        prompt = f"""Create a comprehensive LinkedIn content strategy for this professional:

PROFILE:
- Content Focus: {approach}
- Industry: {industry}
- Expertise Areas: {', '.join(expertise_areas)}
- Posting Frequency: {frequency}
- Content Types: {', '.join(content_types)}
- User Strengths: {', '.join(user_strengths[:5])}
- Assessment Insights: {self._get_assessment_summary(user_profile)}

Generate detailed content strategy in JSON format:
{{
    "content_pillars": [
        {{"pillar": "Industry Insights", "percentage": 40, "description": "Share trends and analysis"}},
        {{"pillar": "Personal Experience", "percentage": 30, "description": "Career lessons and stories"}},
        {{"pillar": "Thought Leadership", "percentage": 20, "description": "Opinions and predictions"}},
        {{"pillar": "Community Building", "percentage": 10, "description": "Engage with others' content"}}
    ],
    "content_ideas": [
        {{
            "title": "5 trends shaping {industry} in 2024",
            "type": "Text Post",
            "pillar": "Industry Insights",
            "outline": ["Trend 1", "Trend 2", "Impact", "Call to action"],
            "hook": "The {industry} landscape is changing rapidly...",
            "engagement_strategy": "Ask audience about their experiences"
        }}
    ],
    "posting_schedule": {{
        "Monday": "Industry news commentary",
        "Wednesday": "Personal insight or lesson learned",
        "Friday": "Weekend reflection or motivation"
    }},
    "engagement_tactics": [
        "Ask questions to spark discussion",
        "Share others' content with your perspective",
        "Comment on 10 posts daily in your network"
    ],
    "monthly_themes": [
        {{"month": "Month 1", "theme": "Industry Expertise", "focus": "Establish credibility"}},
        {{"month": "Month 2", "theme": "Personal Brand", "focus": "Share unique perspective"}},
        {{"month": "Month 3", "theme": "Thought Leadership", "focus": "Original insights"}}
    ],
    "metrics_to_track": [
        "Profile views growth",
        "Post engagement rate",
        "Connection requests",
        "Content reach and impressions"
    ]
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            result = json.loads(response.content)
            return result
            
        except Exception:
            return self._generate_fallback_content_strategy(approach, industry, expertise_areas)
    
    def _display_content_strategy_results(self, strategy: Dict[str, Any]):
        """Display the generated content strategy"""
        
        # Content pillars
        pillars = strategy.get('content_pillars', [])
        if pillars:
            st.subheader("🏛️ Your Content Pillars")
            
            for pillar in pillars:
                col1, col2, col3 = st.columns([2, 1, 3])
                with col1:
                    st.markdown(f"**{pillar.get('pillar', 'Unknown')}**")
                with col2:
                    st.markdown(f"{pillar.get('percentage', 0)}%")
                with col3:
                    st.markdown(pillar.get('description', 'No description'))
        
        # Content ideas
        content_ideas = strategy.get('content_ideas', [])
        if content_ideas:
            st.subheader("💡 Content Ideas")
            
            for i, idea in enumerate(content_ideas[:6], 1):
                with st.expander(f"💭 Content Idea {i}: {idea.get('title', 'Untitled')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Type:** {idea.get('type', 'Unknown')}")
                        st.markdown(f"**Pillar:** {idea.get('pillar', 'Unknown')}")
                        
                        outline = idea.get('outline', [])
                        if outline:
                            st.markdown("**Outline:**")
                            for point in outline:
                                st.markdown(f"• {point}")
                    
                    with col2:
                        hook = idea.get('hook', '')
                        if hook:
                            st.markdown("**Hook:**")
                            st.markdown(f"*{hook}*")
                        
                        engagement = idea.get('engagement_strategy', '')
                        if engagement:
                            st.markdown("**Engagement Strategy:**")
                            st.markdown(engagement)
        
        # Posting schedule
        schedule = strategy.get('posting_schedule', {})
        if schedule:
            st.subheader("📅 Weekly Posting Schedule")
            
            for day, content_type in schedule.items():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"**{day}:**")
                with col2:
                    st.markdown(content_type)
        
        # Monthly themes
        themes = strategy.get('monthly_themes', [])
        if themes:
            st.subheader("🎨 Quarterly Content Themes")
            
            for theme in themes:
                col1, col2, col3 = st.columns([1, 2, 2])
                with col1:
                    st.markdown(f"**{theme.get('month', 'Month')}**")
                with col2:
                    st.markdown(theme.get('theme', 'Theme'))
                with col3:
                    st.markdown(theme.get('focus', 'Focus'))
        
        # Engagement tactics and metrics
        col1, col2 = st.columns(2)
        
        with col1:
            tactics = strategy.get('engagement_tactics', [])
            if tactics:
                st.subheader("🤝 Engagement Tactics")
                for tactic in tactics:
                    st.markdown(f"• {tactic}")
        
        with col2:
            metrics = strategy.get('metrics_to_track', [])
            if metrics:
                st.subheader("📊 Success Metrics")
                for metric in metrics:
                    st.markdown(f"• {metric}")
    
    def _display_networking_plan(self, user_profile: Dict[str, Any]):
        """Display networking strategy and outreach tools"""
        
        st.subheader("🤝 Strategic Networking Plan")
        st.markdown("Build meaningful professional relationships with targeted outreach")
        
        # Networking goals
        networking_goal = st.selectbox(
            "Primary Networking Goal:",
            ["Job Search", "Business Development", "Knowledge Sharing", "Industry Influence", 
             "Mentorship", "Partnership Opportunities"],
            help="What's your main reason for networking?"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_roles = st.multiselect(
                "Target Roles to Connect With:",
                ["Hiring Managers", "Recruiters", "Industry Leaders", "Peers", 
                 "Potential Clients", "Mentors", "Team Members"],
                help="Who do you want to connect with?"
            )
            
            industry_focus = st.selectbox(
                "Industry Focus:",
                ["Same Industry", "Adjacent Industries", "Completely New Industry", "Multiple Industries"]
            )
        
        with col2:
            company_types = st.multiselect(
                "Target Company Types:",
                ["Startups", "Scale-ups", "Fortune 500", "Mid-size Companies", 
                 "Consulting Firms", "Government", "Non-profit"],
                help="What types of organizations?"
            )
            
            geographic_focus = st.selectbox(
                "Geographic Focus:",
                ["Local/Regional", "National", "Global", "Remote-first companies"]
            )
        
        if st.button("🎯 Generate Networking Strategy", type="primary"):
            with st.spinner("Creating your networking action plan..."):
                networking_plan = self._generate_networking_plan(
                    user_profile, networking_goal, target_roles, industry_focus,
                    company_types, geographic_focus
                )
                
                self._display_networking_results(networking_plan)
    
    def _generate_networking_plan(self, user_profile: Dict[str, Any], goal: str,
                                 target_roles: List[str], industry_focus: str,
                                 company_types: List[str], geographic_focus: str) -> Dict[str, Any]:
        """Generate comprehensive networking strategy"""
        
        user_strengths = self._extract_user_strengths(user_profile)
        
        prompt = f"""Create a comprehensive LinkedIn networking strategy:

NETWORKING PROFILE:
- Primary Goal: {goal}
- Target Roles: {', '.join(target_roles)}
- Industry Focus: {industry_focus}
- Company Types: {', '.join(company_types)}
- Geographic Focus: {geographic_focus}
- User Strengths: {', '.join(user_strengths[:5])}
- Assessment Insights: {self._get_assessment_summary(user_profile)}

Generate networking strategy in JSON format:
{{
    "outreach_strategy": {{
        "weekly_targets": {{
            "new_connections": 15,
            "follow_ups": 10,
            "meaningful_conversations": 5
        }},
        "connection_approach": [
            "Research target's background and recent activity",
            "Find common connections or experiences",
            "Craft personalized message mentioning specific details",
            "Suggest mutual value exchange"
        ]
    }},
    "message_templates": [
        {{
            "scenario": "Cold outreach to hiring manager",
            "template": "Hi {{name}}, I noticed your team is growing at {{company}}. I'm particularly drawn to {{specific_company_initiative}}. With my background in {{relevant_experience}}, I'd love to learn more about {{specific_role}}. Would you be open to a brief conversation?",
            "personalization_tips": ["Research recent company news", "Mention specific role or project", "Show genuine interest"],
            "success_rate": "15-25%"
        }}
    ]],
    "networking_activities": [
        {{
            "activity": "Industry events and webinars",
            "frequency": "2-3 per month",
            "approach": "Attend, engage in chat, follow up with speakers and attendees",
            "roi": "High - targeted audience"
        }}
    ],
    "relationship_nurturing": [
        "Share relevant articles with personal notes",
        "Congratulate on achievements and company news",
        "Make valuable introductions between connections",
        "Offer help or expertise when appropriate"
    ],
    "tracking_system": {{
        "metrics": ["Response rate", "Meeting conversion", "Referral generation"],
        "tools": ["LinkedIn Sales Navigator", "CRM system", "Spreadsheet tracking"],
        "review_frequency": "Weekly review and adjustment"
    }}
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            result = json.loads(response.content)
            return result
            
        except Exception:
            return self._generate_fallback_networking_plan(goal, target_roles)
    
    # Helper methods
    def _extract_user_strengths(self, user_profile: Dict[str, Any]) -> List[str]:
        """Extract user strengths from assessment data"""
        strengths = []
        assessments = user_profile.get('assessments', {})
        
        for assessment_data in assessments.values():
            if assessment_data.get('completed') and assessment_data.get('data'):
                data = assessment_data['data']
                if 'strengths' in data:
                    strengths.extend(data['strengths'][:2])
        
        if not strengths:
            strengths = ["Professional experience", "Learning agility", "Problem solving"]
        
        return list(set(strengths))
    
    def _get_assessment_summary(self, user_profile: Dict[str, Any]) -> str:
        """Get summary of completed assessments"""
        assessments = user_profile.get('assessments', {})
        completed = [name for name, data in assessments.items() if data.get('completed')]
        
        if completed:
            return f"Completed assessments: {', '.join(completed[:5])}"
        return "Assessment data available for personalization"
    
    def _analyze_headline(self, headline: str) -> Dict[str, Any]:
        """Analyze current headline for issues and scoring"""
        issues = []
        keyword_score = 5
        impact_score = 5
        
        if len(headline) < 50:
            issues.append("Headline is too short - consider adding more specific details")
        if len(headline) > 220:
            issues.append("Headline exceeds 220 character limit")
        if not any(word in headline.lower() for word in ['expert', 'specialist', 'manager', 'engineer', 'analyst']):
            issues.append("Consider including your professional title or expertise area")
        if headline.count('|') > 3:
            issues.append("Too many separators - simplify structure")
        
        return {
            'keyword_score': keyword_score,
            'impact_score': impact_score,
            'issues': issues
        }
    
    def _analyze_summary(self, summary: str) -> Dict[str, Any]:
        """Analyze current summary for scoring"""
        return {
            'readability': min(10, max(1, 10 - len(summary.split()) // 50)),
            'keyword_score': 6,  # Would be more sophisticated
            'engagement': 7
        }
    
    def _generate_fallback_content_strategy(self, approach: str, industry: str, expertise_areas: List[str]) -> Dict[str, Any]:
        """Generate fallback content strategy"""
        return {
            "content_pillars": [
                {"pillar": "Industry Insights", "percentage": 40, "description": f"Share {industry} trends and news"},
                {"pillar": "Professional Experience", "percentage": 35, "description": "Personal lessons and stories"},
                {"pillar": "Thought Leadership", "percentage": 25, "description": "Opinions and predictions"}
            ],
            "content_ideas": [
                {
                    "title": f"Key trends in {industry} for 2024",
                    "type": "Text Post",
                    "pillar": "Industry Insights",
                    "outline": ["Current state", "Emerging trends", "Implications", "Predictions"],
                    "hook": f"The {industry} landscape is evolving rapidly...",
                    "engagement_strategy": "Ask audience about their observations"
                }
            ],
            "posting_schedule": {
                "Monday": "Industry commentary",
                "Wednesday": "Personal insight",
                "Friday": "Weekend motivation"
            },
            "engagement_tactics": [
                "Ask thought-provoking questions",
                "Share and comment on others' posts",
                "Engage with industry hashtags"
            ]
        }
    
    def _generate_fallback_networking_plan(self, goal: str, target_roles: List[str]) -> Dict[str, Any]:
        """Generate fallback networking plan"""
        return {
            "outreach_strategy": {
                "weekly_targets": {
                    "new_connections": 10,
                    "follow_ups": 5,
                    "meaningful_conversations": 3
                }
            },
            "message_templates": [
                {
                    "scenario": "General networking",
                    "template": "Hi {name}, I came across your profile and was impressed by your experience in {field}. I'd love to connect and learn from your insights.",
                    "success_rate": "20-30%"
                }
            ],
            "networking_activities": [
                {
                    "activity": "Industry groups and forums",
                    "frequency": "Weekly participation",
                    "approach": "Share insights and engage with posts",
                    "roi": "Medium - broad reach"
                }
            ]
        }
    
    def _display_networking_results(self, networking_plan: Dict[str, Any]):
        """Display networking strategy results"""
        
        # Weekly targets
        targets = networking_plan.get('outreach_strategy', {}).get('weekly_targets', {})
        if targets:
            st.subheader("🎯 Weekly Networking Targets")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("New Connections", targets.get('new_connections', 0))
            with col2:
                st.metric("Follow-ups", targets.get('follow_ups', 0))
            with col3:
                st.metric("Conversations", targets.get('meaningful_conversations', 0))
        
        # Message templates
        templates = networking_plan.get('message_templates', [])
        if templates:
            st.subheader("📝 Outreach Message Templates")
            
            for i, template in enumerate(templates, 1):
                scenario = template.get('scenario', f'Template {i}')
                message = template.get('template', '')
                success_rate = template.get('success_rate', 'Unknown')
                
                with st.expander(f"📧 {scenario} (Success Rate: {success_rate})"):
                    st.code(message, language="text")
                    
                    tips = template.get('personalization_tips', [])
                    if tips:
                        st.markdown("**💡 Personalization Tips:**")
                        for tip in tips:
                            st.markdown(f"• {tip}")
        
        # Networking activities
        activities = networking_plan.get('networking_activities', [])
        if activities:
            st.subheader("🎪 Recommended Networking Activities")
            
            for activity in activities:
                name = activity.get('activity', 'Activity')
                frequency = activity.get('frequency', 'Regular')
                approach = activity.get('approach', 'Engage actively')
                roi = activity.get('roi', 'Medium')
                
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.markdown(f"**{name}**")
                with col2:
                    st.markdown(f"*{frequency}*")
                with col3:
                    st.markdown(f"ROI: {roi}")
                
                st.markdown(f"**Approach:** {approach}")
                st.markdown("---")
    
    def _display_keyword_research(self, user_profile: Dict[str, Any]):
        """Display LinkedIn keyword research tool"""
        
        st.subheader("🔍 LinkedIn Keyword Optimization")
        st.markdown("Research and optimize keywords for better profile visibility")
        
        # This would be a comprehensive keyword research tool
        st.info("🚧 Keyword Research Tool - Coming Soon! This will help you identify the most effective keywords for your industry and role.")
    
    def _display_analytics_tracking(self):
        """Display analytics and tracking dashboard"""
        
        st.subheader("📈 LinkedIn Analytics & Performance")
        st.markdown("Track your LinkedIn performance and networking ROI")
        
        # This would show analytics dashboard
        st.info("📊 Analytics Dashboard - Coming Soon! Track your profile views, connection growth, and content performance.")
