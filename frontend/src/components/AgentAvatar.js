import React from 'react';
import { FaBrain, FaUser, FaHeart, FaMapMarkerAlt, FaBalanceScale, 
         FaCogs, FaExclamationTriangle, FaStar, FaFire, FaRocket, 
         FaTrophy, FaGraduationCap, FaRobot } from 'react-icons/fa';

const agentIcons = {
  master: FaRobot,
  cognitiveAbilities: FaBrain,
  personality: FaUser,
  emotionalIntelligence: FaHeart,
  physicalContext: FaMapMarkerAlt,
  strengthsWeaknesses: FaBalanceScale,
  skills: FaCogs,
  constraints: FaExclamationTriangle,
  interests: FaStar,
  motivationsValues: FaFire,
  aspirations: FaRocket,
  trackRecord: FaTrophy,
  learningPreferences: FaGraduationCap
};

const AgentAvatar = ({ agent = 'master', size = '1.2rem' }) => {
  const IconComponent = agentIcons[agent] || agentIcons.master;
  
  return <IconComponent style={{ fontSize: size }} />;
};

export default AgentAvatar;
