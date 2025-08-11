const { GoogleGenerativeAI } = require('@google/generative-ai');

class TrackRecordAgent {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    this.systemPrompt = `
    You are the Track Record Agent. Assess past education, projects, and work history. Invite users to share accomplishments and milestones, then synthesize a track record for career guidance.

    Track Record Areas:
    1. Educational Background - Degrees, courses, academic achievements
    2. Work Experience - Jobs, internships, volunteer work
    3. Projects & Accomplishments - Significant achievements
    4. Leadership Roles - Management and initiative-taking experience
    5. Patterns & Themes - Common threads in their history

    Always respond in JSON format with:
    {
      "message": "your response to the user",
      "assessmentData": "structured track record if complete, null if ongoing",
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

    Continue the track record assessment with questions about their background and achievements.
    `;

    try {
      const result = await this.model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Track Record Agent error:', error);
      return {
        message: "Let's review your background and accomplishments. Can you share your educational journey, work experience, and any significant projects or achievements you're proud of?",
        assessmentData: null,
        assessmentComplete: false,
        nextDimension: null
      };
    }
  }
}

module.exports = TrackRecordAgent;
