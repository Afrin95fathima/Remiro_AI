const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

class UserManager {
  constructor() {
    this.usersDir = path.join(__dirname, '../data/users');
    this.ensureDataDirectory();
  }

  async ensureDataDirectory() {
    await fs.ensureDir(this.usersDir);
  }

  async createUser(name) {
    const userId = uuidv4();
    const sanitizedName = name.replace(/[^a-zA-Z0-9\s]/g, '').trim();
    const userDir = path.join(this.usersDir, `${sanitizedName}_${userId}`);
    
    await fs.ensureDir(userDir);
    
    const userData = {
      id: userId,
      name: sanitizedName,
      createdAt: new Date().toISOString(),
      profile: {
        cognitiveAbilities: null,
        personality: null,
        emotionalIntelligence: null,
        physicalContext: null,
        strengthsWeaknesses: null,
        skills: null,
        constraints: null,
        interests: null,
        motivationsValues: null,
        aspirations: null,
        trackRecord: null,
        learningPreferences: null
      },
      sessions: []
    };

    await fs.writeJson(path.join(userDir, 'profile.json'), userData, { spaces: 2 });
    
    return {
      userId,
      name: sanitizedName,
      message: `Welcome ${sanitizedName}! I'm Remiro AI, your career counsellor. I'm here to help you discover your ideal career path through a comprehensive 12-dimensional assessment. Let's begin this journey together.`
    };
  }

  async getUserContext(userId) {
    try {
      const userDirs = await fs.readdir(this.usersDir);
      const userDir = userDirs.find(dir => dir.includes(userId));
      
      if (!userDir) {
        throw new Error('User not found');
      }

      const profilePath = path.join(this.usersDir, userDir, 'profile.json');
      return await fs.readJson(profilePath);
    } catch (error) {
      throw new Error(`Failed to get user context: ${error.message}`);
    }
  }

  async updateUserProfile(userId, dimension, data) {
    try {
      const userDirs = await fs.readdir(this.usersDir);
      const userDir = userDirs.find(dir => dir.includes(userId));
      
      if (!userDir) {
        throw new Error('User not found');
      }

      const profilePath = path.join(this.usersDir, userDir, 'profile.json');
      const profile = await fs.readJson(profilePath);
      
      profile.profile[dimension] = data;
      profile.updatedAt = new Date().toISOString();
      
      await fs.writeJson(profilePath, profile, { spaces: 2 });
      return profile;
    } catch (error) {
      throw new Error(`Failed to update user profile: ${error.message}`);
    }
  }

  async saveConversation(userId, sessionId, conversation) {
    try {
      const userDirs = await fs.readdir(this.usersDir);
      const userDir = userDirs.find(dir => dir.includes(userId));
      
      if (!userDir) {
        throw new Error('User not found');
      }

      const sessionsDir = path.join(this.usersDir, userDir, 'sessions');
      await fs.ensureDir(sessionsDir);
      
      const sessionFile = path.join(sessionsDir, `${sessionId || 'default'}.json`);
      
      let sessionData = [];
      if (await fs.pathExists(sessionFile)) {
        sessionData = await fs.readJson(sessionFile);
      }
      
      sessionData.push(conversation);
      await fs.writeJson(sessionFile, sessionData, { spaces: 2 });
      
      return sessionData;
    } catch (error) {
      throw new Error(`Failed to save conversation: ${error.message}`);
    }
  }

  async getUserData(userId) {
    try {
      const userDirs = await fs.readdir(this.usersDir);
      const userDir = userDirs.find(dir => dir.includes(userId));
      
      if (!userDir) {
        throw new Error('User not found');
      }

      const userDirPath = path.join(this.usersDir, userDir);
      const profilePath = path.join(userDirPath, 'profile.json');
      const sessionsDir = path.join(userDirPath, 'sessions');
      
      const profile = await fs.readJson(profilePath);
      
      let sessions = [];
      if (await fs.pathExists(sessionsDir)) {
        const sessionFiles = await fs.readdir(sessionsDir);
        sessions = await Promise.all(
          sessionFiles.map(async (file) => {
            const sessionData = await fs.readJson(path.join(sessionsDir, file));
            return {
              sessionId: file.replace('.json', ''),
              data: sessionData
            };
          })
        );
      }
      
      return {
        profile,
        sessions,
        folderPath: userDirPath
      };
    } catch (error) {
      throw new Error(`Failed to get user data: ${error.message}`);
    }
  }

  async getUserSummary(userId) {
    try {
      const userData = await this.getUserData(userId);
      const { profile, sessions } = userData;
      
      const summary = {
        user: {
          name: profile.name,
          createdAt: profile.createdAt,
          totalSessions: sessions.length
        },
        profileCompleteness: this.calculateProfileCompleteness(profile.profile),
        dimensionsAssessed: this.getAssessedDimensions(profile.profile),
        conversationSummary: this.generateConversationSummary(sessions),
        recommendations: this.generateRecommendations(profile.profile)
      };
      
      return summary;
    } catch (error) {
      throw new Error(`Failed to generate user summary: ${error.message}`);
    }
  }

  calculateProfileCompleteness(profile) {
    const totalDimensions = Object.keys(profile).length;
    const completedDimensions = Object.values(profile).filter(val => val !== null).length;
    return Math.round((completedDimensions / totalDimensions) * 100);
  }

  getAssessedDimensions(profile) {
    return Object.entries(profile)
      .filter(([key, value]) => value !== null)
      .map(([key]) => key);
  }

  generateConversationSummary(sessions) {
    const totalMessages = sessions.reduce((count, session) => count + session.data.length, 0);
    const lastSession = sessions[sessions.length - 1];
    
    return {
      totalMessages,
      lastActivity: lastSession ? lastSession.data[lastSession.data.length - 1].timestamp : null
    };
  }

  generateRecommendations(profile) {
    const recommendations = [];
    
    Object.entries(profile).forEach(([dimension, data]) => {
      if (data === null) {
        recommendations.push(`Complete ${dimension} assessment for better career guidance`);
      }
    });
    
    if (recommendations.length === 0) {
      recommendations.push('Profile complete! Ready for comprehensive career recommendations');
    }
    
    return recommendations;
  }
}

module.exports = UserManager;
