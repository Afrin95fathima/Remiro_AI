import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import AgentAvatar from './AgentAvatar';

const ProgressContainer = styled.div`
  margin-top: 20px;
`;

const ProgressHeader = styled.h4`
  font-size: 0.9rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 15px;
`;

const DimensionsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const DimensionItem = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  background: ${props => props.isActive ? 'rgba(102, 126, 234, 0.1)' : 'transparent'};
  border-left: 3px solid ${props => props.isCompleted ? '#48bb78' : props.isActive ? '#667eea' : '#e2e8f0'};
  transition: all 0.3s ease;
`;

const DimensionIcon = styled.div`
  color: ${props => props.isCompleted ? '#48bb78' : props.isActive ? '#667eea' : '#a0aec0'};
`;

const DimensionName = styled.span`
  font-size: 0.8rem;
  font-weight: 500;
  color: ${props => props.isCompleted ? '#2d3748' : props.isActive ? '#2d3748' : '#718096'};
  text-transform: capitalize;
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  margin-top: 15px;
  overflow: hidden;
`;

const ProgressFill = styled(motion.div)`
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 3px;
`;

const ProgressText = styled.p`
  font-size: 0.75rem;
  color: #4a5568;
  margin-top: 8px;
  text-align: center;
`;

const dimensions = [
  { key: 'cognitiveAbilities', name: 'Cognitive Abilities' },
  { key: 'personality', name: 'Personality' },
  { key: 'emotionalIntelligence', name: 'Emotional Intelligence' },
  { key: 'physicalContext', name: 'Physical Context' },
  { key: 'strengthsWeaknesses', name: 'Strengths & Weaknesses' },
  { key: 'skills', name: 'Skills' },
  { key: 'constraints', name: 'Constraints' },
  { key: 'interests', name: 'Interests' },
  { key: 'motivationsValues', name: 'Motivations & Values' },
  { key: 'aspirations', name: 'Aspirations' },
  { key: 'trackRecord', name: 'Track Record' },
  { key: 'learningPreferences', name: 'Learning Preferences' }
];

const ProgressIndicator = ({ messages = [] }) => {
  const getActiveAgent = () => {
    const lastBotMessage = [...messages].reverse().find(m => m.sender === 'bot');
    return lastBotMessage?.agent || 'master';
  };

  const getCompletedDimensions = () => {
    const agentMessages = messages.filter(m => m.sender === 'bot' && m.agent !== 'master');
    const agentCounts = {};
    
    agentMessages.forEach(msg => {
      agentCounts[msg.agent] = (agentCounts[msg.agent] || 0) + 1;
    });
    
    // Consider a dimension completed if there are 3+ interactions
    return Object.keys(agentCounts).filter(agent => agentCounts[agent] >= 3);
  };

  const activeAgent = getActiveAgent();
  const completedDimensions = getCompletedDimensions();
  const progressPercentage = Math.round((completedDimensions.length / dimensions.length) * 100);

  return (
    <ProgressContainer>
      <ProgressHeader>Assessment Progress</ProgressHeader>
      
      <DimensionsList>
        {dimensions.map((dimension, index) => {
          const isCompleted = completedDimensions.includes(dimension.key);
          const isActive = activeAgent === dimension.key;
          
          return (
            <DimensionItem
              key={dimension.key}
              isCompleted={isCompleted}
              isActive={isActive}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <DimensionIcon isCompleted={isCompleted} isActive={isActive}>
                <AgentAvatar agent={dimension.key} size="1rem" />
              </DimensionIcon>
              <DimensionName isCompleted={isCompleted} isActive={isActive}>
                {dimension.name}
              </DimensionName>
            </DimensionItem>
          );
        })}
      </DimensionsList>

      <ProgressBar>
        <ProgressFill
          initial={{ width: 0 }}
          animate={{ width: `${progressPercentage}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </ProgressBar>
      
      <ProgressText>
        {progressPercentage}% Complete ({completedDimensions.length}/{dimensions.length} dimensions)
      </ProgressText>
    </ProgressContainer>
  );
};

export default ProgressIndicator;
