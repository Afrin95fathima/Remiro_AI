const { GoogleGenerativeAI } = require('@google/generative-ai');

class PersonalityAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Personality Agent, adept at validated models like Big Five (OCEAN). Your role is to guide users through relevant questions, interpret results, and link personality traits to suitable career paths.

    Big Five Dimensions to Assess:
    1. Openness - Creativity, curiosity, openness to experience
    2. Conscientiousness - Organization, discipline, goal-oriented behavior
    3. Extraversion - Social energy, assertiveness, positive emotions
    4. Agreeableness - Cooperation, trust, empathy
    5. Neuroticism - Emotional stability, stress management

    Assessment Approach:
    - Use conversational questions rather than formal inventory
    - Explore behavioral patterns and preferences
    - Ask about social situations, work styles, stress responses
    - Generate unique scenarios for each user
    - Link traits to career environments and roles
    - Provide positive, constructive insights

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured personality profile if complete, null if ongoing",
      "assessmentComplete": true/false,
      "nextDimension": "suggested next assessment area"
    }
    `;
  }

  async processInteraction(message, userContext) {
    const prompt = `
    ${this.systemPrompt}

    User Context: ${JSON.stringify(userContext.profile, null, 2)}
    User Message: "${message}"

    Continue the personality assessment using the Big Five framework. Create engaging, personalized questions that reveal the user's personality traits and behavioral patterns.

    Generate unique scenarios and questions tailored to this specific user based on their previous responses.
    Focus on understanding their natural preferences and tendencies.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Personality Agent error:', error);
      return {
        message: "I'd like to understand your personality traits to match you with suitable career environments. How do you typically respond when facing a challenging deadline - do you thrive under pressure or prefer to plan well ahead?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = PersonalityAgent;
