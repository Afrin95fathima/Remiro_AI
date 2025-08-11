import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaRobot, FaUser } from 'react-icons/fa';
import api from '../services/api';

const WelcomeContainer = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
`;

const WelcomeCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 60px 40px;
  max-width: 600px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const Logo = styled(motion.div)`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
`;

const LogoIcon = styled(FaRobot)`
  font-size: 3rem;
  color: #667eea;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  color: #4a5568;
  margin-bottom: 40px;
  line-height: 1.6;
`;

const InputSection = styled.div`
  margin-bottom: 30px;
`;

const InputLabel = styled.label`
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 10px;
  text-align: left;
`;

const NameInput = styled.input`
  width: 100%;
  padding: 15px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1.1rem;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
  background: white;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const StartButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const Features = styled.div`
  margin-top: 40px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  text-align: left;
`;

const Feature = styled.div`
  background: rgba(102, 126, 234, 0.1);
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
`;

const FeatureTitle = styled.h3`
  font-size: 0.9rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 5px;
`;

const FeatureDesc = styled.p`
  font-size: 0.8rem;
  color: #4a5568;
  line-height: 1.4;
`;

const ErrorMessage = styled.div`
  background: #fed7d7;
  color: #c53030;
  padding: 10px 15px;
  border-radius: 8px;
  margin-top: 15px;
  font-size: 0.9rem;
`;

const WelcomeScreen = ({ onUserRegistered, isLoading, setIsLoading }) => {
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!name.trim()) {
      setError('Please enter your name to continue');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await api.registerUser(name.trim());
      onUserRegistered(response);
    } catch (err) {
      setError('Failed to register. Please try again.');
      console.error('Registration error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <WelcomeContainer>
      <WelcomeCard
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Logo
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
        >
          <LogoIcon />
          <Title>Remiro AI</Title>
        </Logo>
        
        <Subtitle>
          Your Career Counsellor
          <br />
          Discover your ideal career path through comprehensive 12-dimensional assessment
        </Subtitle>

        <form onSubmit={handleSubmit}>
          <InputSection>
            <InputLabel>Enter your name to begin your career journey</InputLabel>
            <NameInput
              type="text"
              placeholder="Your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={isLoading}
            />
          </InputSection>

          <StartButton
            type="submit"
            disabled={isLoading || !name.trim()}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <FaUser />
            {isLoading ? 'Starting Your Journey...' : 'Begin Assessment'}
          </StartButton>

          {error && <ErrorMessage>{error}</ErrorMessage>}
        </form>

        <Features>
          <Feature>
            <FeatureTitle>12D Assessment</FeatureTitle>
            <FeatureDesc>Comprehensive evaluation across 12 career dimensions</FeatureDesc>
          </Feature>
          <Feature>
            <FeatureTitle>AI-Powered</FeatureTitle>
            <FeatureDesc>Personalized guidance using advanced AI agents</FeatureDesc>
          </Feature>
          <Feature>
            <FeatureTitle>Career Matching</FeatureTitle>
            <FeatureDesc>Find careers that align with your unique profile</FeatureDesc>
          </Feature>
        </Features>
      </WelcomeCard>
    </WelcomeContainer>
  );
};

export default WelcomeScreen;
