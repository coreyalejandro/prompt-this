import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [progress, setProgress] = useState({
    completedExercises: [],
    completedTutorials: []
  });

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem('prompt_this_user');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(userData);
      setIsAuthenticated(true);
       fetchProgress(userData.id);
    }
  }, []);

  const generateUserId = () => {
    return 'user_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
  };

  const login = (username) => {
    const userData = {
      id: generateUserId(),
      username: username || 'Anonymous User',
      createdAt: new Date().toISOString()
    };
    
    setUser(userData);
    setIsAuthenticated(true);
    localStorage.setItem('prompt_this_user', JSON.stringify(userData));

    fetchProgress(userData.id);

    return userData;
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('prompt_this_user');
    setProgress({ completedExercises: [], completedTutorials: [] });
  };

  const fetchProgress = async (userId) => {
    try {
      const response = await axios.get(`${API}/user-progress/${userId}`);
      setProgress(response.data);
    } catch (error) {
      if (error.response && error.response.status === 404) {
        const newProgress = {
          user_id: userId,
          completedExercises: [],
          completedTutorials: []
        };
        await axios.post(`${API}/user-progress`, newProgress);
        setProgress(newProgress);
      } else {
        console.error('Error fetching progress:', error);
      }
    }
  };

  const updateProgress = async (updates) => {
    const updated = { ...progress, ...updates };
    setProgress(updated);
    if (user) {
      try {
        await axios.put(`${API}/user-progress/${user.id}`, {
          user_id: user.id,
          ...updated
        });
      } catch (error) {
        console.error('Error updating progress:', error);
      }
    }
  };

  const completeExercise = (exerciseId) => {
    if (progress.completedExercises.includes(exerciseId)) return;
    updateProgress({
      completedExercises: [...progress.completedExercises, exerciseId]
    });
  };

  const completeTutorial = (tutorialId) => {
    if (progress.completedTutorials.includes(tutorialId)) return;
    updateProgress({
      completedTutorials: [...progress.completedTutorials, tutorialId]
    });
  };

  const value = {
    user,
    isAuthenticated,
    progress,
    login,
    logout,
    completeExercise,
    completeTutorial
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};