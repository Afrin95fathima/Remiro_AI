const { GoogleGenerativeAI } = require('@google/generative-ai');

class LearningPreferencesAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Learning Preferences Agent. Explore how the user best acquires new knowledge: visually, hands-on, collaboratively, etc. Suggest learning pathways that align.

    Learning Style Areas:
    1. Learning Modality - Visual, auditory, kinesthetic preferences
    2. Pace & Structure - Self-paced vs. structured, intensive vs. gradual
    3. Social Learning - Individual vs. group learning preferences
    4. Feedback Style - How they prefer to receive guidance
    5. Content Format - Books, videos, practice, mentorship

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured learning preferences if complete, null if ongoing",
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

    Continue the learning preferences assessment with questions about how they best acquire new skills.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Learning Preferences Agent error:', error);
      return {
        message: "Let's understand how you learn best. Do you prefer learning through reading, watching videos, hands-on practice, or working with others? What's your ideal learning environment?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = LearningPreferencesAgent;
