    def generate_synchronous_response(
        self, 
        user_input: str, 
        user_profile: Dict[str, Any], 
        conversation_history: List[Dict] = None
    ) -> Dict[str, Any]:
        """Pure synchronous response generation without async dependencies"""
        
        user_name = user_profile.get('name', 'there')
        user_input_lower = user_input.lower()
        
        # Analyze conversation context
        has_assessment_data = any(
            user_profile.get(key, {}).get('assessment_complete', False)
            for key in ['interests', 'skills', 'personality', 'aspirations', 'motivations_values']
        )
        
        question_count = len([msg for msg in (conversation_history or []) if msg.get('role') == 'assistant'])
        
        # Smart response routing based on input content
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "start", "begin"]):
            return {
                'success': True,
                'message': f"Hello {user_name}! 👋 Welcome to your personal AI career counselor! I'm here to help you navigate your professional journey with personalized insights and guidance.\n\nI can assist you with:\n• **Career exploration** and path planning\n• **Skills assessment** and development\n• **Interview preparation** and strategies\n• **Industry insights** and trends\n• **Professional growth** planning\n\nWhat brings you here today? Are you exploring new career opportunities, planning a transition, or looking for general career guidance?",
                'action_type': 'greeting',
                'needs_assessment': False
            }
            
        elif any(word in user_input_lower for word in ["career", "guidance", "advice", "path", "direction"]):
            if has_assessment_data:
                return {
                    'success': True,
                    'message': f"Based on your profile, {user_name}, I can see you've made great progress with your career assessment! Let me provide some personalized insights:\n\n🎯 **Your Career Direction**: Your interests and skills suggest strong potential in areas that match your personality and aspirations.\n\n💡 **Key Recommendations**:\n• Focus on roles that align with your core strengths\n• Consider industries that match your interests\n• Develop skills that complement your natural abilities\n\nWhat specific aspect of your career path would you like to explore further? I can help you with job search strategies, skill development plans, or industry insights.",
                    'action_type': 'personalized_guidance',
                    'needs_assessment': False
                }
            else:
                return {
                    'success': True,
                    'message': f"I'd love to help you with career guidance, {user_name}! 🎯 To provide the most personalized and valuable insights, I recommend starting with our comprehensive career assessment.\n\nOur assessment covers 12 key dimensions:\n• **Interests & Passions** - What truly motivates you\n• **Skills & Abilities** - Your current strengths\n• **Personality** - How you work best\n• **Aspirations** - Your career goals and dreams\n• **Values** - What matters most to you\n\n...and 7 more important areas!\n\nThis helps me understand your unique profile and provide tailored career recommendations. Would you like to start with the assessment, or do you have specific questions I can help with right now?",
                    'action_type': 'assessment_invitation',
                    'needs_assessment': True
                }
                
        elif any(word in user_input_lower for word in ["ai", "artificial intelligence", "machine learning", "ml", "data science"]):
            return {
                'success': True,
                'message': f"Excellent choice, {user_name}! 🤖 AI and machine learning are among the most exciting and fastest-growing fields today.\n\n**🚀 Why AI/ML is Great:**\n• High demand across all industries\n• Excellent salary potential ($120K-$300K+)\n• Continuous learning and innovation\n• Solving real-world problems\n\n**💼 Career Paths:**\n• **ML Engineer** - Building and deploying models\n• **Data Scientist** - Extracting insights from data\n• **AI Researcher** - Advancing the field\n• **AI Product Manager** - Bridging tech and business\n\n**🛠️ Key Skills to Develop:**\n• Programming: Python, R, SQL\n• Math: Statistics, Linear Algebra\n• Tools: TensorFlow, PyTorch, Pandas\n• Soft Skills: Problem-solving, Communication\n\nWhat's your current background? Are you starting fresh or transitioning from another field?",
                'action_type': 'field_guidance',
                'needs_assessment': True
            }
            
        elif any(word in user_input_lower for word in ["interview", "prep", "preparation", "job search"]):
            return {
                'success': True,
                'message': f"Great question, {user_name}! 💼 Interview preparation is crucial for career success. Here's a comprehensive approach:\n\n**🎯 Interview Preparation Strategy:**\n\n**1. Research Phase:**\n• Company background and values\n• Role requirements and expectations\n• Industry trends and challenges\n\n**2. Practice Common Questions:**\n• \"Tell me about yourself\"\n• \"Why are you interested in this role?\"\n• \"What are your strengths/weaknesses?\"\n\n**3. Behavioral Questions (STAR Method):**\n• Situation, Task, Action, Result\n• Prepare 5-7 strong examples\n\n**4. Technical Preparation:**\n• Review relevant skills and concepts\n• Practice coding/technical problems if applicable\n\n**5. Questions to Ask:**\n• Team dynamics and culture\n• Growth opportunities\n• Challenges facing the role\n\nWhat type of role are you preparing for? I can provide more specific guidance!",
                'action_type': 'interview_guidance',
                'needs_assessment': False
            }
            
        elif question_count >= 3 and not has_assessment_data:
            return {
                'success': True,
                'message': f"I really enjoy our conversation, {user_name}! 😊 Based on our discussion, I think you'd benefit greatly from our comprehensive 12-dimensional career assessment.\n\nThe assessment will help us:\n• **Identify** your unique strengths and interests\n• **Explore** career paths that truly fit you\n• **Create** a personalized development plan\n• **Uncover** opportunities you might not have considered\n\nIt's designed to be engaging and insightful, not just another quiz! Each dimension reveals important aspects of your professional identity.\n\nReady to discover your ideal career path? Let's start with the assessment! 🚀",
                'action_type': 'assessment_transition',
                'needs_assessment': True
            }
            
        else:
            # General conversational response
            return {
                'success': True,
                'message': f"That's an interesting point, {user_name}! I appreciate you sharing that with me. As your AI career counselor, I'm here to help you explore any career-related questions or challenges you might have.\n\nIs there a particular aspect of your professional journey you'd like to discuss? Whether it's exploring new opportunities, developing skills, planning a career change, or preparing for interviews - I'm here to support you! 🌟",
                'action_type': 'general_response',
                'needs_assessment': False
            }
