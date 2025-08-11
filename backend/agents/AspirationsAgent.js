const { GoogleGenerativeAI } = require('@google/generative-ai');

class AspirationsAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Aspirations Agent. Focus on the user's long-term goals and lifestyle desires. Guide visioning exercises, then clearly articulate their north star and future ambitions.

    Aspiration Areas:
    1. Career Vision - Where they see themselves professionally
    2. Lifestyle Goals - How they want to live and work
    3. Impact Aspirations - Legacy and contribution they want to make
    4. Personal Growth - Who they want to become
    5. Life Balance - Integration of work and personal life

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured aspirations profile if complete, null if ongoing",
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

    Continue the aspirations assessment with visioning questions about their future goals.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Aspirations Agent error:', error);
      return {
        message: "Let's envision your future. Where do you see yourself in 5-10 years? What kind of impact do you want to make, and what does your ideal professional life look like?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = AspirationsAgent;
