const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs-extra');
const path = require('path');
require('dotenv').config();

const MasterAgent = require('./agents/MasterAgent');
const UserManager = require('./utils/UserManager');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Initialize services
const userManager = new UserManager();
const masterAgent = new MasterAgent();

// Routes
app.post('/api/chat', async (req, res) => {
  try {
    const { message, userId, sessionId } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Handle user registration if no userId
    if (!userId) {
      const response = await masterAgent.handleInitialInteraction(message);
      return res.json(response);
    }

    // Get user context
    const userContext = await userManager.getUserContext(userId);
    
    // Process message through master agent
    const response = await masterAgent.processMessage(message, userId, userContext);
    
    // Save conversation
    await userManager.saveConversation(userId, sessionId, {
      timestamp: new Date().toISOString(),
      userMessage: message,
      botResponse: response
    });

    res.json(response);
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/register-user', async (req, res) => {
  try {
    const { name } = req.body;
    
    if (!name) {
      return res.status(400).json({ error: 'Name is required' });
    }

    const user = await userManager.createUser(name);
    res.json(user);
  } catch (error) {
    console.error('User registration error:', error);
    res.status(500).json({ error: 'Failed to register user' });
  }
});

app.get('/api/user/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const userData = await userManager.getUserData(userId);
    res.json(userData);
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({ error: 'User not found' });
  }
});

app.get('/api/user/:userId/summary', async (req, res) => {
  try {
    const { userId } = req.params;
    const summary = await userManager.getUserSummary(userId);
    res.json(summary);
  } catch (error) {
    console.error('Get user summary error:', error);
    res.status(500).json({ error: 'Failed to generate summary' });
  }
});

// Serve static files from React app
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../frontend/build')));
  
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`Remiro AI Server running on port ${PORT}`);
});
