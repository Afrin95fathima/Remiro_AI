const { GoogleGenerativeAI } = require('@google/generative-ai');

class MotivationsValuesAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Motivations & Values Agent. Uncover what fundamentally drives the user—purpose, recognition, stability, impact, growth, etc. Do so through scenario-based or open-ended queries.

    Core Motivators:
    1. Purpose & Meaning - Making a difference, contributing to society
    2. Recognition & Achievement - Success, accomplishment, status
    3. Security & Stability - Financial security, job stability
    4. Growth & Learning - Personal development, skill building
    5. Autonomy & Freedom - Independence, flexibility, control
    6. Relationships & Connection - Teamwork, helping others

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured motivations profile if complete, null if ongoing",
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

    Continue the motivations and values assessment with deep, meaningful questions about what drives them.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Motivations Values Agent error:', error);
      return {
        message: "Let's explore what truly motivates you. What gives your work meaning? Is it making an impact, achieving recognition, having security, or something else entirely?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = MotivationsValuesAgent;
