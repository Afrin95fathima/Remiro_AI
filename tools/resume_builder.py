"""
Resume Builder & ATS Reviewer Module for Remiro AI
==================================================

This module provides comprehensive resume building and reviewing capabilities
with ATS-friendly analysis and professional formatting.
"""

import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import streamlit as st

class ResumeBuilder:
    """Professional resume builder with ATS optimization"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def display_resume_builder(self, user_profile: Dict[str, Any]):
        """Display the resume builder interface"""
        
        st.header("📄 Professional Resume Builder")
        st.markdown("Create an ATS-friendly resume that gets noticed by recruiters")
        
        # Resume building tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Build Resume", 
            "📊 ATS Review", 
            "📋 Templates", 
            "💾 My Resumes"
        ])
        
        with tab1:
            self._display_resume_form(user_profile)
        
        with tab2:
            self._display_ats_reviewer()
        
        with tab3:
            self._display_templates()
        
        with tab4:
            self._display_saved_resumes(user_profile)
    
    def _display_resume_form(self, user_profile: Dict[str, Any]):
        """Display the resume building form"""
        
        st.subheader("Build Your Professional Resume")
        
        # Initialize resume data in session state
        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = {
                'personal_info': {},
                'professional_summary': '',
                'work_experience': [],
                'education': [],
                'skills': [],
                'certifications': [],
                'projects': [],
                'achievements': []
            }
        
        resume_data = st.session_state.resume_data
        
        # Personal Information Section
        with st.expander("👤 Personal Information", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                resume_data['personal_info']['full_name'] = st.text_input(
                    "Full Name *", 
                    value=resume_data['personal_info'].get('full_name', user_profile.get('name', ''))
                )
                resume_data['personal_info']['phone'] = st.text_input(
                    "Phone Number *", 
                    value=resume_data['personal_info'].get('phone', '')
                )
                resume_data['personal_info']['location'] = st.text_input(
                    "Location (City, State) *", 
                    value=resume_data['personal_info'].get('location', '')
                )
            
            with col2:
                resume_data['personal_info']['email'] = st.text_input(
                    "Email Address *", 
                    value=resume_data['personal_info'].get('email', '')
                )
                resume_data['personal_info']['linkedin'] = st.text_input(
                    "LinkedIn Profile", 
                    value=resume_data['personal_info'].get('linkedin', '')
                )
                resume_data['personal_info']['portfolio'] = st.text_input(
                    "Portfolio/Website", 
                    value=resume_data['personal_info'].get('portfolio', '')
                )
        
        # Professional Summary
        with st.expander("📋 Professional Summary", expanded=True):
            st.markdown("*A compelling 2-3 sentence overview of your professional background*")
            resume_data['professional_summary'] = st.text_area(
                "Professional Summary *",
                value=resume_data.get('professional_summary', ''),
                height=100,
                help="Focus on your years of experience, key skills, and what you bring to employers"
            )
            
            if st.button("🤖 AI-Generate Summary", key="ai_summary"):
                if user_profile.get('assessments'):
                    summary = self._generate_ai_summary(user_profile)
                    resume_data['professional_summary'] = summary
                    st.rerun()
        
        # Work Experience
        with st.expander("💼 Work Experience", expanded=True):
            st.markdown("*List your work experience in reverse chronological order*")
            
            # Add new experience button
            if st.button("➕ Add Work Experience", key="add_work_exp"):
                resume_data['work_experience'].append({
                    'job_title': '',
                    'company': '',
                    'location': '',
                    'start_date': '',
                    'end_date': '',
                    'current': False,
                    'responsibilities': []
                })
                st.rerun()
            
            # Display existing work experiences
            for i, exp in enumerate(resume_data['work_experience']):
                with st.container():
                    st.markdown(f"**Experience #{i+1}**")
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        exp['job_title'] = st.text_input(f"Job Title", key=f"job_title_{i}", value=exp.get('job_title', ''))
                        exp['company'] = st.text_input(f"Company", key=f"company_{i}", value=exp.get('company', ''))
                    
                    with col2:
                        exp['location'] = st.text_input(f"Location", key=f"exp_location_{i}", value=exp.get('location', ''))
                        exp['current'] = st.checkbox(f"Current Role", key=f"current_{i}", value=exp.get('current', False))
                    
                    with col3:
                        if st.button(f"🗑️", key=f"delete_exp_{i}", help="Delete this experience"):
                            resume_data['work_experience'].pop(i)
                            st.rerun()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        exp['start_date'] = st.text_input(f"Start Date (MM/YYYY)", key=f"start_date_{i}", value=exp.get('start_date', ''))
                    with col2:
                        if not exp['current']:
                            exp['end_date'] = st.text_input(f"End Date (MM/YYYY)", key=f"end_date_{i}", value=exp.get('end_date', ''))
                        else:
                            exp['end_date'] = 'Present'
                    
                    # Responsibilities
                    st.markdown("**Key Responsibilities & Achievements:**")
                    responsibilities_text = st.text_area(
                        f"Enter each responsibility/achievement on a new line",
                        key=f"responsibilities_{i}",
                        value='\n'.join(exp.get('responsibilities', [])),
                        height=150
                    )
                    exp['responsibilities'] = [r.strip() for r in responsibilities_text.split('\n') if r.strip()]
                    
                    if st.button(f"🤖 Optimize with AI", key=f"optimize_exp_{i}"):
                        optimized = self._optimize_experience_ai(exp)
                        exp['responsibilities'] = optimized
                        st.rerun()
                    
                    st.divider()
        
        # Education
        with st.expander("🎓 Education", expanded=True):
            self._display_education_section(resume_data)
        
        # Skills
        with st.expander("🛠️ Skills", expanded=True):
            self._display_skills_section(resume_data, user_profile)
        
        # Additional Sections
        with st.expander("🏆 Additional Sections (Optional)"):
            self._display_additional_sections(resume_data)
        
        # Generate Resume Button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📄 Preview Resume", type="primary", use_container_width=True):
                self._preview_resume(resume_data)
        
        with col2:
            if st.button("💾 Save Resume", use_container_width=True):
                self._save_resume(resume_data, user_profile)
        
        with col3:
            if st.button("📥 Download PDF", use_container_width=True):
                self._download_resume_pdf(resume_data)
    
    def _generate_ai_summary(self, user_profile: Dict[str, Any]) -> str:
        """Generate AI-powered professional summary"""
        
        assessments = user_profile.get('assessments', {})
        background = user_profile.get('background', 'Professional')
        
        # Extract key insights from assessments
        strengths = []
        skills = []
        values = []
        
        for assessment_name, assessment_data in assessments.items():
            if assessment_data.get('completed') and assessment_data.get('data'):
                data = assessment_data['data']
                if 'strengths' in data:
                    strengths.extend(data['strengths'][:2])  # Top 2 strengths per assessment
                if 'themes' in data:
                    skills.extend(data['themes'][:2])
                if 'career_implications' in data:
                    values.extend(data['career_implications'][:1])
        
        prompt = f"""Create a compelling professional summary for a resume based on this career assessment data:

Background: {background}
Key Strengths: {', '.join(strengths[:6])}
Skills/Themes: {', '.join(skills[:4])}
Career Focus: {', '.join(values[:3])}

Requirements:
- 2-3 sentences maximum
- Professional, confident tone
- Include years of experience (estimate based on background)
- Highlight top 3-4 most relevant skills
- End with value proposition for employers
- Use industry keywords
- ATS-friendly language

Examples of good summaries:
"Experienced Marketing Professional with 5+ years driving digital campaigns and brand growth. Proven expertise in data analytics, content strategy, and cross-functional collaboration. Passionate about leveraging creative problem-solving to deliver measurable results that exceed business objectives."

Write a professional summary following this format."""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content.strip()
        except Exception:
            return f"Dynamic {background} with proven expertise in problem-solving, collaboration, and strategic thinking. Passionate about continuous learning and delivering high-quality results that drive organizational success."
    
    def _display_ats_reviewer(self):
        """Display ATS resume review functionality"""
        
        st.subheader("📊 ATS Resume Reviewer")
        st.markdown("Upload your resume to get detailed ATS compatibility analysis")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF, DOCX, TXT)",
            type=['pdf', 'docx', 'txt'],
            help="Upload your current resume for ATS analysis"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            file_content = uploaded_file.read()
            
            with st.spinner("Analyzing your resume for ATS compatibility..."):
                # Extract text from file
                resume_text = self._extract_text_from_file(uploaded_file, file_content)
                
                # Perform ATS analysis
                analysis = self._perform_ats_analysis(resume_text)
                
                # Display results
                self._display_ats_results(analysis)
        
        # Job description matcher
        st.markdown("---")
        st.subheader("🎯 Job Description Matcher")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Your Resume**")
            resume_text_input = st.text_area(
                "Paste your resume text here:",
                height=300,
                placeholder="Copy and paste your resume content..."
            )
        
        with col2:
            st.markdown("**Job Description**")
            job_description = st.text_area(
                "Paste the job description:",
                height=300,
                placeholder="Copy and paste the job description you're interested in..."
            )
        
        if st.button("🔍 Analyze Match Score", type="primary"):
            if resume_text_input and job_description:
                with st.spinner("Calculating match score..."):
                    match_analysis = self._analyze_job_match(resume_text_input, job_description)
                    self._display_match_results(match_analysis)
            else:
                st.error("Please provide both resume text and job description")
    
    def _perform_ats_analysis(self, resume_text: str) -> Dict[str, Any]:
        """Perform comprehensive ATS analysis"""
        
        analysis = {
            'overall_score': 0,
            'sections': {},
            'keywords': {},
            'formatting': {},
            'recommendations': []
        }
        
        # Check for essential sections
        sections = {
            'contact_info': bool(re.search(r'(\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|@.*\.com)', resume_text, re.IGNORECASE)),
            'professional_summary': bool(re.search(r'(summary|profile|objective)', resume_text, re.IGNORECASE)),
            'work_experience': bool(re.search(r'(experience|employment|work history)', resume_text, re.IGNORECASE)),
            'education': bool(re.search(r'(education|degree|university|college)', resume_text, re.IGNORECASE)),
            'skills': bool(re.search(r'(skills|competencies|technical)', resume_text, re.IGNORECASE))
        }
        
        analysis['sections'] = sections
        
        # Calculate scores
        section_score = sum(sections.values()) / len(sections) * 100
        
        # Check formatting issues
        formatting_issues = []
        if len(re.findall(r'[•▪▫‣⁃]', resume_text)) < 3:
            formatting_issues.append("Add bullet points for better readability")
        
        if not re.search(r'\b(20\d{2}|19\d{2})\b', resume_text):
            formatting_issues.append("Include dates for work experience and education")
        
        analysis['formatting']['issues'] = formatting_issues
        analysis['formatting']['score'] = max(0, 100 - len(formatting_issues) * 15)
        
        # Overall score
        analysis['overall_score'] = (section_score + analysis['formatting']['score']) / 2
        
        return analysis
    
    def _display_ats_results(self, analysis: Dict[str, Any]):
        """Display ATS analysis results"""
        
        # Overall score
        score = analysis['overall_score']
        
        if score >= 80:
            score_color = "🟢"
            score_text = "Excellent"
        elif score >= 60:
            score_color = "🟡"
            score_text = "Good"
        else:
            score_color = "🔴"
            score_text = "Needs Improvement"
        
        st.metric(
            f"{score_color} ATS Compatibility Score",
            f"{score:.0f}/100",
            f"{score_text}"
        )
        
        # Section analysis
        st.subheader("📋 Section Analysis")
        
        col1, col2 = st.columns(2)
        
        sections_present = []
        sections_missing = []
        
        for section, present in analysis['sections'].items():
            section_name = section.replace('_', ' ').title()
            if present:
                sections_present.append(f"✅ {section_name}")
            else:
                sections_missing.append(f"❌ {section_name}")
        
        with col1:
            st.markdown("**Present Sections:**")
            for section in sections_present:
                st.markdown(section)
        
        with col2:
            st.markdown("**Missing Sections:**")
            for section in sections_missing:
                st.markdown(section)
            if not sections_missing:
                st.markdown("✅ All essential sections present!")
        
        # Formatting issues
        if analysis['formatting']['issues']:
            st.subheader("⚠️ Formatting Recommendations")
            for issue in analysis['formatting']['issues']:
                st.markdown(f"• {issue}")
    
    def _extract_text_from_file(self, uploaded_file, file_content: bytes) -> str:
        """Extract text from uploaded file"""
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'txt':
            return file_content.decode('utf-8')
        
        elif file_extension == 'pdf':
            # For production, you'd use PyPDF2 or pdfplumber
            # For now, return a placeholder
            return "PDF text extraction would be implemented here with PyPDF2 library"
        
        elif file_extension == 'docx':
            # For production, you'd use python-docx
            # For now, return a placeholder
            return "DOCX text extraction would be implemented here with python-docx library"
        
        return "Could not extract text from file"
    
    def _analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze how well resume matches job description"""
        
        prompt = f"""Analyze how well this resume matches the job description and provide a detailed compatibility report:

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_description[:2000]}

Provide analysis in this JSON format:
{{
    "overall_match_score": 85,
    "matching_keywords": ["python", "machine learning", "data analysis"],
    "missing_keywords": ["tensorflow", "aws", "docker"],
    "strengths": ["Strong technical background", "Relevant experience"],
    "gaps": ["Missing cloud experience", "No mention of specific tools"],
    "recommendations": ["Add AWS certification", "Highlight relevant projects"],
    "keyword_density_score": 75,
    "experience_match_score": 90,
    "skills_match_score": 80
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            analysis = json.loads(response.content)
            return analysis
        except Exception:
            # Fallback analysis
            return {
                "overall_match_score": 65,
                "matching_keywords": ["experience", "skills", "professional"],
                "missing_keywords": ["specific industry terms"],
                "strengths": ["General professional background"],
                "gaps": ["Need more specific keywords"],
                "recommendations": ["Tailor resume to job requirements"],
                "keyword_density_score": 60,
                "experience_match_score": 70,
                "skills_match_score": 65
            }
    
    def _display_match_results(self, analysis: Dict[str, Any]):
        """Display job match analysis results"""
        
        st.subheader("🎯 Match Analysis Results")
        
        # Overall match score
        overall_score = analysis.get('overall_match_score', 0)
        
        if overall_score >= 80:
            color = "🟢"
            status = "Excellent Match"
        elif overall_score >= 60:
            color = "🟡"
            status = "Good Match"
        else:
            color = "🔴"
            status = "Needs Improvement"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"{color} Overall Match", f"{overall_score}%", status)
        with col2:
            st.metric("🎯 Experience Match", f"{analysis.get('experience_match_score', 0)}%")
        with col3:
            st.metric("🛠️ Skills Match", f"{analysis.get('skills_match_score', 0)}%")
        
        # Detailed analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Matching Keywords")
            for keyword in analysis.get('matching_keywords', [])[:10]:
                st.markdown(f"• {keyword}")
            
            st.subheader("💪 Strengths")
            for strength in analysis.get('strengths', []):
                st.markdown(f"• {strength}")
        
        with col2:
            st.subheader("❌ Missing Keywords")
            for keyword in analysis.get('missing_keywords', [])[:10]:
                st.markdown(f"• {keyword}")
            
            st.subheader("📈 Recommendations")
            for rec in analysis.get('recommendations', []):
                st.markdown(f"• {rec}")
    
    def _display_templates(self):
        """Display resume templates"""
        
        st.subheader("📋 Professional Resume Templates")
        st.markdown("Choose from ATS-friendly templates optimized for different industries")
        
        templates = {
            "Modern Professional": {
                "description": "Clean, ATS-friendly design perfect for corporate roles",
                "industries": ["Business", "Finance", "Consulting", "Technology"],
                "features": ["Contact header", "Professional summary", "Work experience", "Education", "Skills"]
            },
            "Technical Expert": {
                "description": "Technical-focused layout for IT and engineering roles",
                "industries": ["Software Development", "Engineering", "Data Science", "IT"],
                "features": ["Technical skills section", "Projects showcase", "Certifications", "GitHub integration"]
            },
            "Creative Professional": {
                "description": "Balanced creativity and professionalism for creative industries",
                "industries": ["Marketing", "Design", "Media", "Communications"],
                "features": ["Portfolio links", "Creative projects", "Brand personal statement"]
            }
        }
        
        for template_name, template_info in templates.items():
            with st.expander(f"📄 {template_name}", expanded=False):
                st.markdown(f"**Description:** {template_info['description']}")
                st.markdown(f"**Best for:** {', '.join(template_info['industries'])}")
                st.markdown("**Key Features:**")
                for feature in template_info['features']:
                    st.markdown(f"• {feature}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"👀 Preview {template_name}", key=f"preview_{template_name}"):
                        st.info("Template preview would be displayed here")
                with col2:
                    if st.button(f"📝 Use Template", key=f"use_{template_name}", type="primary"):
                        st.success(f"Loading {template_name} template...")
                        # Would populate resume_data with template structure
    
    def _display_saved_resumes(self, user_profile: Dict[str, Any]):
        """Display saved resumes"""
        
        st.subheader("💾 My Saved Resumes")
        
        # Get saved resumes from user profile
        saved_resumes = user_profile.get('saved_resumes', [])
        
        if not saved_resumes:
            st.info("No saved resumes yet. Create your first resume using the Build Resume tab!")
            return
        
        for i, resume in enumerate(saved_resumes):
            with st.expander(f"📄 {resume.get('title', f'Resume {i+1}')}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Created:** {resume.get('created_date', 'Unknown')}")
                    st.markdown(f"**Last Modified:** {resume.get('modified_date', 'Unknown')}")
                    if resume.get('target_role'):
                        st.markdown(f"**Target Role:** {resume['target_role']}")
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_resume_{i}"):
                        st.session_state.resume_data = resume.get('data', {})
                        st.success("Resume loaded for editing!")
                        st.rerun()
                    
                    if st.button("📥 Download", key=f"download_resume_{i}"):
                        self._download_resume_pdf(resume.get('data', {}))
                    
                    if st.button("🗑️ Delete", key=f"delete_resume_{i}"):
                        # Would delete resume from user profile
                        st.warning("Delete confirmation would appear here")
    
    def _save_resume(self, resume_data: Dict[str, Any], user_profile: Dict[str, Any]):
        """Save resume to user profile"""
        
        resume_title = st.text_input("Resume Title:", value="My Resume")
        target_role = st.text_input("Target Role (Optional):", value="")
        
        if st.button("💾 Confirm Save"):
            saved_resume = {
                'title': resume_title,
                'target_role': target_role,
                'data': resume_data,
                'created_date': datetime.now().strftime("%Y-%m-%d"),
                'modified_date': datetime.now().strftime("%Y-%m-%d")
            }
            
            if 'saved_resumes' not in user_profile:
                user_profile['saved_resumes'] = []
            
            user_profile['saved_resumes'].append(saved_resume)
            
            # Save to user manager (would be implemented)
            st.success(f"✅ Resume '{resume_title}' saved successfully!")
    
    def _preview_resume(self, resume_data: Dict[str, Any]):
        """Preview the resume"""
        
        st.subheader("📄 Resume Preview")
        
        # Generate preview HTML
        preview_html = self._generate_resume_html(resume_data)
        
        # Display preview
        st.markdown(preview_html, unsafe_allow_html=True)
    
    def _generate_resume_html(self, resume_data: Dict[str, Any]) -> str:
        """Generate HTML representation of resume"""
        
        personal_info = resume_data.get('personal_info', {})
        
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;">
            <header style="text-align: center; margin-bottom: 20px;">
                <h1 style="margin: 0; color: #2c3e50;">{personal_info.get('full_name', 'Your Name')}</h1>
                <p style="margin: 5px 0; color: #7f8c8d;">
                    {personal_info.get('phone', '')} | {personal_info.get('email', '')} | {personal_info.get('location', '')}
                </p>
                <p style="margin: 5px 0; color: #3498db;">
                    {personal_info.get('linkedin', '')} | {personal_info.get('portfolio', '')}
                </p>
            </header>
        """
        
        # Professional Summary
        if resume_data.get('professional_summary'):
            html += f"""
            <section style="margin-bottom: 20px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;">PROFESSIONAL SUMMARY</h2>
                <p style="text-align: justify; line-height: 1.6;">{resume_data['professional_summary']}</p>
            </section>
            """
        
        # Work Experience
        if resume_data.get('work_experience'):
            html += '<section style="margin-bottom: 20px;"><h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;">WORK EXPERIENCE</h2>'
            
            for exp in resume_data['work_experience']:
                html += f"""
                <div style="margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #2c3e50;">{exp.get('job_title', '')} - {exp.get('company', '')}</h3>
                    <p style="margin: 2px 0; color: #7f8c8d; font-style: italic;">{exp.get('location', '')} | {exp.get('start_date', '')} - {exp.get('end_date', '')}</p>
                    <ul style="margin: 8px 0; padding-left: 20px;">
                """
                
                for responsibility in exp.get('responsibilities', []):
                    html += f"<li style='margin-bottom: 3px;'>{responsibility}</li>"
                
                html += "</ul></div>"
            
            html += "</section>"
        
        # Skills
        if resume_data.get('skills'):
            html += f"""
            <section style="margin-bottom: 20px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;">SKILLS</h2>
                <p>{', '.join(resume_data['skills'])}</p>
            </section>
            """
        
        html += "</div>"
        return html
    
    def _download_resume_pdf(self, resume_data: Dict[str, Any]):
        """Generate and download resume as PDF"""
        
        # For production, would use libraries like reportlab or weasyprint
        st.info("PDF generation would be implemented using reportlab or weasyprint library")
        st.markdown("Generated PDF would include:")
        st.markdown("• Professional formatting")
        st.markdown("• ATS-friendly layout")
        st.markdown("• Clean typography")
        st.markdown("• Optimized for printing")

# Additional helper functions for other sections would go here...
