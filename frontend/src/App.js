import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import ChatInterface from './components/ChatInterface';
import WelcomeScreen from './components/WelcomeScreen';
import UserDashboard from './components/UserDashboard';
import { UserProvider } from './context/UserContext';

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const App = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <UserProvider>
      <Router>
        <AppContainer>
          <Routes>
            <Route 
              path="/" 
              element={
                currentUser ? (
                  <ChatInterface 
                    user={currentUser} 
                    onUserChange={setCurrentUser}
                  />
                ) : (
                  <WelcomeScreen 
                    onUserRegistered={setCurrentUser}
                    isLoading={isLoading}
                    setIsLoading={setIsLoading}
                  />
                )
              } 
            />
            <Route 
              path="/dashboard/:userId" 
              element={<UserDashboard />} 
            />
            <Route 
              path="/chat" 
              element={
                <ChatInterface 
                  user={currentUser} 
                  onUserChange={setCurrentUser}
                />
              } 
            />
          </Routes>
        </AppContainer>
      </Router>
    </UserProvider>
  );
};

export default App;
