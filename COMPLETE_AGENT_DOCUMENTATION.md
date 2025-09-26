# Remiro AI - Complete Agent System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Agent Architecture](#agent-architecture)
3. [Individual Agent Specifications](#individual-agent-specifications)
4. [Master Agent Workflow](#master-agent-workflow)
5. [Logical Flow & State Management](#logical-flow--state-management)
6. [AI Prompts & Templates](#ai-prompts--templates)
7. [Assessment Completion Logic](#assessment-completion-logic)

---

## System Overview

### 🎯 Purpose
Remiro AI is a comprehensive 12-dimensional career counseling system that uses AI-powered agents to assess and guide users through personalized career development.

### 🏗️ Architecture
- **12 Specialized Assessment Agents** - Each focusing on a specific career dimension
- **1 Master Career Agent** - Orchestrates the entire journey and provides insights
- **EnhancedAgent Base Class** - Unified structure for all assessment agents
- **Multi-choice Question System** - Structured assessment with predefined options
- **AI-Powered Analysis** - Uses Google Gemini 2.0 Flash for intelligent responses

### 📊 Assessment Dimensions
1. **Personality** - Work style and natural preferences
2. **Interests** - What captivates and motivates the user
3. **Aspirations** - Career dreams and future vision
4. **Skills** - Current abilities and competencies
5. **Motivations & Values** - Core drivers and principles
6. **Cognitive Abilities** - Thinking and problem-solving style
7. **Learning Preferences** - How they process information best
8. **Physical Context** - Ideal work environment and conditions
9. **Strengths & Weaknesses** - Honest self-assessment of capabilities
10. **Emotional Intelligence** - Interpersonal and emotional skills
11. **Track Record** - Past achievements and success patterns
12. **Constraints** - Practical considerations affecting career choices

---

## Agent Architecture

### 🔧 EnhancedAgent Base Class

```python
class EnhancedAgent:
    def __init__(self, llm, agent_name: str, assessment_type: str):
        self.llm = llm
        self.agent_name = agent_name
        self.assessment_type = assessment_type
        self.question_index = 0
        self.user_responses = []
        self.questions_data = self._get_questions_for_type()
```

### 🔄 Core Methods
- `get_questions()` - Returns structured questions for the agent
- `process_interaction()` - Handles user responses and progresses through questions
- `_complete_assessment()` - AI analysis when all questions are answered
- `get_current_question()` - Gets the current question with options

---

## Individual Agent Specifications

### 1. 🧠 Personality Agent
**Purpose**: Explore natural work style and personality preferences
**Agent Name**: "Personality & Work Style Counselor"
**Assessment Type**: "personality"

#### Questions:
1. **Work Preference**: "How do you prefer to work on projects?"
   - Options: Leading teams, Collaborating, Independent work, Mixed approach, Supportive role

2. **Energy Sources**: "What energizes you most at work?"
   - Options: Problem-solving, Relationships, Innovation, Helping others, Goals, Learning

3. **Stress Management**: "How do you handle workplace stress?"
   - Options: Take charge, Seek support, Reflect, Focus control, Use humor, Break tasks

#### AI Analysis Prompt:
```
As an expert Personality & Work Style Counselor, analyze [user]'s responses to complete their personality assessment:
[User responses]
Provide comprehensive assessment with strengths, themes, career implications, and development suggestions.
```

---

### 2. 💡 Interests Agent
**Purpose**: Discover what truly captivates and motivates the user
**Agent Name**: "Career Interests Counselor"
**Assessment Type**: "interests"

#### Questions:
1. **Time Loss Activities**: "Which activities make you lose track of time?"
   - Options: Data analysis, Creating, Helping people, Technology, Building, Teaching, Planning

2. **Fascinating Topics**: "What topics do you find most fascinating?"
   - Options: Science/tech, Arts, Business, Health, Environment, Social issues, History, Psychology

3. **Free Time Preferences**: "In your free time, you're most likely to:"
   - Options: Read/learn, Creative projects, Volunteer, Exercise, Socialize, Study, Travel

#### AI Analysis Prompt:
```
As an expert Career Interests Counselor, analyze [user]'s responses to complete their interests assessment:
[User responses]
Identify key interest patterns, natural inclinations, and how these connect to career opportunities.
```

---

### 3. 🎯 Aspirations Agent
**Purpose**: Explore career dreams and future vision
**Agent Name**: "Career Aspirations Counselor"
**Assessment Type**: "aspirations"

#### Questions:
1. **Career Impact**: "What kind of impact do you want to make in your career?"
   - Options: Global solutions, Help individuals, Build businesses, Advance knowledge, Lead/inspire, Environmental, Cultural

2. **Success Definition**: "What does career success look like to you?"
   - Options: Financial security, Recognition, Work-life balance, Growth, Meaningful work, Creative freedom, Relationships, Goals

3. **10-Year Legacy**: "In 10 years, you'd like to be known for:"
   - Options: Expertise, Leadership, Innovation, Helping others, Building, Social change, Work-life integration

#### AI Analysis Prompt:
```
As an expert Career Aspirations Counselor, analyze [user]'s responses to complete their aspirations assessment:
[User responses]
Identify their vision, ambitions, and how these align with potential career paths.
```

---

### 4. 🛠️ Skills Agent
**Purpose**: Identify superpowers and key capabilities
**Agent Name**: "Skills Assessment Counselor"
**Assessment Type**: "skills"

#### Questions:
1. **Sought-After Skills**: "Which skills do others often come to you for help with?"
   - Options: Problem-solving, Communication, Project management, Creative design, Technical, Teaching, Negotiation, Research

2. **Confident Tasks**: "What types of tasks do you complete most confidently?"
   - Options: Analytical work, Creative projects, People management, Technical implementation, Writing, Sales, Planning, Hands-on building

3. **Proud Achievements**: "Which achievements are you most proud of?"
   - Options: Technical solutions, Team leadership, Original creation, Process improvement, Teaching/mentoring, Relationships, Goal achievement, Community impact

#### AI Analysis Prompt:
```
As an expert Skills Assessment Counselor, analyze [user]'s responses to complete their skills assessment:
[User responses]
Identify their core competencies, natural talents, and skill development opportunities.
```

---

### 5. ⭐ Motivations & Values Agent
**Purpose**: Discover core drivers and what values are most important
**Agent Name**: "Values & Motivations Counselor"
**Assessment Type**: "motivations_values"

#### Questions:
1. **Work Satisfaction**: "What aspects of work give you the most satisfaction?"
   - Options: Problem-solving, Helping others, Creating, Results, Learning, Great people, Impact, Autonomy

2. **Core Values**: "Which values are most important to you in your career?"
   - Options: Integrity, Innovation, Collaboration, Excellence, Service, Growth, Balance, Security, Recognition

3. **Motivation Sources**: "What motivates you to do your best work?"
   - Options: Personal satisfaction, Recognition, Financial rewards, Making difference, Learning, Competition, Team success, Building legacy

#### AI Analysis Prompt:
```
As an expert Values & Motivations Counselor, analyze [user]'s responses to complete their motivations_values assessment:
[User responses]
Identify their core drivers, value system, and how these influence career satisfaction.
```

---

### 6. 🧩 Cognitive Abilities Agent
**Purpose**: Explore thinking and problem-solving style
**Agent Name**: "Cognitive Abilities Counselor"
**Assessment Type**: "cognitive_abilities"

#### Questions:
1. **Problem-Solving Approach**: "When facing a complex problem, you typically:"
   - Options: Break down, Pattern recognition, Brainstorm, Research, Discuss, Think through, Experiment

2. **Information Processing**: "How do you prefer to process information?"
   - Options: Visual diagrams, Written docs, Verbal discussion, Hands-on, Step-by-step, Big picture, Real examples

3. **Natural Thinking**: "What types of thinking come naturally to you?"
   - Options: Logical/analytical, Creative/innovative, Strategic planning, Detail-oriented, Intuitive, Critical evaluation, Holistic systems

#### AI Analysis Prompt:
```
As an expert Cognitive Abilities Counselor, analyze [user]'s responses to complete their cognitive_abilities assessment:
[User responses]
Identify their cognitive strengths, thinking patterns, and optimal intellectual challenges.
```

---

### 7. 📚 Learning Preferences Agent
**Purpose**: Understand how they learn and process information best
**Agent Name**: "Learning Preferences Counselor"
**Assessment Type**: "learning_preferences"

#### Questions:
1. **Learning Methods**: "How do you prefer to learn new skills?"
   - Options: Hands-on practice, Reading, Videos, Structured courses, Mentoring, Group discussions, Trial and error

2. **Learning Environment**: "What learning environment works best for you?"
   - Options: Quiet focused space, Interactive groups, Real-world work, Online flexible, Structured classroom, One-on-one, Conferences

3. **Information Retention**: "How do you retain information best?"
   - Options: Detailed notes, Visual mind maps, Teaching others, Immediate practice, Connecting knowledge, Regular review, Real application

#### AI Analysis Prompt:
```
As an expert Learning Preferences Counselor, analyze [user]'s responses to complete their learning_preferences assessment:
[User responses]
Identify their optimal learning style, development approach, and skill acquisition preferences.
```

---

### 8. 🌍 Physical Context Agent
**Purpose**: Explore ideal work environment and conditions
**Agent Name**: "Work Environment Counselor"
**Assessment Type**: "physical_context"

#### Questions:
1. **Work Environment**: "What work environment helps you do your best work?"
   - Options: Private office, Open collaborative, Home office, Outdoor/natural, High-energy, Calm organized, Varied locations

2. **Work Schedule**: "What work schedule do you prefer?"
   - Options: Traditional 9-5, Flexible hours, Early morning, Evening/night, Compressed week, Project-based, Completely flexible

3. **Physical Productivity**: "What physical aspects are important for your productivity?"
   - Options: Natural lighting, Comfortable seating, Quiet environment, Technology access, Movement space, Temperature control, Colleague proximity, Food access

#### AI Analysis Prompt:
```
As an expert Work Environment Counselor, analyze [user]'s responses to complete their physical_context assessment:
[User responses]
Identify their optimal work environment, schedule preferences, and productivity factors.
```

---

### 9. 💪 Strengths & Weaknesses Agent
**Purpose**: Honest exploration of professional strengths and growth areas
**Agent Name**: "Strengths & Development Counselor"
**Assessment Type**: "strengths_weaknesses"

#### Questions:
1. **Greatest Strengths**: "What do you consider your greatest strengths?"
   - Options: Analytical skills, Communication, Creative thinking, Leadership, Attention to detail, Adaptability, Persistence, Empathy

2. **Development Areas**: "Which areas do you feel you could develop further?"
   - Options: Public speaking, Technical skills, Time management, Networking, Conflict resolution, Strategic thinking, Business acumen, Cross-cultural communication

3. **Self-Improvement**: "How do you typically work on self-improvement?"
   - Options: Formal training, Reading/self-study, Seeking feedback, Finding mentors, Regular practice, Professional groups, Reflection, Goal setting

#### AI Analysis Prompt:
```
As an expert Strengths & Development Counselor, analyze [user]'s responses to complete their strengths_weaknesses assessment:
[User responses]
Identify their key strengths, development opportunities, and growth strategies.
```

---

### 10. ❤️ Emotional Intelligence Agent
**Purpose**: Explore interpersonal skills and emotional awareness
**Agent Name**: "Emotional Intelligence Counselor"
**Assessment Type**: "emotional_intelligence"

#### Questions:
1. **Workplace Relationships**: "How do you typically handle workplace relationships?"
   - Options: Build connections, Professional boundaries, Mediate conflicts, Provide support, Focus on tasks, Adapt to people, Active listening

2. **Emotion Management**: "How do you manage your emotions in challenging situations?"
   - Options: Stay calm, Process first, Express openly, Find solutions, Seek support, Stress techniques, Channel motivation

3. **Understanding Others**: "What's your approach to understanding others?"
   - Options: Ask and listen, Observe non-verbals, Empathize, Consider perspective, Communication style, Notice patterns, Create safe spaces

#### AI Analysis Prompt:
```
As an expert Emotional Intelligence Counselor, analyze [user]'s responses to complete their emotional_intelligence assessment:
[User responses]
Identify their EQ strengths, interpersonal skills, and emotional management capabilities.
```

---

### 11. 🏆 Track Record Agent
**Purpose**: Review accomplishments and success patterns
**Agent Name**: "Achievement & Experience Counselor"
**Assessment Type**: "track_record"

#### Questions:
1. **Proud Achievements**: "What achievements are you most proud of?"
   - Options: Academic accomplishments, Professional recognition, Project contributions, Problem-solving/innovation, Helping/mentoring, Skill mastery, Challenge overcome, Organizational change

2. **Success Patterns**: "What patterns do you see in your successes?"
   - Options: Strong preparation, Persistence, Collaboration, Creative problem-solving, Quality focus, Relationship building, Continuous learning, Calculated risks

3. **Self-Learning**: "What have you learned about yourself from your experiences?"
   - Options: Thrive under pressure, Naturally curious, Help-oriented, Big picture thinking, People-focused, Problem-solving oriented, Resilient, Meaning-motivated

#### AI Analysis Prompt:
```
As an expert Achievement & Experience Counselor, analyze [user]'s responses to complete their track_record assessment:
[User responses]
Identify their success patterns, achievements, and what their track record reveals about their potential.
```

---

### 12. ⚖️ Constraints Agent
**Purpose**: Discuss practical considerations that influence career choices
**Agent Name**: "Practical Considerations Counselor"
**Assessment Type**: "constraints"

#### Questions:
1. **Career Influences**: "Which factors influence your career choices?"
   - Options: Geographic location, Family responsibilities, Financial needs, Work schedule, Health considerations, Educational requirements, Industry stability, Company culture

2. **Non-Negotiables**: "What are your non-negotiable requirements?"
   - Options: Work-life balance, Competitive salary, Advancement opportunities, Meaningful work, Flexibility, Professional development, Supportive environment, Job security

3. **Constraint Navigation**: "How do you typically navigate career constraints?"
   - Options: Creative solutions, Prioritize importance, Gradual progress, Seek guidance, Temporary compromises, Focus on control, Adapt expectations, Find opportunities in limitations

#### AI Analysis Prompt:
```
As an expert Practical Considerations Counselor, analyze [user]'s responses to complete their constraints assessment:
[User responses]
Identify their practical limitations, requirements, and strategies for working within constraints.
```

---

## Master Agent Workflow

### 🎭 Master Career Agent
**Class**: MasterCareerAgent
**Purpose**: Orchestrate the entire career counseling journey

### Core Methods:

#### 1. get_assessment_progress()
**Purpose**: Calculate completion status across all 12 dimensions
```python
def get_assessment_progress(self, user_profile):
    assessments = user_profile.get('assessments', {})
    all_dimensions = [12 dimension list]
    
    completed = [dim for dim in all_dimensions if assessments.get(dim, {}).get('completed', False)]
    remaining = [dim for dim in all_dimensions if dim not in completed]
    
    return {
        "completed": completed,
        "remaining": remaining, 
        "progress_percentage": round((len(completed) / len(all_dimensions)) * 100, 1),
        "total_dimensions": len(all_dimensions)
    }
```

#### 2. get_next_options()
**Purpose**: Determine what assessment options to show user
**Logic Flow**:
- If ≥8 assessments completed → Show "Generate Action Plan"
- Otherwise → Show remaining assessment options
- If ≥3 assessments completed → Add "Get Career Insights" option

#### 3. generate_insights()
**Purpose**: Provide interim insights based on completed assessments
**AI Prompt**:
```
As a Master Career Counselor, provide personalized insights for [user] based on their completed assessments:

Assessment Data: [JSON of completed assessments]
Progress: [X]/12 assessments completed

Provide encouraging insights in JSON format:
{
    "message": "personalized message addressing them by name with insights",
    "key_patterns": ["major patterns emerging from assessments"],
    "career_directions": ["potential career paths based on current data"],
    "next_priorities": ["most important remaining assessments"],
    "confidence_level": "assessment readiness level"
}
```

#### 4. generate_action_plan()
**Purpose**: Create comprehensive career action plan after sufficient assessments
**AI Prompt**:
```
Create a comprehensive career action plan for [user], a [background], based on their assessments:

Assessment Data: [Full JSON of all assessments]

Provide detailed action plan in JSON format:
{
    "message": "personalized welcome message",
    "career_summary": {
        "primary_direction": "main career recommendation",
        "key_strengths": ["top 3-4 strengths"],
        "unique_value": "what makes them uniquely valuable"
    },
    "immediate_actions": [
        {"action": "specific step", "timeline": "timeframe", "why": "importance"}
    ],
    "skill_development": [
        {"skill": "skill to develop", "approach": "how to develop", "timeline": "timeframe"}
    ],
    "career_paths": ["specific career options with explanations"],
    "next_steps": ["immediate actions to take"]
}
```

---

## Logical Flow & State Management

### 🔄 Assessment Flow

#### 1. User Registration
- User provides name and background
- UserManager creates unique user profile with UUID
- Profile stored in `data/users/[name]_[uuid]/profile.json`

#### 2. Dashboard Display
- Master Agent calculates progress across all 12 dimensions
- Shows completed vs remaining assessments
- Provides next step recommendations

#### 3. Agent Selection
- User chooses from available assessment options
- System loads appropriate EnhancedAgent instance
- Agent displays introduction and first question

#### 4. Question Progression
- Agent presents multiple-choice questions sequentially
- User selections stored in agent's response array
- Progress tracked (Question X of Y)

#### 5. Assessment Completion
- When all questions answered, AI analysis triggered
- Assessment data generated and stored
- User profile updated with completion status
- Return to dashboard with progress updated

#### 6. Insights Generation (≥3 completed)
- Master Agent analyzes completed assessments
- Provides interim insights and patterns
- Suggests priority for remaining assessments

#### 7. Action Plan Generation (≥8 completed)
- Comprehensive analysis of all assessment data
- Detailed career recommendations
- Specific action items and development plan

### 📊 State Management

#### Session State Variables:
- `user_profile`: Current user's complete profile data
- `current_agent`: Currently active assessment agent
- `agent_responses`: Temporary storage for current assessment
- `user_manager`: Handles profile persistence

#### Profile Structure:
```json
{
    "name": "User Name",
    "background": "Professional/Student/etc",
    "created_at": "ISO timestamp",
    "assessments": {
        "personality": {
            "completed": true/false,
            "data": { /* assessment results */ },
            "completed_at": "ISO timestamp"
        },
        // ... other 11 assessments
    }
}
```

---

## Assessment Completion Logic

### 🎯 Completion Criteria
- All questions in an assessment must be answered
- AI analysis must be successfully completed
- Assessment data must be stored in user profile
- `completed: true` flag must be set

### 🔄 Progress Calculation
```python
# In MasterCareerAgent.get_assessment_progress()
completed = [dim for dim in all_dimensions 
            if assessments.get(dim, {}).get('completed', False)]
remaining = [dim for dim in all_dimensions if dim not in completed]
progress_percentage = round((len(completed) / len(all_dimensions)) * 100, 1)
```

### 📈 Milestone Triggers
- **3+ Assessments**: "Get Career Insights" option becomes available
- **8+ Assessments**: "Generate Career Action Plan" option becomes available
- **12 Assessments**: Full comprehensive career guidance unlocked

---

## AI Prompts & Templates

### 🤖 Standard Assessment Completion Prompt Template
```
As an expert [Agent Name], analyze [User Name]'s responses to complete their [assessment_type] assessment:

[User Response Summary]

Based on their selected options, provide a comprehensive assessment in JSON format:
{
    "message": "warm, encouraging completion message that celebrates their insights",
    "assessment_data": {
        "summary": "key insights from their selections",
        "strengths": ["specific strengths identified from choices"],
        "themes": ["major patterns from selected options"],
        "career_implications": ["how choices connect to career opportunities"],
        "development_suggestions": ["areas for growth based on responses"]
    },
    "assessment_complete": true
}
```

### 🎯 Response Processing
1. User selections collected throughout assessment
2. Formatted into readable summary for AI
3. AI analyzes patterns and provides structured insights
4. Results stored in user profile with completion timestamp
5. Dashboard updated to reflect new completion status

### 🔄 Error Handling
- JSON parsing failures gracefully handled
- Fallback responses provided if AI unavailable
- Assessment can be retaken if completion fails
- Progress always preserved between sessions

---

## Summary

The Remiro AI system provides a comprehensive, structured approach to career assessment through:

- **12 Specialized Agents** each with 3 carefully crafted questions
- **Unified EnhancedAgent Architecture** ensuring consistency
- **AI-Powered Analysis** providing personalized insights
- **Progressive Revelation** of career guidance based on completion
- **Master Agent Orchestration** managing the entire journey
- **Robust State Management** preserving progress across sessions

This creates a thorough 36-question assessment framework (3 questions × 12 agents) that builds a complete picture of an individual's career profile and provides actionable guidance for their professional development.
