"""
Application Tracker & Career Management Dashboard for Remiro AI
============================================================

Comprehensive job application tracking, interview scheduling, networking management,
and career progress monitoring with analytics and insights.
"""

import json
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import streamlit as st
import uuid

class ApplicationTracker:
    """Comprehensive career management and application tracking system"""
    
    def __init__(self, llm):
        self.llm = llm
        
        # Application status options
        self.application_statuses = [
            "📝 Preparing to Apply",
            "📤 Applied", 
            "📧 Application Reviewed",
            "📞 Phone/Initial Screen",
            "💼 Technical Interview",
            "👥 Panel Interview",
            "🏢 Onsite/Final Round",
            "✅ Offer Received",
            "❌ Rejected",
            "⏸️ On Hold",
            "🚫 Withdrew Application"
        ]
        
        # Interview types and preparation
        self.interview_types = {
            "Phone Screen": {
                "duration": "15-30 minutes",
                "focus": "Basic qualifications, cultural fit",
                "prep_tips": [
                    "Research company basics",
                    "Prepare elevator pitch",
                    "Have questions ready about role"
                ]
            },
            "Technical Interview": {
                "duration": "45-90 minutes", 
                "focus": "Technical skills, problem-solving",
                "prep_tips": [
                    "Practice coding problems",
                    "Review technical concepts",
                    "Prepare to explain past projects"
                ]
            },
            "Behavioral Interview": {
                "duration": "30-60 minutes",
                "focus": "Past experiences, soft skills",
                "prep_tips": [
                    "Use STAR method for examples",
                    "Prepare leadership/conflict stories",
                    "Research company values"
                ]
            },
            "Panel Interview": {
                "duration": "60-90 minutes",
                "focus": "Team fit, multiple perspectives",
                "prep_tips": [
                    "Prepare for multiple questioners",
                    "Research each interviewer",
                    "Practice maintaining engagement with all"
                ]
            }
        }
        
        # Networking contact categories
        self.contact_categories = [
            "🎯 Target Company Employee",
            "👑 Hiring Manager", 
            "🤝 Recruiter",
            "🏆 Industry Leader",
            "👨‍🏫 Mentor/Advisor",
            "👥 Peer/Colleague",
            "📚 Informational Interview",
            "🔗 LinkedIn Connection"
        ]
    
    def display_application_tracker(self, user_profile: Dict[str, Any]):
        """Display the comprehensive application tracking interface"""
        
        st.header("📋 Career Management Dashboard")
        st.markdown("Track applications, interviews, networking, and career progress in one place")
        
        # Initialize user data if not exists
        if 'applications' not in user_profile:
            user_profile['applications'] = []
        if 'networking_contacts' not in user_profile:
            user_profile['networking_contacts'] = []
        if 'career_goals' not in user_profile:
            user_profile['career_goals'] = {}
        
        # Main dashboard tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Dashboard Overview",
            "📝 Job Applications", 
            "🤝 Networking Hub",
            "📅 Interview Scheduler",
            "🎯 Goal Tracking",
            "📈 Career Analytics"
        ])
        
        with tab1:
            self._display_dashboard_overview(user_profile)
        
        with tab2:
            self._display_job_applications(user_profile)
        
        with tab3:
            self._display_networking_hub(user_profile)
        
        with tab4:
            self._display_interview_scheduler(user_profile)
        
        with tab5:
            self._display_goal_tracking(user_profile)
        
        with tab6:
            self._display_career_analytics(user_profile)
    
    def _display_dashboard_overview(self, user_profile: Dict[str, Any]):
        """Display main dashboard with key metrics and recent activity"""
        
        st.subheader("📊 Your Career Dashboard")
        
        applications = user_profile.get('applications', [])
        networking_contacts = user_profile.get('networking_contacts', [])
        
        # Key metrics
        total_applications = len(applications)
        active_applications = len([app for app in applications if app.get('status') not in ['✅ Offer Received', '❌ Rejected', '🚫 Withdrew Application']])
        interviews_scheduled = len([app for app in applications if 'interviews' in app and app['interviews']])
        total_contacts = len(networking_contacts)
        
        # Metrics display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total Applications", total_applications)
            if total_applications > 0:
                success_rate = len([app for app in applications if app.get('status') == '✅ Offer Received']) / total_applications * 100
                st.metric("🎯 Success Rate", f"{success_rate:.1f}%")
        
        with col2:
            st.metric("🔄 Active Applications", active_applications)
            response_rate = len([app for app in applications if app.get('status') not in ['📝 Preparing to Apply', '📤 Applied']]) / max(total_applications, 1) * 100
            st.metric("📊 Response Rate", f"{response_rate:.1f}%")
        
        with col3:
            st.metric("🎤 Interviews Scheduled", interviews_scheduled)
            avg_time_to_interview = 14  # This would be calculated from actual data
            st.metric("⏱️ Avg Time to Interview", f"{avg_time_to_interview} days")
        
        with col4:
            st.metric("🤝 Network Contacts", total_contacts)
            active_contacts = len([contact for contact in networking_contacts if contact.get('last_contact_date') and (datetime.now() - datetime.fromisoformat(contact['last_contact_date'])).days < 30])
            st.metric("🔥 Active Contacts", active_contacts)
        
        # Recent activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Recent Applications")
            recent_apps = sorted(applications, key=lambda x: x.get('applied_date', '2024-01-01'), reverse=True)[:5]
            
            if recent_apps:
                for app in recent_apps:
                    company = app.get('company', 'Unknown Company')
                    position = app.get('position', 'Unknown Position')
                    status = app.get('status', '📝 Preparing to Apply')
                    applied_date = app.get('applied_date', 'Unknown')
                    
                    with st.expander(f"{company} - {position}"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"**Status:** {status}")
                        with col_b:
                            st.markdown(f"**Applied:** {applied_date}")
            else:
                st.markdown("*No applications yet. Add your first application in the Job Applications tab!*")
        
        with col2:
            st.subheader("📅 Upcoming Activities")
            
            # This would show upcoming interviews, follow-ups, etc.
            upcoming_activities = [
                {"type": "Interview", "company": "Tech Corp", "date": "Tomorrow 2:00 PM", "prep_status": "✅ Ready"},
                {"type": "Follow-up", "company": "Startup Inc", "date": "Friday", "prep_status": "⏳ Pending"},
            ]
            
            for activity in upcoming_activities[:5]:
                activity_type = activity.get('type', 'Activity')
                company = activity.get('company', 'Company')
                date = activity.get('date', 'TBD')
                status = activity.get('prep_status', '⏳ Pending')
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**{activity_type}:** {company}")
                with col_b:
                    st.markdown(f"**{date}** - {status}")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("➕ Add Application", use_container_width=True):
                st.session_state.show_add_application = True
        
        with col2:
            if st.button("👤 Add Contact", use_container_width=True):
                st.session_state.show_add_contact = True
        
        with col3:
            if st.button("📅 Schedule Interview", use_container_width=True):
                st.session_state.show_schedule_interview = True
        
        with col4:
            if st.button("🎯 Set Goal", use_container_width=True):
                st.session_state.show_set_goal = True
        
        # AI-powered insights
        if applications or networking_contacts:
            st.subheader("🧠 AI Insights & Recommendations")
            insights = self._generate_dashboard_insights(user_profile)
            
            for insight in insights:
                insight_type = insight.get('type', 'info')
                message = insight.get('message', '')
                
                if insight_type == 'success':
                    st.success(message)
                elif insight_type == 'warning':
                    st.warning(message)
                else:
                    st.info(message)
    
    def _display_job_applications(self, user_profile: Dict[str, Any]):
        """Display job application management interface"""
        
        st.subheader("📝 Job Application Manager")
        
        # Add new application
        with st.expander("➕ Add New Application", expanded=bool(getattr(st.session_state, 'show_add_application', False))):
            self._add_new_application(user_profile)
        
        # Application filters and search
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status:",
                ["All"] + self.application_statuses
            )
        
        with col2:
            company_search = st.text_input("Search Company:", placeholder="Company name...")
        
        with col3:
            date_range = st.selectbox(
                "Date Range:",
                ["All Time", "Last Week", "Last Month", "Last 3 Months"]
            )
        
        # Applications table
        applications = user_profile.get('applications', [])
        
        if applications:
            # Filter applications
            filtered_apps = self._filter_applications(applications, status_filter, company_search, date_range)
            
            st.subheader(f"📋 Your Applications ({len(filtered_apps)})")
            
            # Applications display
            for i, app in enumerate(filtered_apps):
                self._display_application_card(app, i, user_profile)
        
        else:
            st.markdown("### 🎯 Ready to Start Your Job Search?")
            st.markdown("""
            **Get started by adding your first application!**
            
            💡 **Pro Tips:**
            - Track every application, even if it's just an inquiry
            - Add notes about the role, company culture, and key contacts
            - Set reminders for follow-ups
            - Upload relevant documents for easy access
            """)
            
            if st.button("➕ Add Your First Application", type="primary"):
                st.session_state.show_add_application = True
                st.rerun()
    
    def _add_new_application(self, user_profile: Dict[str, Any]):
        """Add new job application form"""
        
        with st.form("add_application"):
            col1, col2 = st.columns(2)
            
            with col1:
                company = st.text_input("Company Name*", placeholder="e.g., Google")
                position = st.text_input("Position Title*", placeholder="e.g., Senior Software Engineer")
                job_url = st.text_input("Job Posting URL", placeholder="https://...")
                salary_range = st.text_input("Salary Range", placeholder="e.g., $120k - $150k")
            
            with col2:
                location = st.text_input("Location", placeholder="e.g., San Francisco, CA / Remote")
                application_source = st.selectbox("Application Source", 
                    ["Company Website", "LinkedIn", "Indeed", "Glassdoor", "Referral", "Recruiter", "Other"])
                status = st.selectbox("Current Status", self.application_statuses)
                priority = st.selectbox("Priority Level", ["🔥 High", "📈 Medium", "📋 Low"])
            
            # Additional details
            job_description = st.text_area("Job Description", height=100, 
                placeholder="Paste key requirements and responsibilities...")
            
            notes = st.text_area("Notes & Strategy", height=100,
                placeholder="Application strategy, key contacts, company insights...")
            
            # Contacts at company
            st.markdown("**Contacts at Company (Optional)**")
            col1, col2 = st.columns(2)
            with col1:
                contact_name = st.text_input("Contact Name", placeholder="John Smith")
                contact_role = st.text_input("Contact Role", placeholder="Engineering Manager")
            with col2:
                contact_email = st.text_input("Contact Email", placeholder="john@company.com")
                contact_linkedin = st.text_input("Contact LinkedIn", placeholder="linkedin.com/in/johnsmith")
            
            submitted = st.form_submit_button("📝 Add Application", type="primary")
            
            if submitted:
                if company and position:
                    new_application = {
                        'id': str(uuid.uuid4()),
                        'company': company,
                        'position': position,
                        'job_url': job_url,
                        'salary_range': salary_range,
                        'location': location,
                        'application_source': application_source,
                        'status': status,
                        'priority': priority,
                        'job_description': job_description,
                        'notes': notes,
                        'applied_date': datetime.now().strftime('%Y-%m-%d'),
                        'created_date': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat(),
                        'contacts': [],
                        'interviews': [],
                        'documents': [],
                        'follow_ups': []
                    }
                    
                    # Add contact if provided
                    if contact_name:
                        contact = {
                            'name': contact_name,
                            'role': contact_role,
                            'email': contact_email,
                            'linkedin': contact_linkedin
                        }
                        new_application['contacts'].append(contact)
                    
                    user_profile['applications'].append(new_application)
                    st.success(f"✅ Added application for {position} at {company}!")
                    st.session_state.show_add_application = False
                    st.rerun()
                else:
                    st.error("Please fill in Company Name and Position Title")
    
    def _display_application_card(self, app: Dict[str, Any], index: int, user_profile: Dict[str, Any]):
        """Display individual application card"""
        
        company = app.get('company', 'Unknown Company')
        position = app.get('position', 'Unknown Position')
        status = app.get('status', '📝 Preparing to Apply')
        priority = app.get('priority', '📋 Low')
        applied_date = app.get('applied_date', 'Unknown')
        
        # Main card
        with st.expander(f"{priority} {company} - {position} ({status})", expanded=False):
            # Application details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Company:** {company}")
                st.markdown(f"**Position:** {position}")
                st.markdown(f"**Location:** {app.get('location', 'Not specified')}")
                
                if app.get('salary_range'):
                    st.markdown(f"**Salary:** {app['salary_range']}")
            
            with col2:
                st.markdown(f"**Status:** {status}")
                st.markdown(f"**Priority:** {priority}")
                st.markdown(f"**Applied:** {applied_date}")
                st.markdown(f"**Source:** {app.get('application_source', 'Unknown')}")
            
            with col3:
                # Quick stats
                interviews = len(app.get('interviews', []))
                contacts = len(app.get('contacts', []))
                follow_ups = len(app.get('follow_ups', []))
                
                st.markdown(f"**Interviews:** {interviews}")
                st.markdown(f"**Contacts:** {contacts}")  
                st.markdown(f"**Follow-ups:** {follow_ups}")
            
            # Job description preview
            if app.get('job_description'):
                st.markdown("**Job Description:**")
                st.markdown(app['job_description'][:300] + "..." if len(app['job_description']) > 300 else app['job_description'])
            
            # Notes
            if app.get('notes'):
                st.markdown("**Notes:**")
                st.markdown(app['notes'])
            
            # Action buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button(f"✏️ Edit", key=f"edit_app_{index}"):
                    self._edit_application(app, user_profile)
            
            with col2:
                if st.button(f"📅 Interview", key=f"interview_app_{index}"):
                    st.session_state[f'schedule_interview_{app["id"]}'] = True
            
            with col3:
                if st.button(f"📝 Follow-up", key=f"followup_app_{index}"):
                    st.session_state[f'add_followup_{app["id"]}'] = True
            
            with col4:
                if st.button(f"👤 Contact", key=f"contact_app_{index}"):
                    st.session_state[f'add_contact_{app["id"]}'] = True
            
            with col5:
                if st.button(f"🗑️ Delete", key=f"delete_app_{index}"):
                    if st.session_state.get(f'confirm_delete_{app["id"]}'):
                        user_profile['applications'].remove(app)
                        st.success("Application deleted!")
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_{app["id"]}'] = True
                        st.warning("Click again to confirm deletion")
            
            # Conditional sections based on session state
            if st.session_state.get(f'schedule_interview_{app["id"]}'):
                self._add_interview_to_application(app)
            
            if st.session_state.get(f'add_followup_{app["id"]}'):
                self._add_followup_to_application(app)
            
            if st.session_state.get(f'add_contact_{app["id"]}'):
                self._add_contact_to_application(app)
    
    def _display_networking_hub(self, user_profile: Dict[str, Any]):
        """Display networking contact management"""
        
        st.subheader("🤝 Networking Hub")
        st.markdown("Manage your professional network and relationship building")
        
        # Add new contact
        with st.expander("👤 Add New Contact", expanded=bool(getattr(st.session_state, 'show_add_contact', False))):
            self._add_new_contact(user_profile)
        
        # Contact filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.selectbox("Filter by Category:", ["All"] + self.contact_categories)
        
        with col2:
            company_filter = st.text_input("Filter by Company:", placeholder="Company name...")
        
        with col3:
            contact_frequency = st.selectbox("Contact Frequency:", ["All", "Recent (30 days)", "Needs Follow-up"])
        
        # Display contacts
        contacts = user_profile.get('networking_contacts', [])
        
        if contacts:
            filtered_contacts = self._filter_contacts(contacts, category_filter, company_filter, contact_frequency)
            
            st.subheader(f"👥 Your Network ({len(filtered_contacts)})")
            
            for i, contact in enumerate(filtered_contacts):
                self._display_contact_card(contact, i, user_profile)
        
        else:
            st.markdown("### 🌱 Start Building Your Professional Network")
            st.markdown("""
            **Your network is your net worth!**
            
            💡 **Networking Tips:**
            - Quality over quantity - focus on meaningful connections
            - Add value to others before asking for help
            - Keep regular contact with key relationships
            - Track interaction history and personal details
            """)
    
    def _add_new_contact(self, user_profile: Dict[str, Any]):
        """Add new networking contact form"""
        
        with st.form("add_contact"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*", placeholder="Jane Smith")
                company = st.text_input("Company", placeholder="Tech Corp")
                position = st.text_input("Position/Title", placeholder="Senior Engineering Manager")
                category = st.selectbox("Contact Category", self.contact_categories)
            
            with col2:
                email = st.text_input("Email", placeholder="jane@techcorp.com")
                phone = st.text_input("Phone", placeholder="+1 (555) 123-4567")
                linkedin = st.text_input("LinkedIn Profile", placeholder="linkedin.com/in/janesmith")
                how_met = st.text_input("How You Met", placeholder="LinkedIn, Conference, Referral, etc.")
            
            # Additional details
            notes = st.text_area("Notes & Context", height=100,
                placeholder="Personal details, conversation history, mutual connections...")
            
            tags = st.text_input("Tags (comma-separated)", 
                placeholder="hiring-manager, python-expert, startup-founder")
            
            # Interaction tracking
            st.markdown("**Last Interaction (Optional)**")
            col1, col2 = st.columns(2)
            with col1:
                last_contact_date = st.date_input("Last Contact Date", value=None)
                interaction_type = st.selectbox("Interaction Type", 
                    ["Email", "LinkedIn Message", "Phone Call", "Video Call", "In-Person Meeting", "Conference", "Other"])
            with col2:
                interaction_notes = st.text_area("Interaction Summary", height=60,
                    placeholder="Brief summary of your last interaction...")
            
            submitted = st.form_submit_button("👤 Add Contact", type="primary")
            
            if submitted:
                if name:
                    new_contact = {
                        'id': str(uuid.uuid4()),
                        'name': name,
                        'company': company,
                        'position': position,
                        'category': category,
                        'email': email,
                        'phone': phone,
                        'linkedin': linkedin,
                        'how_met': how_met,
                        'notes': notes,
                        'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
                        'created_date': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat(),
                        'interactions': []
                    }
                    
                    # Add interaction if provided
                    if last_contact_date and interaction_type:
                        interaction = {
                            'date': last_contact_date.isoformat(),
                            'type': interaction_type,
                            'notes': interaction_notes,
                            'created_date': datetime.now().isoformat()
                        }
                        new_contact['interactions'].append(interaction)
                        new_contact['last_contact_date'] = last_contact_date.isoformat()
                    
                    user_profile['networking_contacts'].append(new_contact)
                    st.success(f"✅ Added {name} to your network!")
                    st.session_state.show_add_contact = False
                    st.rerun()
                else:
                    st.error("Please provide at least the contact's name")
    
    def _display_contact_card(self, contact: Dict[str, Any], index: int, user_profile: Dict[str, Any]):
        """Display individual contact card"""
        
        name = contact.get('name', 'Unknown Name')
        company = contact.get('company', 'Unknown Company')
        position = contact.get('position', 'Unknown Position')
        category = contact.get('category', '🔗 LinkedIn Connection')
        
        # Calculate days since last contact
        last_contact = contact.get('last_contact_date')
        days_since_contact = "Never" 
        if last_contact:
            try:
                last_date = datetime.fromisoformat(last_contact)
                days_since = (datetime.now() - last_date).days
                if days_since == 0:
                    days_since_contact = "Today"
                elif days_since == 1:
                    days_since_contact = "Yesterday"
                else:
                    days_since_contact = f"{days_since} days ago"
            except:
                days_since_contact = "Unknown"
        
        # Card header with color coding based on contact recency
        if days_since_contact == "Never":
            header_color = "🔴"
        elif "day" in days_since_contact and int(days_since_contact.split()[0]) > 90:
            header_color = "🟡"
        else:
            header_color = "🟢"
        
        with st.expander(f"{header_color} {name} - {company} ({category})", expanded=False):
            # Contact details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Name:** {name}")
                st.markdown(f"**Company:** {company}")
                st.markdown(f"**Position:** {position}")
                st.markdown(f"**Category:** {category}")
                
                if contact.get('how_met'):
                    st.markdown(f"**How Met:** {contact['how_met']}")
            
            with col2:
                st.markdown(f"**Last Contact:** {days_since_contact}")
                
                if contact.get('email'):
                    st.markdown(f"**Email:** {contact['email']}")
                if contact.get('phone'):
                    st.markdown(f"**Phone:** {contact['phone']}")
                if contact.get('linkedin'):
                    st.markdown(f"**LinkedIn:** [Profile]({contact['linkedin']})")
            
            # Tags
            tags = contact.get('tags', [])
            if tags:
                st.markdown(f"**Tags:** {', '.join(tags)}")
            
            # Notes
            if contact.get('notes'):
                st.markdown("**Notes:**")
                st.markdown(contact['notes'])
            
            # Recent interactions
            interactions = contact.get('interactions', [])
            if interactions:
                st.markdown("**Recent Interactions:**")
                recent_interactions = sorted(interactions, key=lambda x: x.get('date', ''), reverse=True)[:3]
                
                for interaction in recent_interactions:
                    date = interaction.get('date', 'Unknown')
                    interaction_type = interaction.get('type', 'Unknown')
                    notes = interaction.get('notes', '')
                    st.markdown(f"• **{date}** - {interaction_type}: {notes[:100]}...")
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button(f"📧 Log Interaction", key=f"interact_{index}"):
                    st.session_state[f'log_interaction_{contact["id"]}'] = True
            
            with col2:
                if st.button(f"✏️ Edit Contact", key=f"edit_contact_{index}"):
                    st.session_state[f'edit_contact_{contact["id"]}'] = True
            
            with col3:
                if st.button(f"📧 Email Draft", key=f"email_draft_{index}"):
                    self._generate_email_draft(contact)
            
            with col4:
                if st.button(f"🗑️ Remove", key=f"delete_contact_{index}"):
                    if st.session_state.get(f'confirm_delete_contact_{contact["id"]}'):
                        user_profile['networking_contacts'].remove(contact)
                        st.success("Contact removed!")
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_contact_{contact["id"]}'] = True
                        st.warning("Click again to confirm removal")
            
            # Conditional interaction logging
            if st.session_state.get(f'log_interaction_{contact["id"]}'):
                self._log_interaction_form(contact)
    
    def _display_interview_scheduler(self, user_profile: Dict[str, Any]):
        """Display interview scheduling and preparation interface"""
        
        st.subheader("📅 Interview Scheduler & Prep")
        st.markdown("Manage interviews and preparation materials")
        
        # This would be a comprehensive interview management system
        st.info("🎤 Interview Scheduler - Advanced interview management coming soon!")
    
    def _display_goal_tracking(self, user_profile: Dict[str, Any]):
        """Display career goal tracking interface"""
        
        st.subheader("🎯 Career Goal Tracking")
        st.markdown("Set, track, and achieve your career objectives")
        
        # This would be a goal tracking system
        st.info("🎯 Goal Tracking - Comprehensive goal management coming soon!")
    
    def _display_career_analytics(self, user_profile: Dict[str, Any]):
        """Display career analytics and insights"""
        
        st.subheader("📈 Career Analytics")
        st.markdown("Analyze your job search performance and career progress")
        
        applications = user_profile.get('applications', [])
        contacts = user_profile.get('networking_contacts', [])
        
        if not applications and not contacts:
            st.info("📊 Start adding applications and contacts to see your analytics!")
            return
        
        # Application analytics
        if applications:
            st.markdown("### 📝 Application Analytics")
            
            # Status distribution
            status_counts = {}
            for app in applications:
                status = app.get('status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Application Status Distribution:**")
                for status, count in status_counts.items():
                    percentage = (count / len(applications)) * 100
                    st.markdown(f"• {status}: {count} ({percentage:.1f}%)")
            
            with col2:
                # Response rate analysis
                total_apps = len(applications)
                responses = len([app for app in applications if app.get('status') not in ['📝 Preparing to Apply', '📤 Applied']])
                response_rate = (responses / total_apps * 100) if total_apps > 0 else 0
                
                st.metric("📊 Response Rate", f"{response_rate:.1f}%")
                
                # Success metrics
                interviews = len([app for app in applications if 'interviews' in app and app['interviews']])
                offers = len([app for app in applications if app.get('status') == '✅ Offer Received'])
                
                st.metric("🎤 Interview Rate", f"{(interviews/total_apps*100):.1f}%" if total_apps > 0 else "0%")
                st.metric("✅ Offer Rate", f"{(offers/total_apps*100):.1f}%" if total_apps > 0 else "0%")
        
        # Network analytics
        if contacts:
            st.markdown("### 🤝 Network Analytics")
            
            # Contact categories
            category_counts = {}
            for contact in contacts:
                category = contact.get('category', 'Unknown')
                category_counts[category] = category_counts.get(category, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Network Composition:**")
                for category, count in category_counts.items():
                    percentage = (count / len(contacts)) * 100
                    st.markdown(f"• {category}: {count} ({percentage:.1f}%)")
            
            with col2:
                # Networking activity
                recent_contacts = len([c for c in contacts if c.get('last_contact_date') and 
                                     (datetime.now() - datetime.fromisoformat(c['last_contact_date'])).days < 30])
                
                st.metric("🔥 Active Contacts (30 days)", recent_contacts)
                st.metric("📈 Network Growth", f"+{len(contacts)} this period")
        
        # AI-powered insights
        if applications or contacts:
            st.markdown("### 🧠 AI-Powered Insights")
            insights = self._generate_career_analytics_insights(user_profile)
            
            for insight in insights:
                st.markdown(f"💡 **{insight['title']}**")
                st.markdown(f"   {insight['description']}")
                if insight.get('action'):
                    st.markdown(f"   🎯 *Action:* {insight['action']}")
                st.markdown("")
    
    # Helper methods
    def _filter_applications(self, applications: List[Dict], status_filter: str, company_search: str, date_range: str) -> List[Dict]:
        """Filter applications based on criteria"""
        filtered = applications
        
        # Status filter
        if status_filter != "All":
            filtered = [app for app in filtered if app.get('status') == status_filter]
        
        # Company search
        if company_search:
            filtered = [app for app in filtered if company_search.lower() in app.get('company', '').lower()]
        
        # Date range filter would be implemented here
        
        return filtered
    
    def _filter_contacts(self, contacts: List[Dict], category_filter: str, company_filter: str, frequency: str) -> List[Dict]:
        """Filter contacts based on criteria"""
        filtered = contacts
        
        # Category filter
        if category_filter != "All":
            filtered = [contact for contact in filtered if contact.get('category') == category_filter]
        
        # Company filter
        if company_filter:
            filtered = [contact for contact in filtered if company_filter.lower() in contact.get('company', '').lower()]
        
        # Frequency filter would be implemented here
        
        return filtered
    
    def _generate_dashboard_insights(self, user_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate AI-powered dashboard insights"""
        insights = []
        
        applications = user_profile.get('applications', [])
        contacts = user_profile.get('networking_contacts', [])
        
        if len(applications) > 0:
            response_rate = len([app for app in applications if app.get('status') not in ['📝 Preparing to Apply', '📤 Applied']]) / len(applications)
            
            if response_rate < 0.2:
                insights.append({
                    'type': 'warning',
                    'message': 'Your response rate is below 20%. Consider improving your resume or targeting more suitable roles.'
                })
            elif response_rate > 0.4:
                insights.append({
                    'type': 'success', 
                    'message': f'Great response rate of {response_rate*100:.1f}%! Your applications are resonating well.'
                })
        
        if len(contacts) < 5:
            insights.append({
                'type': 'info',
                'message': 'Consider expanding your network. Aim for at least 10-15 quality professional contacts.'
            })
        
        return insights
    
    def _generate_career_analytics_insights(self, user_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate career analytics insights"""
        insights = []
        
        applications = user_profile.get('applications', [])
        contacts = user_profile.get('networking_contacts', [])
        
        # Application insights
        if applications:
            total_apps = len(applications)
            active_apps = len([app for app in applications if app.get('status') not in ['✅ Offer Received', '❌ Rejected', '🚫 Withdrew Application']])
            
            insights.append({
                'title': 'Application Pipeline Health',
                'description': f'You have {active_apps} active applications out of {total_apps} total. This indicates a healthy pipeline.',
                'action': 'Continue applying to 3-5 new positions weekly to maintain momentum.'
            })
        
        # Network insights  
        if contacts:
            recent_contacts = len([c for c in contacts if c.get('last_contact_date') and 
                                 (datetime.now() - datetime.fromisoformat(c['last_contact_date'])).days < 30])
            
            if recent_contacts < len(contacts) * 0.3:
                insights.append({
                    'title': 'Network Engagement Opportunity',
                    'description': f'Only {recent_contacts} of your {len(contacts)} contacts have been reached recently.',
                    'action': 'Reach out to 2-3 dormant connections weekly to rekindle relationships.'
                })
        
        return insights
    
    def _edit_application(self, app: Dict[str, Any], user_profile: Dict[str, Any]):
        """Edit application details"""
        st.info("Edit functionality would allow updating application details")
    
    def _add_interview_to_application(self, app: Dict[str, Any]):
        """Add interview to application"""
        st.info("Interview scheduling would be implemented here")
    
    def _add_followup_to_application(self, app: Dict[str, Any]):
        """Add follow-up to application"""
        st.info("Follow-up tracking would be implemented here")
    
    def _add_contact_to_application(self, app: Dict[str, Any]):
        """Add contact to application"""
        st.info("Contact addition would be implemented here")
    
    def _log_interaction_form(self, contact: Dict[str, Any]):
        """Log interaction with contact form"""
        st.info("Interaction logging form would be implemented here")
    
    def _generate_email_draft(self, contact: Dict[str, Any]):
        """Generate email draft for contact"""
        st.info("AI email draft generation would be implemented here")
