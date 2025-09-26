# 🚀 Remiro AI - Advanced 12D Career Counselling System

**The most advanced and personalized career assistance platform powered by 12 specialized AI agents**

## 🎯 Overview

Remiro AI is an innovative multi-agent career counseling system that provides comprehensive 12-dimensional assessment and personalized career guidance. Using Google Gemini 2.0 Flash API and advanced LangGraph workflow orchestration, it delivers empathetic, conversational career advice tailored to each individual.

## ✨ Key Features

- **12D Assessment Framework**: Comprehensive evaluation across 12 career dimensions
- **Empathetic AI Conversations**: Emotionally intelligent responses with personalized follow-ups
- **Professional UI**: Modern, clean Streamlit interface with professional styling
- **Comprehensive Career Analysis**: Detailed recommendations, roadmaps, and development plans
- **Persistent Data**: Conversation history and assessment tracking
- **Real-time Progress**: Visual progress indicators and dashboard views

## 🤖 12D Agent System

1. **Personality Agent** - MBTI and personality trait assessment
2. **Skills Agent** - Technical and soft skills evaluation
3. **Interests Agent** - Career interests and passion discovery
4. **Aspirations Agent** - Long-term goals and career vision
5. **Cognitive Abilities Agent** - Problem-solving and analytical skills
6. **Emotional Intelligence Agent** - EQ and interpersonal skills
7. **Learning Preferences Agent** - Preferred learning styles and methods
8. **Motivations & Values Agent** - Core values and motivational drivers
9. **Strengths & Weaknesses Agent** - SWOT analysis for career development
10. **Track Record Agent** - Past achievements and performance patterns
11. **Constraints Agent** - Limitations and constraints analysis
12. **Physical Context Agent** - Location, mobility, and physical considerations

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Google Gemini API Key

### 1. Clone and Install Dependencies
```bash
git clone https://github.com/YourUsername/Remiro_AI.git
cd Remiro_AI
pip install -r requirements.txt
```

### 2. Get Google Gemini API Key
1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create a new API key for Gemini API
3. Copy your API key

### 3. Configure API Key (Choose One Method)

**Method 1: Streamlit Secrets (Recommended)**
1. Edit `.streamlit/secrets.toml`
2. Replace `YOUR_GOOGLE_API_KEY_HERE` with your actual API key:
```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

**Method 2: Environment Variable**
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your_actual_api_key_here"

# Windows Command Prompt
set GOOGLE_API_KEY=your_actual_api_key_here

# Linux/Mac
export GOOGLE_API_KEY=your_actual_api_key_here
```

**Method 3: .env File**
1. Copy `.env.example` to `.env`
2. Replace `YOUR_GOOGLE_API_KEY_HERE` with your actual API key

### 4. Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🎨 Architecture

### Backend Components
- **LangGraph Workflow**: Orchestrates conversation flow between agents
- **State Management**: Pydantic models for type-safe data handling
- **User Management**: Persistent storage for conversations and assessments
- **Agent System**: 12 specialized agents + 1 master orchestrator

### Frontend Components
- **Streamlit Interface**: Professional, responsive web interface
- **Chat System**: Real-time conversation with agent identification
- **Progress Tracking**: Visual assessment completion indicators
- **Dashboard**: Comprehensive career analysis views

## 📁 Project Structure
```
remiro_ai/
├── agents/                 # 12D Agent implementations
├── core/                   # Core system components
│   ├── langgraph_workflow.py
│   ├── state_models.py
│   └── user_manager.py
├── ui/                     # User interface components
├── data/users/            # User conversation storage
├── .streamlit/            # Streamlit configuration
└── app.py                 # Main application
```

## 🚀 Usage

1. **Start Assessment**: Begin your 12-dimensional career journey
2. **Engage with Agents**: Have empathetic conversations with specialized AI agents
3. **Complete Dimensions**: Work through all 12 assessment areas
4. **Receive Analysis**: Get comprehensive career recommendations and roadmaps
5. **Track Progress**: Monitor your assessment completion and development

## 🔧 Troubleshooting

### Common Issues

**API Key Error**: Ensure your Google Gemini API key is properly configured in secrets.toml or environment variables.

**Dependency Issues**: Make sure all packages are installed: `pip install -r requirements.txt`

**Port Conflicts**: If port 8501 is busy, use: `streamlit run app.py --server.port 8502`

## 📊 Features in Detail

### Empathetic AI Conversations
- Emotional tone detection and matching
- Context-aware personalized responses  
- Follow-up questions based on user engagement
- Professional, supportive communication style

### Comprehensive Career Analysis
- Role recommendations with match scores
- Detailed skill development plans
- Career roadmaps with timelines
- Industry insights and trends

### Professional Interface
- Clean, modern design with custom CSS
- Responsive layout for all devices
- Intuitive navigation and progress indicators
- Professional color scheme and typography

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please contact [your-email@example.com] or create an issue in the GitHub repository.

---

**🌟 Transform your career journey with Remiro AI - where advanced AI meets personalized career guidance!**