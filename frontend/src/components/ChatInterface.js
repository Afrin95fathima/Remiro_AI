import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FaRobot, FaUser, FaPaperPlane, FaChartBar, FaHome } from 'react-icons/fa';
import { useUser } from '../context/UserContext';
import api from '../services/api';
import AgentAvatar from './AgentAvatar';
import ProgressIndicator from './ProgressIndicator';

const ChatContainer = styled.div`
  height: 100vh;
  display: flex;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const Sidebar = styled.div`
  width: 300px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
`;

const SidebarHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
`;

const UserAvatar = styled.div`
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
`;

const UserName = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
`;

const MainChat = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
`;

const ChatHeader = styled.div`
  padding: 20px 30px;
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: between;
  gap: 15px;
`;

const BotInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
`;

const BotAvatar = styled.div`
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
`;

const BotTitle = styled.div`
  h2 {
    font-size: 1.3rem;
    font-weight: 600;
    color: #2d3748;
    margin: 0 0 5px 0;
  }
  
  p {
    font-size: 0.9rem;
    color: #4a5568;
    margin: 0;
  }
`;

const HeaderActions = styled.div`
  display: flex;
  gap: 10px;
`;

const HeaderButton = styled.button`
  background: transparent;
  border: 2px solid #667eea;
  color: #667eea;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  transition: all 0.3s ease;

  &:hover {
    background: #667eea;
    color: white;
  }
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px 30px;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const MessageBubble = styled(motion.div)`
  display: flex;
  align-items: flex-start;
  gap: 12px;
  ${props => props.isUser && `
    flex-direction: row-reverse;
    text-align: right;
  `}
`;

const MessageAvatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  flex-shrink: 0;
  
  ${props => props.isUser ? `
    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  ` : `
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  `}
`;

const MessageContent = styled.div`
  max-width: 70%;
  background: ${props => props.isUser ? 
    'linear-gradient(135deg, #4299e1 0%, #3182ce 100%)' : 
    'white'
  };
  color: ${props => props.isUser ? 'white' : '#2d3748'};
  padding: 15px 20px;
  border-radius: 18px;
  ${props => props.isUser ? `
    border-bottom-right-radius: 4px;
  ` : `
    border-bottom-left-radius: 4px;
  `}
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  line-height: 1.5;
  white-space: pre-wrap;
`;

const MessageMeta = styled.div`
  font-size: 0.75rem;
  color: ${props => props.isUser ? 'rgba(255,255,255,0.7)' : '#718096'};
  margin-top: 5px;
`;

const InputSection = styled.form`
  padding: 20px 30px;
  background: rgba(255, 255, 255, 0.95);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 15px;
  align-items: flex-end;
`;

const MessageInput = styled.textarea`
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 15px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  resize: none;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const SendButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const TypingIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px 20px;
`;

const TypingDots = styled.div`
  display: flex;
  gap: 4px;
  
  span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #667eea;
    animation: typing 1.4s ease-in-out infinite;
    
    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }

  @keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
  }
`;

const ChatInterface = ({ user, onUserChange }) => {
  const { sessionId, conversationHistory, addMessage } = useUser();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState('master');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (user && user.message) {
      const welcomeMessage = {
        id: Date.now(),
        content: user.message,
        sender: 'bot',
        agent: 'master',
        timestamp: new Date().toISOString()
      };
      setMessages([welcomeMessage]);
      addMessage(welcomeMessage);
    }
  }, [user]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      content: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    addMessage(userMessage);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await api.sendMessage({
        message: inputMessage.trim(),
        userId: user?.userId,
        sessionId
      });

      const botMessage = {
        id: Date.now() + 1,
        content: response.response,
        sender: 'bot',
        agent: response.agent || 'master',
        timestamp: new Date().toISOString(),
        profileStatus: response.profileStatus
      };

      setMessages(prev => [...prev, botMessage]);
      addMessage(botMessage);
      setCurrentAgent(response.agent || 'master');

    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        content: 'I apologize, but I encountered an issue. Please try again.',
        sender: 'bot',
        agent: 'master',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const getInitials = (name) => {
    return name ? name.split(' ').map(n => n[0]).join('').toUpperCase() : 'U';
  };

  return (
    <ChatContainer>
      <Sidebar>
        <SidebarHeader>
          <UserInfo>
            <UserAvatar>
              {getInitials(user?.name)}
            </UserAvatar>
            <UserName>{user?.name}</UserName>
          </UserInfo>
          <ProgressIndicator messages={messages} />
        </SidebarHeader>
      </Sidebar>

      <MainChat>
        <ChatHeader>
          <BotInfo>
            <BotAvatar>
              <FaRobot />
            </BotAvatar>
            <BotTitle>
              <h2>Remiro AI</h2>
              <p>Your Career Counsellor</p>
            </BotTitle>
          </BotInfo>
          <HeaderActions>
            <HeaderButton type="button" onClick={() => window.location.href = '/'}>
              <FaHome />
              Home
            </HeaderButton>
            <HeaderButton type="button">
              <FaChartBar />
              Progress
            </HeaderButton>
          </HeaderActions>
        </ChatHeader>

        <MessagesContainer>
          <AnimatePresence>
            {messages.map((message) => (
              <MessageBubble
                key={message.id}
                isUser={message.sender === 'user'}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <MessageAvatar isUser={message.sender === 'user'}>
                  {message.sender === 'user' ? <FaUser /> : <AgentAvatar agent={message.agent} />}
                </MessageAvatar>
                <div>
                  <MessageContent isUser={message.sender === 'user'}>
                    {message.content}
                  </MessageContent>
                  <MessageMeta isUser={message.sender === 'user'}>
                    {message.agent && message.agent !== 'master' && `${message.agent} • `}
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </MessageMeta>
                </div>
              </MessageBubble>
            ))}
          </AnimatePresence>

          {isLoading && (
            <TypingIndicator
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <MessageAvatar>
                <FaRobot />
              </MessageAvatar>
              <TypingDots>
                <span></span>
                <span></span>
                <span></span>
              </TypingDots>
            </TypingIndicator>
          )}
          
          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputSection onSubmit={handleSubmit}>
          <MessageInput
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share your thoughts and responses..."
            disabled={isLoading}
            rows={1}
          />
          <SendButton
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FaPaperPlane />
          </SendButton>
        </InputSection>
      </MainChat>
    </ChatContainer>
  );
};

export default ChatInterface;
