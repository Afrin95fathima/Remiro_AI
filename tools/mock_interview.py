"""
Mock Interview AI System for Remiro AI
=====================================

Provides comprehensive mock interview practice with industry-specific questions,
real-time feedback, and performance analytics.
"""

import json
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
import streamlit as st

class MockInterviewAI:
    """AI-powered mock interview system"""
    
    def __init__(self, llm):
        self.llm = llm
        
        # Industry-specific question banks
        self.question_banks = {
            "Software Engineering": {
                "behavioral": [
                    "Tell me about a challenging bug you had to debug.",
                    "Describe a time when you had to learn a new technology quickly.",
                    "How do you handle code reviews and feedback from senior developers?",
                    "Tell me about a project where you had to work with a difficult team member.",
                    "Describe your approach to writing clean, maintainable code."
                ],
                "technical": [
                    "Explain the difference between REST and GraphQL APIs.",
                    "How would you optimize a slow database query?",
                    "What's the difference between synchronous and asynchronous programming?",
                    "Explain the concept of dependency injection.",
                    "How do you ensure your code is secure against common vulnerabilities?"
                ],
                "situational": [
                    "Your application is down in production. Walk me through your troubleshooting process.",
                    "You disagree with a technical decision made by your team lead. How do you handle it?",
                    "You're running behind on a sprint deadline. How do you communicate and manage expectations?",
                    "A stakeholder requests a feature that you know will cause technical debt. How do you respond?"
                ]
            },
            "Data Science": {
                "behavioral": [
                    "Tell me about a data project where your initial hypothesis was wrong.",
                    "How do you explain complex statistical concepts to non-technical stakeholders?",
                    "Describe a time when you had to work with messy or incomplete data.",
                    "Tell me about a machine learning model you built that didn't perform as expected."
                ],
                "technical": [
                    "Explain the bias-variance tradeoff in machine learning.",
                    "How do you handle missing data in your datasets?",
                    "What's the difference between supervised and unsupervised learning?",
                    "Explain cross-validation and why it's important.",
                    "How do you measure the performance of a classification model?"
                ],
                "situational": [
                    "Your model shows great performance in testing but poor results in production. What do you do?",
                    "A business stakeholder wants to use AI for a problem that doesn't need machine learning. How do you respond?",
                    "You discover bias in your training data. How do you address it?"
                ]
            },
            "Product Management": {
                "behavioral": [
                    "Tell me about a product feature you championed that failed.",
                    "Describe how you've handled conflicting priorities from different stakeholders.",
                    "Tell me about a time you had to make a product decision without complete data.",
                    "How do you handle pushback from engineering teams on your roadmap?"
                ],
                "technical": [
                    "How do you prioritize features in your product roadmap?",
                    "Explain how you would measure the success of a new feature.",
                    "What frameworks do you use for product discovery?",
                    "How do you conduct user research and incorporate feedback?"
                ],
                "situational": [
                    "Your biggest competitor just launched a feature you were planning. What's your response?",
                    "Engineering says your top priority feature will take 6 months instead of 2. How do you handle it?",
                    "You have limited resources and multiple urgent requests. How do you decide what to build?"
                ]
            },
            "Marketing": {
                "behavioral": [
                    "Tell me about a marketing campaign that didn't meet expectations.",
                    "Describe how you've used data to improve marketing performance.",
                    "Tell me about a time you had to market a product you didn't fully understand.",
                    "How do you handle creative differences with designers or agencies?"
                ],
                "technical": [
                    "How do you measure marketing ROI across different channels?",
                    "Explain your approach to A/B testing marketing campaigns.",
                    "How do you determine the right marketing mix for a new product?",
                    "What tools do you use for marketing automation and why?"
                ],
                "situational": [
                    "Your biggest marketing channel just changed their algorithm, reducing your reach by 50%. What do you do?",
                    "You need to launch a product in a market you've never worked in before. How do you approach it?",
                    "Your CEO wants to cut the marketing budget by 30%. How do you adjust your strategy?"
                ]
            },
            "General": {
                "behavioral": [
                    "Tell me about yourself and your career journey.",
                    "Why are you interested in this role and our company?",
                    "Describe your greatest professional achievement.",
                    "Tell me about a time you failed and what you learned from it.",
                    "How do you handle stress and tight deadlines?",
                    "Describe a situation where you had to work with a difficult colleague.",
                    "Tell me about a time you had to learn something new quickly.",
                    "How do you prioritize tasks when everything seems urgent?",
                    "Describe your ideal work environment and management style.",
                    "Where do you see yourself in 5 years?"
                ],
                "situational": [
                    "How would you handle a situation where you disagree with your manager?",
                    "What would you do if you realized you made a mistake that affected others?",
                    "How would you approach a project with unclear requirements?",
                    "What would you do if you had competing priorities from different stakeholders?"
                ]
            }
        }
    
    def display_mock_interview(self, user_profile: Dict[str, Any]):
        """Display the mock interview interface"""
        
        st.header("🎤 AI Mock Interview Practice")
        st.markdown("Practice interviews with AI-powered feedback and coaching")
        
        # Interview tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Start Interview",
            "📊 Practice Sessions", 
            "💡 Interview Tips",
            "🏆 Performance Analytics"
        ])
        
        with tab1:
            self._display_interview_setup(user_profile)
        
        with tab2:
            self._display_practice_sessions(user_profile)
        
        with tab3:
            self._display_interview_tips()
        
        with tab4:
            self._display_analytics(user_profile)
    
    def _display_interview_setup(self, user_profile: Dict[str, Any]):
        """Display interview setup and configuration"""
        
        st.subheader("🎯 Interview Setup")
        
        # Interview configuration
        col1, col2 = st.columns(2)
        
        with col1:
            interview_type = st.selectbox(
                "Interview Type:",
                ["Behavioral", "Technical", "Mixed", "Phone Screen", "Final Round"],
                help="Choose the type of interview you want to practice"
            )
            
            industry = st.selectbox(
                "Industry/Role:",
                ["General", "Software Engineering", "Data Science", "Product Management", 
                 "Marketing", "Sales", "Consulting", "Finance"],
                help="Select your target industry for relevant questions"
            )
            
            difficulty_level = st.selectbox(
                "Difficulty Level:",
                ["Entry Level", "Mid Level", "Senior Level", "Executive"],
                help="Choose appropriate difficulty for your experience level"
            )
        
        with col2:
            num_questions = st.slider(
                "Number of Questions:",
                min_value=3,
                max_value=15,
                value=8,
                help="How many questions do you want to practice?"
            )
            
            time_limit = st.selectbox(
                "Time Limit per Question:",
                ["No Limit", "1 minute", "2 minutes", "3 minutes", "5 minutes"],
                help="Set a time limit to simulate real interview pressure"
            )
            
            feedback_style = st.selectbox(
                "Feedback Style:",
                ["Detailed", "Concise", "Coaching", "Scoring Only"],
                help="Choose how you want to receive feedback"
            )
        
        # Company-specific preparation
        with st.expander("🏢 Company-Specific Preparation (Optional)"):
            company_name = st.text_input("Company Name:", placeholder="e.g., Google, Microsoft, Startups")
            company_info = st.text_area(
                "Company Information:",
                placeholder="Paste company info, values, recent news, or job description...",
                height=100
            )
            
            if company_name and company_info:
                st.info(f"Questions will be customized for {company_name} based on the information provided.")
        
        # Start interview button
        if st.button("🎬 Start Interview", type="primary", use_container_width=True):
            # Initialize interview session
            interview_config = {
                'type': interview_type,
                'industry': industry,
                'difficulty': difficulty_level,
                'num_questions': num_questions,
                'time_limit': time_limit,
                'feedback_style': feedback_style,
                'company_name': company_name,
                'company_info': company_info,
                'started_at': datetime.now().isoformat()
            }
            
            st.session_state.interview_active = True
            st.session_state.interview_config = interview_config
            st.session_state.current_question_idx = 0
            st.session_state.interview_responses = []
            
            st.rerun()
        
        # Active interview session
        if st.session_state.get('interview_active', False):
            self._run_interview_session(user_profile)
    
    def _run_interview_session(self, user_profile: Dict[str, Any]):
        """Run the active interview session"""
        
        config = st.session_state.interview_config
        current_idx = st.session_state.current_question_idx
        
        st.markdown("---")
        st.subheader(f"🎤 {config['type']} Interview - {config['industry']}")
        
        # Progress indicator
        progress = (current_idx + 1) / config['num_questions']
        st.progress(progress)
        st.markdown(f"**Question {current_idx + 1} of {config['num_questions']}**")
        
        # Generate question
        if current_idx < config['num_questions']:
            question = self._generate_question(config, current_idx, user_profile)
            
            # Display question
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #2d3748; margin-bottom: 15px;">💬 Interview Question:</h3>
                <p style="font-size: 18px; color: #4a5568; line-height: 1.6; margin: 0;">
                    {question}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Timer display
            if config['time_limit'] != "No Limit":
                st.markdown(f"⏰ **Time Limit:** {config['time_limit']}")
                # In production, would implement actual countdown timer
            
            # Response input
            response_method = st.radio(
                "How would you like to respond?",
                ["Type Response", "Record Audio", "Just Get Feedback"],
                horizontal=True
            )
            
            user_response = ""
            
            if response_method == "Type Response":
                user_response = st.text_area(
                    "Your Response:",
                    height=200,
                    placeholder="Type your interview response here. Take your time to craft a thoughtful answer using the STAR method (Situation, Task, Action, Result) for behavioral questions."
                )
            
            elif response_method == "Record Audio":
                st.info("🎙️ Audio recording feature would be implemented here using speech-to-text")
                # Would implement audio recording and transcription
                user_response = st.text_area("Transcribed Response:", height=100)
            
            else:  # Just Get Feedback
                user_response = "User requested feedback without providing response"
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("📝 Get Feedback", type="primary", disabled=not user_response):
                    feedback = self._generate_feedback(question, user_response, config)
                    
                    # Store response and feedback
                    st.session_state.interview_responses.append({
                        'question': question,
                        'response': user_response,
                        'feedback': feedback,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    # Display feedback
                    self._display_feedback(feedback)
            
            with col2:
                if st.button("⏭️ Next Question"):
                    st.session_state.current_question_idx += 1
                    st.rerun()
            
            with col3:
                if st.button("🔚 End Interview"):
                    self._end_interview(user_profile)
        
        else:
            # Interview completed
            st.success("🎉 Interview completed!")
            self._display_interview_summary(user_profile)
            self._end_interview(user_profile)
    
    def _generate_question(self, config: Dict[str, Any], question_idx: int, user_profile: Dict[str, Any]) -> str:
        """Generate an appropriate interview question"""
        
        industry = config['industry']
        interview_type = config['type'].lower()
        
        # Get question bank for industry
        questions = self.question_banks.get(industry, self.question_banks["General"])
        
        # Select question type based on interview type
        if interview_type == "behavioral":
            question_pool = questions.get("behavioral", questions.get("behavioral", []))
        elif interview_type == "technical":
            question_pool = questions.get("technical", [])
        elif interview_type == "mixed":
            # Mix of behavioral and technical
            all_questions = []
            all_questions.extend(questions.get("behavioral", []))
            all_questions.extend(questions.get("technical", []))
            all_questions.extend(questions.get("situational", []))
            question_pool = all_questions
        else:
            # Default to behavioral + situational
            question_pool = questions.get("behavioral", []) + questions.get("situational", [])
        
        if not question_pool:
            question_pool = self.question_banks["General"]["behavioral"]
        
        # Select a question
        if question_idx < len(question_pool):
            base_question = question_pool[question_idx % len(question_pool)]
        else:
            base_question = random.choice(question_pool)
        
        # Customize for company if provided
        if config.get('company_name') and config.get('company_info'):
            customized_question = self._customize_question_for_company(
                base_question, 
                config['company_name'], 
                config['company_info']
            )
            return customized_question
        
        return base_question
    
    def _customize_question_for_company(self, question: str, company_name: str, company_info: str) -> str:
        """Customize question for specific company"""
        
        prompt = f"""Customize this interview question for {company_name}:

Original question: {question}

Company information: {company_info}

Make the question more specific and relevant to {company_name} while keeping the core intent. If the original question doesn't need customization, return it as-is.

Examples:
- "Tell me about yourself" → "Tell me about yourself and why you're specifically interested in {company_name}"
- "Describe a challenging project" → "Describe a challenging project, and how you'd apply those learnings at {company_name}"

Return only the customized question."""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content.strip()
        except Exception:
            return f"{question} (Specifically at {company_name})"
    
    def _generate_feedback(self, question: str, response: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI feedback for interview response"""
        
        feedback_style = config.get('feedback_style', 'Detailed')
        difficulty = config.get('difficulty', 'Mid Level')
        
        prompt = f"""You are an expert interview coach. Analyze this interview response and provide {feedback_style.lower()} feedback.

QUESTION: {question}

RESPONSE: {response}

INTERVIEW CONTEXT:
- Role Level: {difficulty}
- Industry: {config.get('industry', 'General')}
- Interview Type: {config.get('type', 'General')}

Provide feedback in JSON format:
{{
    "overall_score": 75,
    "strengths": ["Specific positive points"],
    "areas_for_improvement": ["Specific suggestions"],
    "structure_score": 80,
    "content_score": 70,
    "delivery_score": 75,
    "specific_tips": ["Actionable advice"],
    "sample_improvement": "Here's how you could improve this response...",
    "body_language_tips": ["Professional presence suggestions"],
    "follow_up_questions": ["Questions interviewer might ask next"]
}}

Focus on:
- STAR method usage for behavioral questions
- Specific examples and quantifiable results
- Clarity and conciseness
- Professional tone
- Relevance to the question asked
"""
        
        try:
            response_obj = self.llm.invoke(prompt)
            feedback = json.loads(response_obj.content)
            return feedback
        except Exception as e:
            # Fallback feedback
            return {
                "overall_score": 70,
                "strengths": ["Provided a response", "Professional tone"],
                "areas_for_improvement": ["Add more specific examples", "Use STAR method"],
                "structure_score": 70,
                "content_score": 70,
                "delivery_score": 70,
                "specific_tips": ["Practice with more specific examples", "Work on storytelling"],
                "sample_improvement": "Consider restructuring your response using the STAR method",
                "body_language_tips": ["Maintain eye contact", "Use confident posture"],
                "follow_up_questions": ["Can you give me another example?"]
            }
    
    def _display_feedback(self, feedback: Dict[str, Any]):
        """Display interview feedback"""
        
        st.markdown("---")
        st.subheader("📊 Interview Feedback")
        
        # Overall score
        overall_score = feedback.get('overall_score', 0)
        
        if overall_score >= 80:
            score_color = "🟢"
            score_text = "Excellent"
        elif overall_score >= 60:
            score_color = "🟡"
            score_text = "Good"
        else:
            score_color = "🔴"
            score_text = "Needs Work"
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(f"{score_color} Overall", f"{overall_score}/100", score_text)
        with col2:
            st.metric("📝 Structure", f"{feedback.get('structure_score', 0)}/100")
        with col3:
            st.metric("💡 Content", f"{feedback.get('content_score', 0)}/100")
        with col4:
            st.metric("🎤 Delivery", f"{feedback.get('delivery_score', 0)}/100")
        
        # Detailed feedback
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💪 Strengths")
            for strength in feedback.get('strengths', []):
                st.markdown(f"• {strength}")
            
            st.subheader("🎯 Specific Tips")
            for tip in feedback.get('specific_tips', []):
                st.markdown(f"• {tip}")
        
        with col2:
            st.subheader("📈 Areas for Improvement")
            for area in feedback.get('areas_for_improvement', []):
                st.markdown(f"• {area}")
            
            st.subheader("🔄 Follow-up Questions")
            for question in feedback.get('follow_up_questions', []):
                st.markdown(f"• {question}")
        
        # Sample improvement
        if feedback.get('sample_improvement'):
            with st.expander("✨ Sample Improved Response"):
                st.markdown(feedback['sample_improvement'])
        
        # Body language tips
        if feedback.get('body_language_tips'):
            with st.expander("🤝 Body Language & Presence Tips"):
                for tip in feedback['body_language_tips']:
                    st.markdown(f"• {tip}")
    
    def _display_interview_summary(self, user_profile: Dict[str, Any]):
        """Display complete interview summary"""
        
        responses = st.session_state.get('interview_responses', [])
        
        if not responses:
            return
        
        st.subheader("📊 Interview Summary")
        
        # Calculate overall performance
        total_score = sum(r['feedback']['overall_score'] for r in responses) / len(responses)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🎯 Overall Performance", f"{total_score:.1f}/100")
        with col2:
            st.metric("📝 Questions Answered", len(responses))
        with col3:
            best_score = max(r['feedback']['overall_score'] for r in responses)
            st.metric("🏆 Best Question Score", f"{best_score}/100")
        
        # Question-by-question breakdown
        st.subheader("📋 Question Breakdown")
        
        for i, response_data in enumerate(responses):
            with st.expander(f"Question {i+1} - Score: {response_data['feedback']['overall_score']}/100"):
                st.markdown(f"**Question:** {response_data['question']}")
                st.markdown(f"**Your Response:** {response_data['response'][:200]}...")
                
                feedback = response_data['feedback']
                st.markdown(f"**Strengths:** {', '.join(feedback.get('strengths', [])[:3])}")
                st.markdown(f"**Improvements:** {', '.join(feedback.get('areas_for_improvement', [])[:3])}")
    
    def _end_interview(self, user_profile: Dict[str, Any]):
        """End interview and save results"""
        
        # Save interview session to user profile
        if 'interview_sessions' not in user_profile:
            user_profile['interview_sessions'] = []
        
        interview_session = {
            'config': st.session_state.get('interview_config', {}),
            'responses': st.session_state.get('interview_responses', []),
            'completed_at': datetime.now().isoformat()
        }
        
        user_profile['interview_sessions'].append(interview_session)
        
        # Clear session state
        st.session_state.interview_active = False
        st.session_state.interview_config = {}
        st.session_state.current_question_idx = 0
        st.session_state.interview_responses = []
        
        st.success("Interview session saved! Check Performance Analytics for detailed insights.")
    
    def _display_practice_sessions(self, user_profile: Dict[str, Any]):
        """Display previous practice sessions"""
        
        st.subheader("📊 Previous Practice Sessions")
        
        sessions = user_profile.get('interview_sessions', [])
        
        if not sessions:
            st.info("No practice sessions yet. Start your first mock interview!")
            return
        
        for i, session in enumerate(reversed(sessions[-10:])):  # Show last 10 sessions
            config = session.get('config', {})
            responses = session.get('responses', [])
            
            if responses:
                avg_score = sum(r['feedback']['overall_score'] for r in responses) / len(responses)
            else:
                avg_score = 0
            
            with st.expander(f"Session {len(sessions)-i} - {config.get('industry', 'General')} - {avg_score:.1f}/100"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Date:** {session.get('completed_at', 'Unknown')[:10]}")
                    st.markdown(f"**Type:** {config.get('type', 'Unknown')}")
                    st.markdown(f"**Industry:** {config.get('industry', 'General')}")
                    st.markdown(f"**Questions:** {len(responses)}")
                
                with col2:
                    st.markdown(f"**Average Score:** {avg_score:.1f}/100")
                    st.markdown(f"**Difficulty:** {config.get('difficulty', 'Unknown')}")
                    if config.get('company_name'):
                        st.markdown(f"**Company:** {config['company_name']}")
                
                if st.button(f"📊 View Details", key=f"session_{i}"):
                    # Display detailed session analysis
                    self._display_session_details(session)
    
    def _display_interview_tips(self):
        """Display interview tips and best practices"""
        
        st.subheader("💡 Interview Tips & Best Practices")
        
        tips_categories = {
            "🎯 Before the Interview": [
                "Research the company, its values, recent news, and key employees",
                "Review the job description and match your experience to requirements",
                "Prepare 5-7 specific examples using the STAR method",
                "Practice common questions out loud, not just in your head",
                "Prepare thoughtful questions to ask the interviewer",
                "Test your technology for video interviews"
            ],
            "🗣️ During the Interview": [
                "Start with a confident handshake and eye contact",
                "Listen carefully and ask clarifying questions if needed",
                "Use the STAR method for behavioral questions",
                "Provide specific examples with quantifiable results",
                "Show enthusiasm and genuine interest in the role",
                "Take notes during the interview"
            ],
            "📞 For Phone/Video Interviews": [
                "Find a quiet, well-lit space with good internet",
                "Test your camera, microphone, and interview platform beforehand",
                "Dress professionally even for phone interviews",
                "Keep water, notes, and resume nearby",
                "Look at the camera, not the screen, when speaking",
                "Have a backup plan if technology fails"
            ],
            "🔧 Technical Interviews": [
                "Think out loud and explain your reasoning process",
                "Ask clarifying questions about requirements",
                "Start with a simple solution, then optimize",
                "Write clean, readable code with good variable names",
                "Test your solution with edge cases",
                "Don't be afraid to admit when you don't know something"
            ],
            "❓ Great Questions to Ask": [
                "What does success look like in this role after 90 days?",
                "What are the biggest challenges facing the team right now?",
                "How does this role contribute to the company's goals?",
                "What opportunities are there for professional development?",
                "Can you tell me about the team I'd be working with?",
                "What do you enjoy most about working here?"
            ]
        }
        
        for category, tips in tips_categories.items():
            with st.expander(category, expanded=False):
                for tip in tips:
                    st.markdown(f"• {tip}")
        
        # STAR method explanation
        with st.expander("⭐ The STAR Method", expanded=True):
            st.markdown("""
            **STAR** is a structured approach to answering behavioral interview questions:
            
            - **Situation**: Set the context and background
            - **Task**: Explain what you needed to accomplish
            - **Action**: Describe what you specifically did
            - **Result**: Share the outcome and what you learned
            
            **Example:**
            - *Situation*: "In my previous role as a project manager, our team was behind schedule on a critical client deliverable..."
            - *Task*: "I needed to find a way to get back on track without compromising quality..."
            - *Action*: "I organized daily stand-ups, redistributed tasks based on team strengths, and negotiated a revised timeline with the client..."
            - *Result*: "We delivered the project only 3 days late instead of 2 weeks, and the client was satisfied with our communication throughout the process."
            """)
    
    def _display_analytics(self, user_profile: Dict[str, Any]):
        """Display performance analytics"""
        
        st.subheader("🏆 Performance Analytics")
        
        sessions = user_profile.get('interview_sessions', [])
        
        if not sessions:
            st.info("Complete some mock interviews to see your analytics!")
            return
        
        # Overall statistics
        all_scores = []
        question_types = {}
        industries = {}
        
        for session in sessions:
            responses = session.get('responses', [])
            config = session.get('config', {})
            
            for response in responses:
                score = response['feedback']['overall_score']
                all_scores.append(score)
                
                # Track by industry
                industry = config.get('industry', 'General')
                if industry not in industries:
                    industries[industry] = []
                industries[industry].append(score)
        
        if all_scores:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Average Score", f"{sum(all_scores)/len(all_scores):.1f}/100")
            with col2:
                st.metric("🏆 Best Score", f"{max(all_scores)}/100")
            with col3:
                st.metric("📈 Improvement", f"+{(all_scores[-5:] and sum(all_scores[-5:])/len(all_scores[-5:]) or 0) - (all_scores[:5] and sum(all_scores[:5])/len(all_scores[:5]) or 0):.1f}")
            with col4:
                st.metric("🎯 Sessions", len(sessions))
            
            # Performance by industry
            if industries:
                st.subheader("📊 Performance by Industry")
                
                for industry, scores in industries.items():
                    avg_score = sum(scores) / len(scores)
                    st.markdown(f"**{industry}**: {avg_score:.1f}/100 (based on {len(scores)} questions)")
            
            # Improvement recommendations
            st.subheader("💡 Personalized Recommendations")
            
            recent_scores = all_scores[-10:] if len(all_scores) >= 10 else all_scores
            avg_recent = sum(recent_scores) / len(recent_scores)
            
            if avg_recent < 60:
                st.markdown("🎯 **Focus Areas:**")
                st.markdown("• Practice the STAR method for behavioral questions")
                st.markdown("• Work on providing more specific examples")
                st.markdown("• Practice common interview questions daily")
            elif avg_recent < 80:
                st.markdown("🎯 **Next Level:**")
                st.markdown("• Add more quantifiable results to your stories")
                st.markdown("• Practice industry-specific technical questions")
                st.markdown("• Work on confident delivery and body language")
            else:
                st.markdown("🎯 **Advanced Practice:**")
                st.markdown("• Focus on executive-level questions")
                st.markdown("• Practice case study and strategic thinking questions")
                st.markdown("• Work on asking insightful questions to interviewers")
