const { GoogleGenerativeAI } = require('@google/generative-ai');

class InterestsAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Interests Agent. Use conversational questions, mapping the user's genuine interests to vocational categories. Translate this into concrete fields or industries.

    Interest Categories:
    1. Subject Interests - What topics fascinate them
    2. Activity Preferences - Types of work they enjoy doing
    3. Industry Curiosity - Sectors that capture their attention
    4. Problem Areas - Issues they care about solving
    5. Hobby Connections - Personal interests that could become careers

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured interests profile if complete, null if ongoing",
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

    Continue the interests assessment with engaging questions about their passions and curiosities.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Interests Agent error:', error);
      return {
        message: "Let's explore what genuinely interests you. What topics or activities do you find yourself naturally drawn to? What kind of problems or challenges excite you to work on?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = InterestsAgent;
