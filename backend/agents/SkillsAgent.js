const { GoogleGenerativeAI } = require('@google/generative-ai');

class SkillsAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Skills Agent. Facilitate a comprehensive inventory of the user's hard, soft, domain-specific, and tool-based skills. Ask for role-specific details, rate proficiency if possible.

    Skill Categories:
    1. Technical/Hard Skills - Programming, certifications, specialized knowledge
    2. Soft Skills - Communication, leadership, teamwork
    3. Domain Expertise - Industry-specific knowledge
    4. Tools & Technologies - Software, platforms, equipment
    5. Language Skills - Communication abilities

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured skills inventory if complete, null if ongoing",
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

    Continue the skills assessment with personalized questions about their capabilities and expertise.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Skills Agent error:', error);
      return {
        message: "Let's catalog your skills and abilities. Can you tell me about your technical skills, software you're proficient with, and any certifications or specialized training you have?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = SkillsAgent;
