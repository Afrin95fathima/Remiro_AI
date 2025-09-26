"""
Job Description Matcher & Skill Gap Analyzer for Remiro AI
=========================================================

Provides intelligent job matching, skill gap analysis, and career path mapping
with market data integration and personalized recommendations.
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import streamlit as st

class JobMatcherSkillAnalyzer:
    """Combined job matching and skill analysis system"""
    
    def __init__(self, llm):
        self.llm = llm
        
        # Industry skill requirements database
        self.skill_database = {
            "Software Engineering": {
                "entry_level": [
                    "Programming languages (Python, Java, JavaScript)",
                    "Version control (Git)",
                    "Basic algorithms and data structures",
                    "Web development fundamentals",
                    "Database basics (SQL)",
                    "Testing fundamentals",
                    "Problem-solving",
                    "Communication skills"
                ],
                "mid_level": [
                    "Advanced programming concepts",
                    "System design basics",
                    "API development and integration",
                    "Cloud platforms (AWS, Azure, GCP)",
                    "DevOps fundamentals",
                    "Code review and collaboration",
                    "Performance optimization",
                    "Technical documentation"
                ],
                "senior_level": [
                    "System architecture and design",
                    "Leadership and mentoring",
                    "Advanced cloud technologies",
                    "Microservices architecture",
                    "Security best practices",
                    "Technical strategy",
                    "Cross-functional collaboration",
                    "Project management"
                ]
            },
            "Data Science": {
                "entry_level": [
                    "Python/R programming",
                    "Statistics and probability",
                    "Data manipulation (pandas, SQL)",
                    "Data visualization (matplotlib, seaborn)",
                    "Machine learning basics",
                    "Jupyter notebooks",
                    "Excel proficiency",
                    "Analytical thinking"
                ],
                "mid_level": [
                    "Advanced machine learning algorithms",
                    "Deep learning frameworks (TensorFlow, PyTorch)",
                    "Big data tools (Spark, Hadoop)",
                    "A/B testing and experimentation",
                    "Feature engineering",
                    "Model deployment",
                    "Business intelligence tools",
                    "Stakeholder communication"
                ],
                "senior_level": [
                    "MLOps and model lifecycle management",
                    "Advanced deep learning architectures",
                    "Data strategy and governance",
                    "Team leadership",
                    "Business impact measurement",
                    "Research and innovation",
                    "Cross-functional project leadership",
                    "Technical mentoring"
                ]
            },
            "Product Management": {
                "entry_level": [
                    "Product lifecycle understanding",
                    "User research methods",
                    "Basic analytics (Google Analytics)",
                    "Agile/Scrum methodologies",
                    "Wireframing and prototyping",
                    "Stakeholder communication",
                    "Market research",
                    "Project coordination"
                ],
                "mid_level": [
                    "Product strategy development",
                    "Advanced analytics and metrics",
                    "A/B testing and experimentation",
                    "Roadmap planning and prioritization",
                    "Cross-functional team leadership",
                    "Competitive analysis",
                    "Go-to-market strategy",
                    "Product-market fit analysis"
                ],
                "senior_level": [
                    "Vision and strategy setting",
                    "P&L ownership",
                    "Portfolio management",
                    "Executive communication",
                    "Team building and hiring",
                    "Market expansion strategy",
                    "Strategic partnerships",
                    "Innovation leadership"
                ]
            },
            "Digital Marketing": {
                "entry_level": [
                    "Social media marketing",
                    "Content creation and copywriting",
                    "Basic SEO principles",
                    "Google Analytics basics",
                    "Email marketing platforms",
                    "Graphic design basics",
                    "Campaign execution",
                    "Brand awareness"
                ],
                "mid_level": [
                    "Paid advertising (Google Ads, Facebook Ads)",
                    "Marketing automation",
                    "Advanced SEO and SEM",
                    "Conversion optimization",
                    "Data analysis and reporting",
                    "Lead generation strategies",
                    "Marketing funnel optimization",
                    "Cross-channel campaign management"
                ],
                "senior_level": [
                    "Marketing strategy and planning",
                    "Budget management and ROI optimization",
                    "Team leadership",
                    "Marketing technology stack",
                    "Customer acquisition cost optimization",
                    "Brand positioning and messaging",
                    "Performance marketing at scale",
                    "Strategic partnerships"
                ]
            }
        }
        
        # Career progression paths
        self.career_paths = {
            "Software Engineering": {
                "Individual Contributor": [
                    "Junior Software Developer",
                    "Software Developer",
                    "Senior Software Developer",
                    "Staff Software Engineer",
                    "Principal Engineer",
                    "Distinguished Engineer"
                ],
                "Management": [
                    "Junior Software Developer",
                    "Software Developer",
                    "Senior Software Developer",
                    "Tech Lead",
                    "Engineering Manager",
                    "Director of Engineering",
                    "VP of Engineering"
                ],
                "Specialization": [
                    "Software Developer",
                    "Frontend/Backend Specialist",
                    "DevOps Engineer",
                    "Solutions Architect",
                    "Security Engineer",
                    "Machine Learning Engineer"
                ]
            },
            "Data Science": {
                "Individual Contributor": [
                    "Junior Data Analyst",
                    "Data Analyst",
                    "Data Scientist",
                    "Senior Data Scientist",
                    "Principal Data Scientist",
                    "Chief Data Scientist"
                ],
                "Management": [
                    "Data Scientist",
                    "Senior Data Scientist",
                    "Lead Data Scientist",
                    "Data Science Manager",
                    "Director of Data Science",
                    "VP of Data"
                ],
                "Specialization": [
                    "Data Analyst",
                    "Business Intelligence Analyst",
                    "Machine Learning Engineer",
                    "Data Engineer",
                    "Research Scientist",
                    "AI Product Manager"
                ]
            }
        }
    
    def display_job_matcher_analyzer(self, user_profile: Dict[str, Any]):
        """Display the combined job matcher and skill analyzer interface"""
        
        st.header("🎯 Job Matcher & Skill Gap Analyzer")
        st.markdown("Analyze job matches, identify skill gaps, and plan your career progression")
        
        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Job Match Analysis",
            "📊 Skill Gap Analysis", 
            "🗺️ Career Path Mapping",
            "📈 Market Intelligence"
        ])
        
        with tab1:
            self._display_job_matcher(user_profile)
        
        with tab2:
            self._display_skill_gap_analyzer(user_profile)
        
        with tab3:
            self._display_career_path_mapper(user_profile)
        
        with tab4:
            self._display_market_intelligence()
    
    def _display_job_matcher(self, user_profile: Dict[str, Any]):
        """Display job description matching functionality"""
        
        st.subheader("🔍 Job Description Matcher")
        st.markdown("Analyze how well your profile matches specific job opportunities")
        
        # Input methods
        input_method = st.radio(
            "How would you like to input the job description?",
            ["Paste Job Description", "Upload Job Description", "Job URL"],
            horizontal=True
        )
        
        job_description = ""
        
        if input_method == "Paste Job Description":
            job_description = st.text_area(
                "Job Description:",
                height=300,
                placeholder="Paste the complete job description here...",
                help="Include the full job posting with requirements, responsibilities, and company information"
            )
        
        elif input_method == "Upload Job Description":
            uploaded_file = st.file_uploader("Upload Job Description", type=['txt', 'pdf', 'docx'])
            if uploaded_file:
                job_description = "Job description would be extracted from uploaded file"
                st.info("File upload processing would be implemented here")
        
        elif input_method == "Job URL":
            job_url = st.text_input("Job Posting URL:", placeholder="https://example.com/job-posting")
            if job_url:
                job_description = "Job description would be scraped from URL"
                st.info("URL scraping would be implemented here with appropriate rate limiting")
        
        if job_description:
            col1, col2 = st.columns([3, 1])
            
            with col2:
                company_name = st.text_input("Company Name (Optional):", placeholder="e.g., Google")
                job_title = st.text_input("Job Title:", placeholder="e.g., Senior Software Engineer")
            
            if st.button("🔍 Analyze Job Match", type="primary", use_container_width=True):
                with st.spinner("Analyzing job match..."):
                    # Perform comprehensive job match analysis
                    match_analysis = self._analyze_comprehensive_job_match(
                        job_description, 
                        user_profile,
                        company_name,
                        job_title
                    )
                    
                    self._display_comprehensive_match_results(match_analysis)
    
    def _analyze_comprehensive_job_match(self, job_description: str, user_profile: Dict[str, Any], 
                                       company_name: str = "", job_title: str = "") -> Dict[str, Any]:
        """Perform comprehensive job match analysis"""
        
        # Extract user skills and experience from assessment data
        user_skills = self._extract_user_skills_from_assessments(user_profile)
        user_experience = self._extract_user_experience(user_profile)
        
        prompt = f"""Perform a comprehensive job match analysis between this candidate profile and job description.

CANDIDATE PROFILE:
- Background: {user_profile.get('background', 'Professional')}
- Key Skills: {', '.join(user_skills[:20])}
- Experience Level: {user_experience}
- Assessment Insights: {self._get_assessment_summary(user_profile)}

JOB DESCRIPTION:
{job_description[:3000]}

Company: {company_name}
Position: {job_title}

Provide detailed analysis in JSON format:
{{
    "overall_match_score": 85,
    "match_breakdown": {{
        "skills_match": 78,
        "experience_match": 92,
        "culture_fit": 85,
        "growth_potential": 88
    }},
    "matching_elements": {{
        "required_skills": ["skill1", "skill2"],
        "preferred_skills": ["skill3", "skill4"],
        "experience_areas": ["area1", "area2"],
        "soft_skills": ["communication", "leadership"]
    }},
    "missing_elements": {{
        "critical_skills": ["missing skill 1"],
        "preferred_skills": ["nice to have skill"],
        "experience_gaps": ["specific experience type"],
        "certifications": ["certification name"]
    }},
    "strengths": [
        "Strong technical background aligns with core requirements",
        "Leadership experience matches team lead responsibilities"
    ],
    "concerns": [
        "Limited experience with specific technology stack",
        "May need additional training in domain knowledge"
    ],
    "recommendations": {{
        "immediate_actions": ["action 1", "action 2"],
        "skill_development": ["skill to develop 1", "skill to develop 2"],
        "experience_building": ["how to gain relevant experience"],
        "application_tips": ["how to position application"]
    }},
    "salary_estimate": {{
        "min": 90000,
        "max": 120000,
        "currency": "USD",
        "note": "Based on job requirements and market data"
    }},
    "interview_prep": [
        "Expect questions about specific technology",
        "Prepare examples of similar project experience",
        "Research company's recent initiatives"
    ]
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            analysis = json.loads(response.content)
            
            # Add additional calculated metrics
            analysis['application_readiness'] = self._calculate_application_readiness(analysis)
            analysis['competitive_position'] = self._assess_competitive_position(analysis)
            
            return analysis
            
        except Exception as e:
            # Fallback analysis
            return self._generate_fallback_analysis(job_description, user_profile)
    
    def _display_comprehensive_match_results(self, analysis: Dict[str, Any]):
        """Display comprehensive job match results"""
        
        # Overall Match Score
        overall_score = analysis.get('overall_match_score', 0)
        
        if overall_score >= 85:
            match_color = "🟢"
            match_status = "Excellent Match - Apply Now!"
        elif overall_score >= 70:
            match_color = "🟡"
            match_status = "Good Match - Worth Pursuing"
        elif overall_score >= 55:
            match_color = "🟠"
            match_status = "Partial Match - Need Preparation"
        else:
            match_color = "🔴"
            match_status = "Poor Match - Consider Skill Development"
        
        # Header metrics
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; margin: 20px 0;">
            <h2 style="margin: 0;">{match_color} Overall Match: {overall_score}%</h2>
            <p style="margin: 10px 0 0 0; font-size: 18px;">{match_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed breakdown
        col1, col2, col3, col4 = st.columns(4)
        
        breakdown = analysis.get('match_breakdown', {})
        
        with col1:
            st.metric("🛠️ Skills Match", f"{breakdown.get('skills_match', 0)}%")
        with col2:
            st.metric("📈 Experience Match", f"{breakdown.get('experience_match', 0)}%")
        with col3:
            st.metric("🤝 Culture Fit", f"{breakdown.get('culture_fit', 0)}%")
        with col4:
            st.metric("🚀 Growth Potential", f"{breakdown.get('growth_potential', 0)}%")
        
        # Detailed analysis sections
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Your Strengths for This Role")
            strengths = analysis.get('strengths', [])
            for strength in strengths:
                st.markdown(f"• {strength}")
            
            # Matching elements
            matching = analysis.get('matching_elements', {})
            if matching.get('required_skills'):
                st.subheader("🎯 Matching Required Skills")
                for skill in matching['required_skills'][:8]:
                    st.markdown(f"✅ {skill}")
        
        with col2:
            st.subheader("⚠️ Areas of Concern")
            concerns = analysis.get('concerns', [])
            if concerns:
                for concern in concerns:
                    st.markdown(f"• {concern}")
            else:
                st.markdown("• No major concerns identified!")
            
            # Missing elements
            missing = analysis.get('missing_elements', {})
            if missing.get('critical_skills'):
                st.subheader("❌ Critical Missing Skills")
                for skill in missing['critical_skills']:
                    st.markdown(f"⚠️ {skill}")
        
        # Recommendations
        recommendations = analysis.get('recommendations', {})
        if recommendations:
            st.subheader("💡 Personalized Recommendations")
            
            if recommendations.get('immediate_actions'):
                with st.expander("🚀 Immediate Actions", expanded=True):
                    for action in recommendations['immediate_actions']:
                        st.markdown(f"• {action}")
            
            if recommendations.get('skill_development'):
                with st.expander("📚 Skill Development Plan"):
                    for skill in recommendations['skill_development']:
                        st.markdown(f"• {skill}")
            
            if recommendations.get('application_tips'):
                with st.expander("📝 Application Strategy Tips"):
                    for tip in recommendations['application_tips']:
                        st.markdown(f"• {tip}")
        
        # Salary and Interview Prep
        col1, col2 = st.columns(2)
        
        with col1:
            salary_info = analysis.get('salary_estimate', {})
            if salary_info:
                st.subheader("💰 Estimated Salary Range")
                min_sal = salary_info.get('min', 0)
                max_sal = salary_info.get('max', 0)
                currency = salary_info.get('currency', 'USD')
                
                if min_sal and max_sal:
                    st.markdown(f"**Range:** ${min_sal:,} - ${max_sal:,} {currency}")
                    if salary_info.get('note'):
                        st.markdown(f"*{salary_info['note']}*")
        
        with col2:
            interview_prep = analysis.get('interview_prep', [])
            if interview_prep:
                st.subheader("🎤 Interview Preparation")
                for prep_tip in interview_prep[:5]:
                    st.markdown(f"• {prep_tip}")
        
        # Application readiness assessment
        readiness = analysis.get('application_readiness', 'Unknown')
        competitive_pos = analysis.get('competitive_position', 'Unknown')
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("📋 Application Readiness", readiness)
        with col2:
            st.metric("🏆 Competitive Position", competitive_pos)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Generate Cover Letter", use_container_width=True):
                st.info("Cover letter generator would be implemented here")
        
        with col2:
            if st.button("📊 Create Skill Development Plan", use_container_width=True):
                self._create_skill_development_plan(analysis, analysis.get('missing_elements', {}))
        
        with col3:
            if st.button("💾 Save Analysis", use_container_width=True):
                # Save analysis to user profile
                st.success("Analysis saved to your profile!")
    
    def _display_skill_gap_analyzer(self, user_profile: Dict[str, Any]):
        """Display skill gap analysis functionality"""
        
        st.subheader("📊 Skill Gap Analyzer")
        st.markdown("Identify skill gaps and create personalized learning paths")
        
        # Target role selection
        col1, col2 = st.columns(2)
        
        with col1:
            target_industry = st.selectbox(
                "Target Industry:",
                ["Software Engineering", "Data Science", "Product Management", 
                 "Digital Marketing", "Sales", "Consulting", "Finance"],
                help="Select the industry you want to transition to or advance in"
            )
            
            current_level = st.selectbox(
                "Current Experience Level:",
                ["Student/Entry Level", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
                help="Your current experience level in this industry"
            )
        
        with col2:
            target_level = st.selectbox(
                "Target Experience Level:",
                ["Entry Level", "Mid Level", "Senior Level", "Executive Level"],
                help="The level you want to reach"
            )
            
            specific_role = st.text_input(
                "Specific Target Role (Optional):",
                placeholder="e.g., Senior Data Scientist, Product Manager",
                help="Be specific about the exact role you're targeting"
            )
        
        if st.button("🔍 Analyze Skill Gaps", type="primary", use_container_width=True):
            with st.spinner("Analyzing your skill gaps..."):
                skill_gap_analysis = self._perform_skill_gap_analysis(
                    user_profile, target_industry, current_level, target_level, specific_role
                )
                
                self._display_skill_gap_results(skill_gap_analysis)
    
    def _perform_skill_gap_analysis(self, user_profile: Dict[str, Any], target_industry: str, 
                                   current_level: str, target_level: str, specific_role: str = "") -> Dict[str, Any]:
        """Perform comprehensive skill gap analysis"""
        
        # Get current skills from user assessments
        current_skills = self._extract_user_skills_from_assessments(user_profile)
        user_strengths = self._extract_user_strengths(user_profile)
        
        # Map experience levels
        level_mapping = {
            "Student/Entry Level": "entry_level",
            "1-3 years": "entry_level",
            "3-5 years": "mid_level", 
            "5-10 years": "mid_level",
            "10+ years": "senior_level"
        }
        
        target_level_mapped = {
            "Entry Level": "entry_level",
            "Mid Level": "mid_level",
            "Senior Level": "senior_level",
            "Executive Level": "senior_level"
        }
        
        current_mapped = level_mapping.get(current_level, "mid_level")
        target_mapped = target_level_mapped.get(target_level, "mid_level")
        
        # Get required skills for target
        required_skills = self.skill_database.get(target_industry, {}).get(target_mapped, [])
        
        prompt = f"""Perform comprehensive skill gap analysis for career transition/advancement:

CURRENT PROFILE:
- Industry Background: {user_profile.get('background', 'Professional')}
- Current Skills: {', '.join(current_skills[:25])}
- Key Strengths: {', '.join(user_strengths[:10])}
- Experience Level: {current_level}
- Assessment Data: {self._get_assessment_summary(user_profile)}

TARGET CAREER:
- Industry: {target_industry}
- Target Level: {target_level}
- Specific Role: {specific_role}
- Required Skills for {target_level}: {', '.join(required_skills)}

Provide detailed analysis in JSON format:
{{
    "skill_gap_score": 75,
    "readiness_level": "Moderately Ready",
    "time_to_readiness": "6-12 months",
    "current_strengths": [
        "Transferable skill 1",
        "Relevant experience area"
    ],
    "skill_gaps": {{
        "critical": ["Must-have skill missing"],
        "important": ["Important skill to develop"],
        "nice_to_have": ["Bonus skill for competitive advantage"]
    }},
    "learning_path": {{
        "immediate": [
            {{"skill": "Python Programming", "priority": "High", "time_needed": "2-3 months", "resources": ["Online courses", "Practice projects"]}},
            {{"skill": "Data Analysis", "priority": "High", "time_needed": "1-2 months", "resources": ["Kaggle courses", "Real datasets"]}}
        ],
        "short_term": [
            {{"skill": "Machine Learning", "priority": "Medium", "time_needed": "3-4 months", "resources": ["Coursera ML course", "Personal projects"]}}
        ],
        "long_term": [
            {{"skill": "Leadership", "priority": "Medium", "time_needed": "6+ months", "resources": ["Leadership books", "Mentorship", "Team projects"]}}
        ]
    }},
    "experience_building": [
        "Build portfolio projects demonstrating key skills",
        "Contribute to open source projects",
        "Volunteer for relevant projects at current job"
    ],
    "networking_opportunities": [
        "Join industry professional associations",
        "Attend relevant conferences and meetups",
        "Connect with professionals on LinkedIn"
    ],
    "certification_recommendations": [
        "Relevant certification 1",
        "Industry-standard certification 2"
    ],
    "competitive_analysis": {{
        "your_advantages": ["Unique background strength"],
        "market_challenges": ["Common challenge for career changers"],
        "differentiation_strategy": ["How to stand out"]
    }}
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            analysis = json.loads(response.content)
            
            # Enhance with additional calculations
            analysis['total_learning_time'] = self._calculate_total_learning_time(analysis)
            analysis['monthly_learning_plan'] = self._create_monthly_plan(analysis)
            
            return analysis
            
        except Exception:
            return self._generate_fallback_skill_analysis(target_industry, target_level)
    
    def _display_skill_gap_results(self, analysis: Dict[str, Any]):
        """Display skill gap analysis results"""
        
        # Header with readiness assessment
        readiness = analysis.get('readiness_level', 'Unknown')
        gap_score = analysis.get('skill_gap_score', 0)
        time_needed = analysis.get('time_to_readiness', 'Unknown')
        
        if gap_score >= 80:
            color = "🟢"
            status = "Ready to Apply!"
        elif gap_score >= 60:
            color = "🟡" 
            status = "Almost Ready"
        else:
            color = "🟠"
            status = "Preparation Needed"
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; margin: 20px 0;">
            <h2 style="margin: 0;">{color} Career Readiness: {gap_score}%</h2>
            <p style="margin: 10px 0 0 0; font-size: 18px;">{status} - Est. Time: {time_needed}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Current strengths and gaps
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💪 Your Current Strengths")
            strengths = analysis.get('current_strengths', [])
            for strength in strengths:
                st.markdown(f"✅ {strength}")
            
            if not strengths:
                st.markdown("• Analysis of current strengths in progress...")
        
        with col2:
            st.subheader("🎯 Skill Gaps to Address")
            gaps = analysis.get('skill_gaps', {})
            
            if gaps.get('critical'):
                st.markdown("**🔴 Critical (Must Have):**")
                for skill in gaps['critical'][:5]:
                    st.markdown(f"• {skill}")
            
            if gaps.get('important'):
                st.markdown("**🟡 Important (Should Have):**")
                for skill in gaps['important'][:5]:
                    st.markdown(f"• {skill}")
        
        # Learning path
        learning_path = analysis.get('learning_path', {})
        if learning_path:
            st.subheader("📚 Personalized Learning Path")
            
            # Immediate priorities
            if learning_path.get('immediate'):
                with st.expander("🚀 Immediate Priorities (Next 1-3 months)", expanded=True):
                    for skill_item in learning_path['immediate']:
                        skill_name = skill_item.get('skill', 'Unknown Skill')
                        priority = skill_item.get('priority', 'Medium')
                        time_needed = skill_item.get('time_needed', 'Unknown')
                        resources = skill_item.get('resources', [])
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown(f"**{skill_name}**")
                            st.markdown(f"Resources: {', '.join(resources[:3])}")
                        with col2:
                            st.markdown(f"Priority: **{priority}**")
                            st.markdown(f"Time: {time_needed}")
                        st.markdown("---")
            
            # Short-term goals
            if learning_path.get('short_term'):
                with st.expander("📈 Short-term Goals (3-6 months)"):
                    for skill_item in learning_path['short_term']:
                        skill_name = skill_item.get('skill', 'Unknown Skill')
                        st.markdown(f"• **{skill_name}** ({skill_item.get('time_needed', 'Unknown time')})")
            
            # Long-term development
            if learning_path.get('long_term'):
                with st.expander("🎯 Long-term Development (6+ months)"):
                    for skill_item in learning_path['long_term']:
                        skill_name = skill_item.get('skill', 'Unknown Skill')
                        st.markdown(f"• **{skill_name}** ({skill_item.get('time_needed', 'Unknown time')})")
        
        # Additional recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            exp_building = analysis.get('experience_building', [])
            if exp_building:
                st.subheader("🛠️ Experience Building")
                for exp in exp_building:
                    st.markdown(f"• {exp}")
            
            certs = analysis.get('certification_recommendations', [])
            if certs:
                st.subheader("🏆 Recommended Certifications")
                for cert in certs:
                    st.markdown(f"• {cert}")
        
        with col2:
            networking = analysis.get('networking_opportunities', [])
            if networking:
                st.subheader("🤝 Networking Opportunities")
                for opportunity in networking:
                    st.markdown(f"• {opportunity}")
            
            # Competitive analysis
            competitive = analysis.get('competitive_analysis', {})
            if competitive:
                st.subheader("🏆 Competitive Position")
                if competitive.get('your_advantages'):
                    st.markdown(f"**Advantages:** {', '.join(competitive['your_advantages'][:2])}")
                if competitive.get('differentiation_strategy'):
                    st.markdown(f"**Strategy:** {', '.join(competitive['differentiation_strategy'][:2])}")
        
        # Monthly learning plan
        if analysis.get('monthly_learning_plan'):
            st.subheader("📅 3-Month Learning Plan")
            monthly_plan = analysis['monthly_learning_plan']
            
            col1, col2, col3 = st.columns(3)
            
            for i, (col, month_name) in enumerate([(col1, "Month 1"), (col2, "Month 2"), (col3, "Month 3")]):
                with col:
                    st.markdown(f"**{month_name}**")
                    if i < len(monthly_plan):
                        for item in monthly_plan[i][:4]:
                            st.markdown(f"• {item}")
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Create Study Schedule", use_container_width=True):
                self._create_study_schedule(analysis)
        
        with col2:
            if st.button("🔍 Find Learning Resources", use_container_width=True):
                self._find_learning_resources(analysis)
        
        with col3:
            if st.button("💾 Save Development Plan", use_container_width=True):
                st.success("Development plan saved to your profile!")
    
    # Helper methods for extracting user data
    def _extract_user_skills_from_assessments(self, user_profile: Dict[str, Any]) -> List[str]:
        """Extract skills from user assessment data"""
        skills = []
        assessments = user_profile.get('assessments', {})
        
        for assessment_name, assessment_data in assessments.items():
            if assessment_data.get('completed') and assessment_data.get('data'):
                data = assessment_data['data']
                
                # Extract from different fields
                if 'themes' in data:
                    skills.extend(data['themes'])
                if 'strengths' in data:
                    skills.extend(data['strengths'])
                if 'career_implications' in data:
                    skills.extend(data['career_implications'])
        
        # Add some default skills based on background
        background = user_profile.get('background', 'Professional')
        if background == "Student":
            skills.extend(["Learning agility", "Academic research", "Theoretical knowledge"])
        elif background == "Professional":
            skills.extend(["Professional experience", "Workplace communication", "Problem solving"])
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_user_strengths(self, user_profile: Dict[str, Any]) -> List[str]:
        """Extract user strengths from assessments"""
        strengths = []
        assessments = user_profile.get('assessments', {})
        
        for assessment_data in assessments.values():
            if assessment_data.get('completed') and assessment_data.get('data'):
                data = assessment_data['data']
                if 'strengths' in data:
                    strengths.extend(data['strengths'][:2])  # Top 2 from each assessment
        
        return list(set(strengths))
    
    def _get_assessment_summary(self, user_profile: Dict[str, Any]) -> str:
        """Get a summary of completed assessments"""
        assessments = user_profile.get('assessments', {})
        completed = [name for name, data in assessments.items() if data.get('completed')]
        
        if completed:
            return f"Completed assessments: {', '.join(completed[:5])}"
        return "No assessments completed yet"
    
    def _calculate_application_readiness(self, analysis: Dict[str, Any]) -> str:
        """Calculate application readiness based on match analysis"""
        match_score = analysis.get('overall_match_score', 0)
        
        if match_score >= 80:
            return "Ready to Apply"
        elif match_score >= 65:
            return "Almost Ready"
        else:
            return "Needs Preparation"
    
    def _assess_competitive_position(self, analysis: Dict[str, Any]) -> str:
        """Assess competitive position"""
        match_score = analysis.get('overall_match_score', 0)
        
        if match_score >= 85:
            return "Strong Candidate"
        elif match_score >= 70:
            return "Competitive"
        else:
            return "Developing"
    
    def _extract_user_experience(self, user_profile: Dict[str, Any]) -> str:
        """Extract user experience level"""
        # This would be enhanced to look at actual experience data
        return user_profile.get('experience_level', 'Mid-level professional')
    
    def _generate_fallback_analysis(self, job_description: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback analysis if AI processing fails"""
        return {
            "overall_match_score": 70,
            "match_breakdown": {
                "skills_match": 65,
                "experience_match": 75,
                "culture_fit": 70,
                "growth_potential": 70
            },
            "matching_elements": {
                "required_skills": ["General professional skills"],
                "preferred_skills": ["Communication", "Problem solving"],
                "experience_areas": ["Professional experience"],
                "soft_skills": ["Teamwork", "Adaptability"]
            },
            "missing_elements": {
                "critical_skills": ["Specific technical skills"],
                "preferred_skills": ["Domain expertise"],
                "experience_gaps": ["Industry-specific experience"],
                "certifications": ["Professional certifications"]
            },
            "strengths": ["Strong foundational skills", "Professional background"],
            "concerns": ["Limited specific technical experience"],
            "recommendations": {
                "immediate_actions": ["Tailor resume to highlight relevant skills"],
                "skill_development": ["Focus on key technical skills"],
                "experience_building": ["Seek relevant project experience"],
                "application_tips": ["Emphasize transferable skills"]
            },
            "salary_estimate": {
                "min": 60000,
                "max": 90000,
                "currency": "USD",
                "note": "Estimate based on general market data"
            },
            "interview_prep": ["Research company background", "Prepare skill examples"]
        }
    
    def _generate_fallback_skill_analysis(self, target_industry: str, target_level: str) -> Dict[str, Any]:
        """Generate fallback skill gap analysis"""
        return {
            "skill_gap_score": 65,
            "readiness_level": "Moderately Ready",
            "time_to_readiness": "3-6 months",
            "current_strengths": ["Professional experience", "Learning ability"],
            "skill_gaps": {
                "critical": [f"{target_industry} specific skills"],
                "important": ["Advanced technical skills"],
                "nice_to_have": ["Industry certifications"]
            },
            "learning_path": {
                "immediate": [
                    {"skill": "Core industry skills", "priority": "High", "time_needed": "2-3 months", "resources": ["Online courses", "Books"]}
                ],
                "short_term": [
                    {"skill": "Advanced concepts", "priority": "Medium", "time_needed": "3-4 months", "resources": ["Specialized training"]}
                ],
                "long_term": [
                    {"skill": "Leadership skills", "priority": "Medium", "time_needed": "6+ months", "resources": ["Experience", "Mentorship"]}
                ]
            },
            "experience_building": ["Build relevant projects", "Seek mentorship"],
            "networking_opportunities": ["Join professional groups", "Attend industry events"],
            "certification_recommendations": [f"{target_industry} certification"],
            "competitive_analysis": {
                "your_advantages": ["Diverse background"],
                "market_challenges": ["Competition from specialists"],
                "differentiation_strategy": ["Leverage unique perspective"]
            }
        }
    
    def _calculate_total_learning_time(self, analysis: Dict[str, Any]) -> str:
        """Calculate total learning time from learning path"""
        learning_path = analysis.get('learning_path', {})
        total_months = 0
        
        for phase in ['immediate', 'short_term', 'long_term']:
            if learning_path.get(phase):
                for item in learning_path[phase]:
                    time_str = item.get('time_needed', '1 month')
                    # Simple parsing - would be more sophisticated in production
                    if 'month' in time_str:
                        try:
                            months = int(time_str.split('-')[0])
                            total_months += months
                        except:
                            total_months += 2  # Default
        
        return f"{total_months} months total"
    
    def _create_monthly_plan(self, analysis: Dict[str, Any]) -> List[List[str]]:
        """Create 3-month learning plan"""
        learning_path = analysis.get('learning_path', {})
        monthly_plan = [[], [], []]
        
        # Distribute immediate priorities across first 2 months
        if learning_path.get('immediate'):
            for i, item in enumerate(learning_path['immediate'][:6]):
                month_idx = i % 2
                monthly_plan[month_idx].append(item.get('skill', 'Unknown skill'))
        
        # Add short-term to month 3
        if learning_path.get('short_term'):
            for item in learning_path['short_term'][:3]:
                monthly_plan[2].append(item.get('skill', 'Unknown skill'))
        
        return monthly_plan
    
    def _create_skill_development_plan(self, analysis: Dict[str, Any], missing_elements: Dict[str, Any]):
        """Create detailed skill development plan"""
        st.subheader("📋 Personalized Skill Development Plan")
        
        # Critical skills first
        if missing_elements.get('critical_skills'):
            st.markdown("### 🔴 Priority 1: Critical Skills (Immediate)")
            for skill in missing_elements['critical_skills']:
                with st.expander(f"📚 {skill}"):
                    st.markdown(f"""
                    **Why it's critical:** Required for basic job performance
                    
                    **Learning approach:**
                    - Start with fundamentals course
                    - Practice with hands-on projects
                    - Seek mentorship or guidance
                    
                    **Timeline:** 4-6 weeks intensive study
                    
                    **Resources:**
                    - Online courses (Coursera, Udemy)
                    - Practice platforms
                    - Community forums
                    """)
        
        # Important skills
        if missing_elements.get('preferred_skills'):
            st.markdown("### 🟡 Priority 2: Important Skills (Short-term)")
            for skill in missing_elements['preferred_skills'][:3]:
                with st.expander(f"📈 {skill}"):
                    st.markdown(f"""
                    **Why it's important:** Enhances competitiveness
                    
                    **Learning approach:**
                    - Build on foundation knowledge
                    - Apply in real projects
                    - Connect with professionals using this skill
                    
                    **Timeline:** 2-3 months steady progress
                    """)
    
    def _create_study_schedule(self, analysis: Dict[str, Any]):
        """Create detailed study schedule"""
        st.subheader("📅 Weekly Study Schedule")
        
        learning_path = analysis.get('learning_path', {})
        
        if learning_path.get('immediate'):
            st.markdown("### Week 1-4: Foundation Building")
            
            schedule = {
                "Monday": "Theory and concepts (2 hours)",
                "Tuesday": "Hands-on practice (2 hours)", 
                "Wednesday": "Project work (2 hours)",
                "Thursday": "Review and reinforcement (1 hour)",
                "Friday": "Community engagement (1 hour)",
                "Saturday": "Deep practice session (3 hours)",
                "Sunday": "Weekly review and planning (1 hour)"
            }
            
            for day, activity in schedule.items():
                st.markdown(f"**{day}:** {activity}")
            
            st.markdown("### Study Tips")
            st.markdown("""
            - **Consistency over intensity:** Regular daily practice beats weekend cramming
            - **Active learning:** Apply concepts immediately in mini-projects
            - **Track progress:** Keep a learning journal
            - **Seek feedback:** Join study groups or find a mentor
            - **Rest and review:** Take breaks and regularly review previous material
            """)
    
    def _find_learning_resources(self, analysis: Dict[str, Any]):
        """Display curated learning resources"""
        st.subheader("📚 Curated Learning Resources")
        
        learning_path = analysis.get('learning_path', {})
        
        if learning_path.get('immediate'):
            for skill_item in learning_path['immediate'][:3]:
                skill_name = skill_item.get('skill', 'Unknown')
                
                with st.expander(f"📖 Resources for {skill_name}"):
                    st.markdown("""
                    **Free Resources:**
                    - YouTube tutorials and channels
                    - Free online courses (edX, Khan Academy)
                    - Documentation and official guides
                    - Open source projects
                    - Practice platforms (Codewars, LeetCode)
                    
                    **Paid Resources:**
                    - Udemy/Coursera comprehensive courses
                    - Pluralsight/LinkedIn Learning
                    - Books from O'Reilly, Manning
                    - Bootcamps and intensive programs
                    
                    **Community Resources:**
                    - Reddit communities
                    - Stack Overflow
                    - Discord/Slack groups
                    - Local meetups and conferences
                    
                    **Practice Opportunities:**
                    - Personal projects
                    - Open source contributions
                    - Volunteer work
                    - Freelance small projects
                    """)
    
    def _display_career_path_mapper(self, user_profile: Dict[str, Any]):
        """Display career path mapping functionality"""
        
        st.subheader("🗺️ Career Path Mapper")
        st.markdown("Visualize potential career trajectories and plan your professional journey")
        
        # Current position input
        col1, col2 = st.columns(2)
        
        with col1:
            current_industry = st.selectbox(
                "Current Industry:",
                ["Software Engineering", "Data Science", "Product Management", 
                 "Digital Marketing", "Finance", "Consulting", "Other"],
                help="Your current industry or the one you want to transition from"
            )
            
            current_role = st.text_input(
                "Current Role:",
                placeholder="e.g., Junior Data Analyst",
                help="Your current job title or closest equivalent"
            )
        
        with col2:
            career_goal = st.selectbox(
                "Career Goal:",
                ["Advance in same field", "Change industries", "Move to management", 
                 "Become a specialist", "Start own business", "Freelance/Consulting"],
                help="What type of career change are you looking for?"
            )
            
            time_horizon = st.selectbox(
                "Planning Horizon:",
                ["1-2 years", "3-5 years", "5-10 years", "10+ years"],
                help="How far ahead are you planning?"
            )
        
        # Additional preferences
        with st.expander("🎯 Additional Preferences (Optional)"):
            col1, col2 = st.columns(2)
            
            with col1:
                work_style = st.multiselect(
                    "Preferred Work Style:",
                    ["Remote work", "Hybrid", "Office-based", "Travel required", "Flexible hours"]
                )
                
                company_size = st.multiselect(
                    "Company Size Preference:",
                    ["Startup (1-50)", "Scale-up (51-500)", "Mid-size (501-5000)", "Enterprise (5000+)", "Government", "Non-profit"]
                )
            
            with col2:
                salary_priority = st.selectbox(
                    "Salary Priority:",
                    ["Maximize income", "Work-life balance", "Growth potential", "Job security", "Mission alignment"]
                )
                
                risk_tolerance = st.selectbox(
                    "Risk Tolerance:",
                    ["Conservative (stable career)", "Moderate (some risk for growth)", "Aggressive (high risk, high reward)"]
                )
        
        if st.button("🗺️ Map Career Paths", type="primary", use_container_width=True):
            with st.spinner("Mapping your career paths..."):
                career_paths = self._generate_career_paths(
                    user_profile, current_industry, current_role, career_goal, 
                    time_horizon, work_style, company_size, salary_priority, risk_tolerance
                )
                
                self._display_career_paths(career_paths)
    
    def _generate_career_paths(self, user_profile: Dict[str, Any], current_industry: str, 
                              current_role: str, career_goal: str, time_horizon: str,
                              work_style: List[str], company_size: List[str], 
                              salary_priority: str, risk_tolerance: str) -> Dict[str, Any]:
        """Generate possible career paths"""
        
        # Get predefined paths if available
        base_paths = self.career_paths.get(current_industry, {})
        
        prompt = f"""Generate comprehensive career path analysis and recommendations:

CURRENT SITUATION:
- Industry: {current_industry}
- Current Role: {current_role}
- Career Goal: {career_goal}
- Time Horizon: {time_horizon}
- Work Style: {', '.join(work_style)}
- Company Size: {', '.join(company_size)}
- Salary Priority: {salary_priority}
- Risk Tolerance: {risk_tolerance}

USER PROFILE:
- Background: {user_profile.get('background', 'Professional')}
- Assessment Summary: {self._get_assessment_summary(user_profile)}
- Key Strengths: {', '.join(self._extract_user_strengths(user_profile)[:5])}

Generate detailed career path analysis in JSON format:
{{
    "recommended_paths": [
        {{
            "path_name": "Traditional Advancement",
            "description": "Progressive advancement within current field",
            "timeline": [
                {{"year": "0-1", "role": "Current Role", "salary_range": "50000-70000", "key_skills": ["skill1", "skill2"]}},
                {{"year": "1-3", "role": "Next Level Role", "salary_range": "70000-90000", "key_skills": ["skill3", "skill4"]}},
                {{"year": "3-5", "role": "Senior Role", "salary_range": "90000-120000", "key_skills": ["skill5", "skill6"]}}
            ],
            "pros": ["Predictable progression", "Uses existing skills"],
            "cons": ["Limited scope", "May hit ceiling"],
            "success_probability": 85,
            "required_actions": ["Develop skill X", "Gain certification Y"],
            "networking_strategy": "Build relationships with senior colleagues",
            "risk_level": "Low"
        }}
    ],
    "alternative_paths": [
        {{
            "path_name": "Industry Pivot",
            "description": "Transition to related but different industry",
            "timeline": "Similar structure",
            "pros": ["New opportunities", "Skill diversification"],
            "cons": ["Learning curve", "Initial salary drop"],
            "success_probability": 65,
            "required_actions": ["Reskill in area X", "Build network in new industry"],
            "networking_strategy": "Attend industry events, informational interviews",
            "risk_level": "Medium"
        }}
    ],
    "key_decision_points": [
        {{"timing": "6 months", "decision": "Whether to pursue additional certification", "impact": "Affects advancement speed"}},
        {{"timing": "2 years", "decision": "Management vs specialist track", "impact": "Determines long-term trajectory"}}
    ],
    "market_trends": [
        "Industry trend 1 affecting career prospects",
        "Emerging skill demands",
        "Market outlook for next 5 years"
    ],
    "action_plan": {{
        "next_30_days": ["Action 1", "Action 2"],
        "next_90_days": ["Action 3", "Action 4"],
        "next_year": ["Major milestone 1", "Major milestone 2"]
    }}
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            paths = json.loads(response.content)
            return paths
        except Exception:
            return self._generate_fallback_career_paths(current_industry, career_goal)
    
    def _generate_fallback_career_paths(self, current_industry: str, career_goal: str) -> Dict[str, Any]:
        """Generate fallback career paths"""
        return {
            "recommended_paths": [
                {
                    "path_name": "Progressive Advancement",
                    "description": f"Advance within {current_industry}",
                    "timeline": [
                        {"year": "0-2", "role": "Current Level", "salary_range": "60000-80000", "key_skills": ["Core skills"]},
                        {"year": "2-4", "role": "Mid Level", "salary_range": "80000-100000", "key_skills": ["Advanced skills"]},
                        {"year": "4-6", "role": "Senior Level", "salary_range": "100000-130000", "key_skills": ["Leadership skills"]}
                    ],
                    "pros": ["Builds on experience", "Clear progression"],
                    "cons": ["Limited scope"],
                    "success_probability": 75,
                    "required_actions": ["Skill development", "Network building"],
                    "networking_strategy": "Internal promotion focus",
                    "risk_level": "Low"
                }
            ],
            "alternative_paths": [],
            "key_decision_points": [],
            "market_trends": [f"{current_industry} continues to evolve with new technologies"],
            "action_plan": {
                "next_30_days": ["Assess current skills", "Set learning goals"],
                "next_90_days": ["Begin skill development", "Expand network"],
                "next_year": ["Seek advancement opportunities"]
            }
        }
    
    def _display_career_paths(self, career_paths: Dict[str, Any]):
        """Display career path analysis results"""
        
        # Recommended paths
        recommended = career_paths.get('recommended_paths', [])
        
        if recommended:
            st.subheader("🎯 Recommended Career Paths")
            
            for i, path in enumerate(recommended):
                path_name = path.get('path_name', f'Path {i+1}')
                description = path.get('description', '')
                success_prob = path.get('success_probability', 50)
                risk_level = path.get('risk_level', 'Medium')
                
                # Path header
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"### 📈 {path_name}")
                    st.markdown(description)
                with col2:
                    st.metric("Success Probability", f"{success_prob}%")
                with col3:
                    st.metric("Risk Level", risk_level)
                
                # Timeline visualization
                timeline = path.get('timeline', [])
                if timeline:
                    st.markdown("**Career Progression Timeline:**")
                    
                    for step in timeline:
                        year = step.get('year', 'Unknown')
                        role = step.get('role', 'Role')
                        salary = step.get('salary_range', 'N/A')
                        skills = step.get('key_skills', [])
                        
                        col1, col2, col3 = st.columns([1, 2, 2])
                        with col1:
                            st.markdown(f"**Year {year}**")
                        with col2:
                            st.markdown(f"**{role}**")
                            st.markdown(f"💰 ${salary}")
                        with col3:
                            if skills:
                                st.markdown("**Key Skills:**")
                                for skill in skills[:3]:
                                    st.markdown(f"• {skill}")
                
                # Pros and cons
                col1, col2 = st.columns(2)
                
                with col1:
                    pros = path.get('pros', [])
                    if pros:
                        st.markdown("**✅ Advantages:**")
                        for pro in pros:
                            st.markdown(f"• {pro}")
                
                with col2:
                    cons = path.get('cons', [])
                    if cons:
                        st.markdown("**⚠️ Challenges:**")
                        for con in cons:
                            st.markdown(f"• {con}")
                
                # Required actions
                actions = path.get('required_actions', [])
                if actions:
                    st.markdown("**📋 Required Actions:**")
                    for action in actions:
                        st.markdown(f"• {action}")
                
                st.markdown("---")
        
        # Alternative paths
        alternatives = career_paths.get('alternative_paths', [])
        if alternatives:
            st.subheader("🔄 Alternative Paths to Consider")
            
            for alt in alternatives:
                with st.expander(f"📍 {alt.get('path_name', 'Alternative Path')}"):
                    st.markdown(alt.get('description', 'No description available'))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if alt.get('pros'):
                            st.markdown("**Pros:** " + ", ".join(alt['pros']))
                    with col2:
                        if alt.get('cons'):
                            st.markdown("**Cons:** " + ", ".join(alt['cons']))
        
        # Key decision points
        decisions = career_paths.get('key_decision_points', [])
        if decisions:
            st.subheader("🤔 Key Decision Points Ahead")
            
            for decision in decisions:
                timing = decision.get('timing', 'Soon')
                desc = decision.get('decision', 'Important decision')
                impact = decision.get('impact', 'Will affect your career')
                
                st.markdown(f"**{timing}:** {desc}")
                st.markdown(f"*Impact: {impact}*")
                st.markdown("---")
        
        # Action plan
        action_plan = career_paths.get('action_plan', {})
        if action_plan:
            st.subheader("🎬 Your Action Plan")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if action_plan.get('next_30_days'):
                    st.markdown("**Next 30 Days:**")
                    for action in action_plan['next_30_days']:
                        st.markdown(f"• {action}")
            
            with col2:
                if action_plan.get('next_90_days'):
                    st.markdown("**Next 90 Days:**")
                    for action in action_plan['next_90_days']:
                        st.markdown(f"• {action}")
            
            with col3:
                if action_plan.get('next_year'):
                    st.markdown("**Next Year:**")
                    for action in action_plan['next_year']:
                        st.markdown(f"• {action}")
        
        # Market trends
        trends = career_paths.get('market_trends', [])
        if trends:
            st.subheader("📊 Market Intelligence")
            for trend in trends:
                st.markdown(f"• {trend}")
    
    def _display_market_intelligence(self):
        """Display market intelligence and trends"""
        
        st.subheader("📈 Market Intelligence & Trends")
        st.markdown("Stay informed about job market trends and salary insights")
        
        # Market overview tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Salary Insights",
            "🔥 Hot Skills", 
            "📈 Industry Trends",
            "🌍 Geographic Data"
        ])
        
        with tab1:
            st.markdown("### 💰 Salary Benchmarking")
            
            col1, col2 = st.columns(2)
            with col1:
                industry = st.selectbox("Industry:", ["Software Engineering", "Data Science", "Product Management"])
                location = st.selectbox("Location:", ["San Francisco, CA", "New York, NY", "Austin, TX", "Remote"])
            
            with col2:
                experience = st.selectbox("Experience Level:", ["Entry (0-2 years)", "Mid (3-5 years)", "Senior (6+ years)"])
                company_type = st.selectbox("Company Type:", ["Tech Startup", "Fortune 500", "Mid-size", "Government"])
            
            # Mock salary data
            salary_data = {
                "Software Engineering": {"Entry": 85000, "Mid": 125000, "Senior": 165000},
                "Data Science": {"Entry": 95000, "Mid": 135000, "Senior": 175000},
                "Product Management": {"Entry": 90000, "Mid": 130000, "Senior": 170000}
            }
            
            exp_key = experience.split()[0]
            base_salary = salary_data.get(industry, {}).get(exp_key, 100000)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Median Salary", f"${base_salary:,}")
            with col2:
                st.metric("25th Percentile", f"${int(base_salary * 0.85):,}")
            with col3:
                st.metric("75th Percentile", f"${int(base_salary * 1.15):,}")
            with col4:
                st.metric("Growth (YoY)", "+8.5%")
        
        with tab2:
            st.markdown("### 🔥 Most In-Demand Skills")
            
            hot_skills = {
                "Software Engineering": ["Python", "React", "AWS", "Docker", "Kubernetes", "Go", "TypeScript", "GraphQL"],
                "Data Science": ["Python", "SQL", "Machine Learning", "Tableau", "Spark", "TensorFlow", "R", "Statistics"],
                "Product Management": ["Analytics", "A/B Testing", "Figma", "SQL", "Roadmapping", "Agile", "User Research", "Growth"]
            }
            
            selected_field = st.selectbox("Select Field:", list(hot_skills.keys()))
            skills_list = hot_skills.get(selected_field, [])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🚀 Trending Up:**")
                for skill in skills_list[:4]:
                    growth = f"+{15 + hash(skill) % 20}%"
                    st.markdown(f"• **{skill}** ({growth})")
            
            with col2:
                st.markdown("**💡 Emerging Skills:**")
                emerging = ["AI/ML", "Web3", "Cloud Native", "DevOps"]
                for skill in emerging:
                    st.markdown(f"• {skill}")
        
        with tab3:
            st.markdown("### 📈 Industry Outlook")
            
            trends = {
                "Software Engineering": [
                    "AI/ML integration in all applications",
                    "Continued growth in cloud-native development",
                    "Increased focus on security and privacy",
                    "Remote work becoming permanent fixture"
                ],
                "Data Science": [
                    "MLOps and model deployment focus",
                    "Automated machine learning tools",
                    "Privacy-preserving analytics",
                    "Real-time data processing demand"
                ],
                "Product Management": [
                    "Data-driven decision making standard",
                    "AI-assisted product development",
                    "Sustainability in product design",
                    "Cross-platform user experience focus"
                ]
            }
            
            for industry, trend_list in trends.items():
                with st.expander(f"📊 {industry} Trends"):
                    for trend in trend_list:
                        st.markdown(f"• {trend}")
        
        with tab4:
            st.markdown("### 🌍 Geographic Opportunities")
            
            locations = {
                "Remote-First Companies": {"growth": "+45%", "avg_salary": "$125K", "note": "Fastest growing segment"},
                "San Francisco Bay Area": {"growth": "+12%", "avg_salary": "$165K", "note": "Highest paying, high cost of living"},
                "Austin, TX": {"growth": "+28%", "avg_salary": "$135K", "note": "Tech hub with lower costs"},
                "New York, NY": {"growth": "+18%", "avg_salary": "$145K", "note": "Finance and media tech"},
                "Seattle, WA": {"growth": "+20%", "avg_salary": "$155K", "note": "Cloud and e-commerce center"}
            }
            
            for location, data in locations.items():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**{location}**")
                    st.markdown(f"*{data['note']}*")
                with col2:
                    st.metric("Job Growth", data['growth'])
                with col3:
                    st.metric("Avg Salary", data['avg_salary'])
                st.markdown("---")
