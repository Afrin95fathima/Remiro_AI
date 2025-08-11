import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaUser, FaChartLine, FaFileAlt, FaDownload } from 'react-icons/fa';
import api from '../services/api';

const DashboardContainer = styled.div`
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const DashboardCard = styled(motion.div)`
  max-width: 1200px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: between;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e2e8f0;
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
`;

const UserAvatar = styled.div`
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  font-weight: 600;
`;

const UserDetails = styled.div`
  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #2d3748;
    margin: 0 0 10px 0;
  }
  
  p {
    color: #4a5568;
    margin: 0;
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
`;

const StatCard = styled(motion.div)`
  background: white;
  padding: 25px;
  border-radius: 15px;
  border-left: 4px solid #667eea;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
`;

const StatIcon = styled.div`
  color: #667eea;
  font-size: 2rem;
  margin-bottom: 15px;
`;

const StatValue = styled.h3`
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 5px 0;
`;

const StatLabel = styled.p`
  color: #4a5568;
  font-size: 0.9rem;
  margin: 0;
`;

const SectionTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin: 40px 0 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const SummarySection = styled.div`
  background: #f7fafc;
  padding: 25px;
  border-radius: 15px;
  margin-bottom: 30px;
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 1.1rem;
  color: #4a5568;
`;

const ErrorMessage = styled.div`
  background: #fed7d7;
  color: #c53030;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
`;

const UserDashboard = () => {
  const { userId } = useParams();
  const [userData, setUserData] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUserData();
  }, [userId]);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const [userResponse, summaryResponse] = await Promise.all([
        api.getUserData(userId),
        api.getUserSummary(userId)
      ]);
      
      setUserData(userResponse);
      setSummary(summaryResponse);
    } catch (err) {
      setError('Failed to load user data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getInitials = (name) => {
    return name ? name.split(' ').map(n => n[0]).join('').toUpperCase() : 'U';
  };

  if (loading) {
    return (
      <DashboardContainer>
        <DashboardCard
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <LoadingSpinner>Loading user dashboard...</LoadingSpinner>
        </DashboardCard>
      </DashboardContainer>
    );
  }

  if (error) {
    return (
      <DashboardContainer>
        <DashboardCard
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <ErrorMessage>{error}</ErrorMessage>
        </DashboardCard>
      </DashboardContainer>
    );
  }

  return (
    <DashboardContainer>
      <DashboardCard
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Header>
          <UserInfo>
            <UserAvatar>
              {getInitials(userData?.profile?.name)}
            </UserAvatar>
            <UserDetails>
              <h1>{userData?.profile?.name}</h1>
              <p>Career Assessment Dashboard</p>
              <p>Created: {new Date(userData?.profile?.createdAt).toLocaleDateString()}</p>
            </UserDetails>
          </UserInfo>
        </Header>

        <StatsGrid>
          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <StatIcon><FaChartLine /></StatIcon>
            <StatValue>{summary?.profileCompleteness || 0}%</StatValue>
            <StatLabel>Profile Completeness</StatLabel>
          </StatCard>

          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <StatIcon><FaUser /></StatIcon>
            <StatValue>{summary?.dimensionsAssessed?.length || 0}</StatValue>
            <StatLabel>Dimensions Assessed</StatLabel>
          </StatCard>

          <StatCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <StatIcon><FaFileAlt /></StatIcon>
            <StatValue>{summary?.user?.totalSessions || 0}</StatValue>
            <StatLabel>Chat Sessions</StatLabel>
          </StatCard>
        </StatsGrid>

        <SectionTitle>
          <FaFileAlt />
          Assessment Summary
        </SectionTitle>
        
        <SummarySection>
          <h3>Assessed Dimensions:</h3>
          <p>{summary?.dimensionsAssessed?.length > 0 ? 
            summary.dimensionsAssessed.join(', ') : 
            'No dimensions assessed yet'}</p>
          
          <h3>Conversation Summary:</h3>
          <p>Total Messages: {summary?.conversationSummary?.totalMessages || 0}</p>
          {summary?.conversationSummary?.lastActivity && (
            <p>Last Activity: {new Date(summary.conversationSummary.lastActivity).toLocaleString()}</p>
          )}
          
          <h3>Recommendations:</h3>
          <ul>
            {summary?.recommendations?.map((rec, index) => (
              <li key={index}>{rec}</li>
            )) || <li>No recommendations available yet</li>}
          </ul>
        </SummarySection>

        <SectionTitle>
          <FaDownload />
          Data Location
        </SectionTitle>
        
        <SummarySection>
          <p><strong>User Folder:</strong> {userData?.folderPath}</p>
          <p>All conversation data and assessment results are stored locally in this folder.</p>
        </SummarySection>
      </DashboardCard>
    </DashboardContainer>
  );
};

export default UserDashboard;
