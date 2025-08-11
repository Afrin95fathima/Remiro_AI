const { GoogleGenerativeAI } = require('@google/generative-ai');

class EmotionalIntelligenceAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Emotional Intelligence Agent. Evaluate the user's emotional awareness, regulation, and empathy through situational questions. Give supportive, constructive feedback and recommend ways these skills impact the workplace.

    Assessment Areas:
    1. Self-Awareness - Understanding own emotions and triggers
    2. Self-Regulation - Managing emotions and impulses
    3. Empathy - Understanding others' emotions and perspectives
    4. Social Skills - Communication and relationship management
    5. Motivation - Internal drive and resilience

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured EI profile if complete, null if ongoing",
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

    Continue the emotional intelligence assessment with personalized situational questions.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Emotional Intelligence Agent error:', error);
      return {
        message: "Let's explore your emotional intelligence. Describe a time when you had to manage a difficult conversation with a colleague or friend. How did you approach it?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = EmotionalIntelligenceAgent;
