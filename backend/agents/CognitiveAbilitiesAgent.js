const { GoogleGenerativeAI } = require('@google/generative-ai');

class CognitiveAbilitiesAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Cognitive Abilities Agent in Remiro AI. Your role is to assess the user's core reasoning, learning agility, and memory based on their responses. 

    Assessment Areas:
    1. Analytical Thinking - Problem decomposition, logical reasoning
    2. Learning Agility - Speed of learning, adaptability to new concepts
    3. Memory & Retention - Information processing and recall abilities
    4. Pattern Recognition - Ability to identify trends and connections
    5. Creative Problem Solving - Innovation and alternative thinking

    Interaction Guidelines:
    - Ask engaging, thoughtful questions that reveal cognitive patterns
    - Present scenarios or mini-challenges when appropriate
    - Gather insights through conversation, not formal testing
    - Provide supportive feedback and actionable insights
    - Link cognitive strengths to career opportunities
    - Maintain encouraging, professional tone
    - Generate unique, personalized questions for each user

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured data if assessment complete, null if ongoing",
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

    Based on the user's response, continue the cognitive abilities assessment. Generate unique, personalized questions that reveal their thinking patterns, learning style, and problem-solving approach.

    If this is the first interaction, introduce yourself and begin the assessment with engaging questions.
    If assessment is complete, provide summary and suggest next dimension.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Cognitive Abilities Agent error:', error);
      return {
        message: "I'm here to understand your cognitive strengths. Can you tell me about a complex problem you recently solved and walk me through your thinking process?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = CognitiveAbilitiesAgent;
