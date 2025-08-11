const { GoogleGenerativeAI } = require('@google/generative-ai');

// Import all specialized agents
const CognitiveAbilitiesAgent = require('./CognitiveAbilitiesAgent');
const PersonalityAgent = require('./PersonalityAgent');
const EmotionalIntelligenceAgent = require('./EmotionalIntelligenceAgent');
const PhysicalContextAgent = require('./PhysicalContextAgent');
const StrengthsWeaknessesAgent = require('./StrengthsWeaknessesAgent');
const SkillsAgent = require('./SkillsAgent');
const ConstraintsAgent = require('./ConstraintsAgent');
const InterestsAgent = require('./InterestsAgent');
const MotivationsValuesAgent = require('./MotivationsValuesAgent');
const AspirationsAgent = require('./AspirationsAgent');
const TrackRecordAgent = require('./TrackRecordAgent');
const LearningPreferencesAgent = require('./LearningPreferencesAgent');

const UserManager = require('../utils/UserManager');

class MasterAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    this.userManager = new UserManager();
    
    // Initialize all specialized agents
    this.agents = {
      cognitiveAbilities: new CognitiveAbilitiesAgent(),
      personality: new PersonalityAgent(),
      emotionalIntelligence: new EmotionalIntelligenceAgent(),
      physicalContext: new PhysicalContextAgent(),
      strengthsWeaknesses: new StrengthsWeaknessesAgent(),
      skills: new SkillsAgent(),
      constraints: new ConstraintsAgent(),
      interests: new InterestsAgent(),
      motivationsValues: new MotivationsValuesAgent(),
      aspirations: new AspirationsAgent(),
      trackRecord: new TrackRecordAgent(),
      learningPreferences: new LearningPreferencesAgent()
    };
    
    this.conversationState = new Map();
  }

  async handleInitialInteraction(message) {
    const nameExtractionPrompt = `
    You are the Master Agent of Remiro AI, the user's career navigation companion. 
    
    The user just sent this message: "${message}"
    
    If the message contains a name or seems like an introduction, extract the name and respond warmly.
    If no name is provided, politely ask for their name to begin the career counselling journey.
    
    Always maintain a professional, supportive tone. You are Remiro AI, their career counsellor.
    
    Respond in this JSON format:
    {
      "requiresName": true/false,
      "extractedName": "name if found, null if not",
      "response": "your response message"
    }
    `;

    try {
      const result = await this.model.generateContent(nameExtractionPrompt);
      const response = JSON.parse(result.response.text());
      
      if (!response.requiresName && response.extractedName) {
        // Create user and return welcome message
        const user = await this.userManager.createUser(response.extractedName);
        return {
          requiresRegistration: false,
          userId: user.userId,
          response: user.message + " To provide you with the most personalized career guidance, I'll be conducting a comprehensive 12-dimensional assessment. Are you ready to begin?"
        };
      } else {
        return {
          requiresRegistration: true,
          response: response.response
        };
      }
    } catch (error) {
      console.error('Initial interaction error:', error);
      return {
        requiresRegistration: true,
        response: "Hello! I'm Remiro AI, your career counsellor. To provide you with personalized career guidance, may I have your name please?"
      };
    }
  }

  async processMessage(message, userId, userContext) {
    try {
      // Determine which agent should handle this interaction
      const agentDecision = await this.determineAgent(message, userContext);
      
      if (agentDecision.agent === 'master') {
        return await this.handleMasterResponse(message, userId, userContext, agentDecision);
      } else {
        return await this.routeToSpecializedAgent(message, userId, userContext, agentDecision);
      }
    } catch (error) {
      console.error('Process message error:', error);
      return {
        response: "I apologize, but I encountered an issue processing your message. Could you please try again?",
        agent: "master",
        error: true
      };
    }
  }

  async determineAgent(message, userContext) {
    const agentSelectionPrompt = `
    You are the Master Agent of Remiro AI. Analyze the user's message and current context to determine which agent should handle the response.

    User Message: "${message}"
    
    User Profile Completeness:
    ${Object.entries(userContext.profile).map(([key, value]) => 
      `${key}: ${value ? 'Completed' : 'Not Started'}`
    ).join('\n')}

    Available Specialized Agents:
    1. cognitiveAbilities - Assess reasoning, learning agility, memory
    2. personality - Big Five personality assessment
    3. emotionalIntelligence - Emotional awareness and regulation
    4. physicalContext - Work environment preferences
    5. strengthsWeaknesses - Energy zones and drain activities
    6. skills - Hard, soft, domain-specific skills inventory
    7. constraints - Geographic, financial, family limitations
    8. interests - Genuine interests mapping to careers
    9. motivationsValues - Core drivers and purpose
    10. aspirations - Long-term goals and lifestyle desires
    11. trackRecord - Past education, projects, work history
    12. learningPreferences - How user best acquires knowledge

    Rules:
    1. Route to master if: general conversation, career recommendations synthesis, progress overview
    2. Route to specialized agent if: user shows readiness for specific assessment
    3. Prioritize incomplete dimensions
    4. Consider user's explicit requests
    5. Follow logical assessment flow

    Respond in JSON format:
    {
      "agent": "agent_name or master",
      "reasoning": "why this agent was selected",
      "priority": "high/medium/low",
      "nextSteps": "suggested next actions"
    }
    `;

    try {
      const result = await this.model.generateContent(agentSelectionPrompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Agent determination error:', error);
      return {
        agent: "master",
        reasoning: "Error in agent selection, defaulting to master",
        priority: "medium",
        nextSteps: "Continue general conversation"
      };
    }
  }

  async handleMasterResponse(message, userId, userContext, agentDecision) {
    const masterPrompt = `
    You are the Master Agent of Remiro AI, the user's career navigation companion. Provide a warm, professional response that builds rapport and trust.

    User Message: "${message}"
    Agent Decision Context: ${JSON.stringify(agentDecision)}
    
    User Profile Status:
    ${Object.entries(userContext.profile).map(([key, value]) => 
      `${key}: ${value ? 'Completed' : 'Pending'}`
    ).join('\n')}

    Your Role:
    - Onboard users warmly, building rapport and trust
    - Ask open-ended questions to explore background and goals
    - Guide users through the 12D assessment journey
    - Synthesize insights from specialized agents
    - Provide career recommendations when assessment is complete
    - Maintain supportive, professional tone throughout

    Guidelines:
    - Be empathetic but professional
    - Ask thoughtful, open-ended questions
    - Suggest next assessment steps when appropriate
    - Validate user's responses and show understanding
    - No emojis, maintain professional tone

    Generate a personalized response that continues the career counselling conversation.
    `;

    try {
      const result = await this.model.generateContent(masterPrompt);
      
      return {
        response: result.response.text(),
        agent: "master",
        nextSteps: agentDecision.nextSteps,
        profileStatus: this.userManager.calculateProfileCompleteness(userContext.profile)
      };
    } catch (error) {
      console.error('Master response error:', error);
      return {
        response: "I understand you're here to explore your career path. Let's continue our conversation. What aspect of your career journey would you like to discuss?",
        agent: "master",
        error: true
      };
    }
  }

  async routeToSpecializedAgent(message, userId, userContext, agentDecision) {
    try {
      const agent = this.agents[agentDecision.agent];
      if (!agent) {
        throw new Error(`Agent ${agentDecision.agent} not found`);
      }

      const response = await agent.processInteraction(message, userContext);
      
      // Update user profile if agent provided assessment data
      if (response.assessmentData) {
        await this.userManager.updateUserProfile(userId, agentDecision.agent, response.assessmentData);
      }

      return {
        response: response.message,
        agent: agentDecision.agent,
        assessmentComplete: response.assessmentComplete || false,
        nextDimension: response.nextDimension || null,
        profileStatus: this.userManager.calculateProfileCompleteness(userContext.profile)
      };
    } catch (error) {
      console.error('Specialized agent error:', error);
      return {
        response: "I apologize for the technical difficulty. Let's continue with a different aspect of your career assessment. What would you like to explore?",
        agent: "master",
        error: true
      };
    }
  }

  async generateCareerRecommendations(userId, userContext) {
    const recommendationPrompt = `
    You are the Master Agent of Remiro AI. Generate comprehensive career recommendations based on the user's complete 12D assessment.

    User Profile:
    ${JSON.stringify(userContext.profile, null, 2)}

    Generate detailed career recommendations including:
    1. Top 5 career paths with explanations
    2. Industries that align with their profile
    3. Specific next steps and action items
    4. Learning and development recommendations
    5. Potential challenges and how to overcome them

    Provide actionable, personalized guidance based on their comprehensive assessment.
    `;

    try {
      const result = await this.model.generateContent(recommendationPrompt);
      return result.response.text();
    } catch (error) {
      console.error('Recommendation generation error:', error);
      return "Based on your assessment, I can see several promising career directions for you. Let's schedule a follow-up session to discuss detailed recommendations.";
    }
  }
}

module.exports = MasterAgent;
