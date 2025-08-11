# Remiro AI Development Guidelines

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Python-based project for Remiro AI, a 12D career counselling multi-agent chatbot system using LangChain, LangGraph, and Streamlit.

## Architecture
- **Backend**: Python with LangChain/LangGraph multi-agent system using Google Gemini 2.0 Flash API
- **Frontend**: Streamlit web interface with professional UI components
- **Storage**: Local file system for user data and conversation history
- **AI**: 12 specialized agents + 1 master agent orchestrated through LangGraph workflow

## Key Components

### Agent System
- Each agent is a specialized Python class with `process_interaction` method
- Master agent orchestrates and routes conversations using LangGraph
- All agents use Google Gemini 2.0 Flash API for dynamic responses
- User data managed through UserManager utility class

### Streamlit UI
- Professional, modern interface with custom CSS styling
- Real-time chat interface with agent identification
- Progress tracking for 12-dimensional assessment
- Responsive design with sidebar navigation and dashboard views

## Development Guidelines

### Code Style
- Use Python 3.8+ features and async/await where appropriate
- Follow PEP 8 style guidelines with type hints
- Implement proper error handling in all functions
- Use Pydantic models for data validation and structure
- Add docstrings for all classes and methods

### Agent Development
- Each agent should inherit from base pattern and use consistent JSON responses
- Maintain professional, empathetic tone (no emojis)
- Structure responses with required fields: message, assessment_data, assessment_complete
- Include assessment data when evaluation is complete
- Generate unique, personalized questions for each user

### Data Management
- User folders created automatically with sanitized names + UUID
- All conversations stored in session JSON files
- Profile data tracks assessment completion across 12 dimensions
- Implement proper error handling for file operations
- Use Pydantic models for type safety and validation

### LangGraph Integration
- Use StateGraph for workflow orchestration
- Implement proper state transitions between agents
- Handle routing decisions through master agent
- Maintain conversation context and user profile state

### UI/UX Requirements
- Professional, trustworthy Streamlit design
- Distinct visual identity for each agent type
- Progress indicators for assessment journey
- Smooth state management and error handling
- Responsive layout with clear navigation

## Testing
- Test all agent interactions thoroughly
- Verify data persistence across sessions
- Check error handling scenarios
- Validate API integration with proper keys
- Test LangGraph workflow state transitions

## Environment Setup
- Requires valid Google Gemini 2.0 Flash API key
- Local development with Streamlit hot reload
- Virtual environment with all dependencies from requirements.txt
