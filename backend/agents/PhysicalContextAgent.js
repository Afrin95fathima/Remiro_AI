const { GoogleGenerativeAI } = require('@google/generative-ai');

class PhysicalContextAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Physical Context Agent. Ask about the user's preferences for remote/onsite work, environment, and physical working conditions. Offer career suggestions matched to their comfort zones.

    Assessment Areas:
    1. Work Location Preferences - Remote, hybrid, onsite
    2. Physical Environment - Indoor/outdoor, office/field, travel requirements
    3. Work Schedule - Traditional hours, flexible, shift work
    4. Physical Demands - Sedentary, active, manual labor tolerance
    5. Sensory Preferences - Noise levels, lighting, space requirements

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured physical context profile if complete, null if ongoing",
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

    Continue the physical context assessment with personalized questions about work environment preferences.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Physical Context Agent error:', error);
      return {
        message: "Let's discuss your ideal work environment. Do you prefer working from home, in a traditional office, or a mix of both? What physical setting helps you be most productive?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = PhysicalContextAgent;
