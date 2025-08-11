const { GoogleGenerativeAI } = require('@google/generative-ai');

class ConstraintsAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Constraints Agent. Explore real-world limitations: geography, financial, family, health, etc. Do so respectfully, suggesting alternatives without judgement.

    Constraint Areas:
    1. Geographic - Location preferences, relocation willingness
    2. Financial - Salary requirements, education costs
    3. Family - Caregiving responsibilities, work-life balance
    4. Time - Availability, scheduling limitations
    5. Personal - Health considerations, other commitments

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured constraints profile if complete, null if ongoing",
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

    Continue the constraints assessment with sensitive, respectful questions about limitations.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Constraints Agent error:', error);
      return {
        message: "Let's discuss any practical considerations that might influence your career choices. Are there geographic preferences, family commitments, or other factors I should be aware of when suggesting career paths?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = ConstraintsAgent;
