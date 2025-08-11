const { GoogleGenerativeAI } = require('@google/generative-ai');

class StrengthsWeaknessesAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Strengths & Weaknesses Agent. Help the user identify activities that energize or drain them. Guide self-reflection using structured questions, then summarize the major 'effort zones'.

    Assessment Areas:
    1. Energy Givers - Activities that naturally energize and motivate
    2. Energy Drains - Tasks that feel exhausting or demotivating
    3. Natural Talents - Innate abilities and strengths
    4. Growth Areas - Skills to develop or improve
    5. Flow States - When they perform at their best

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured strengths/weaknesses profile if complete, null if ongoing",
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

    Continue the strengths and weaknesses assessment with personalized questions about energy patterns.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Strengths Weaknesses Agent error:', error);
      return {
        message: "Let's identify your natural strengths and energy patterns. Think about your typical day - what activities make you feel energized and engaged versus what tasks drain your energy?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = StrengthsWeaknessesAgent;
