import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AuthContext = createContext();
const API_URL = '/api';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [progress, setProgress] = useState({
    completedExercises: [],
    completedTutorials: []
  });

  useEffect(() => {
    const savedUser = localStorage.getItem('prompt_this_user');
    const savedToken = localStorage.getItem('prompt_this_token');
    if (savedUser && savedToken) {
      setUser(JSON.parse(savedUser));
      setToken(savedToken);
      setIsAuthenticated(true);
       fetchProgress(userData.id);
    }
  }, []);

  const login = async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_URL}/token`, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Login failed');
    }
    setUser(data.user);
    setToken(data.access_token);
    setIsAuthenticated(true);
    localStorage.setItem('prompt_this_user', JSON.stringify(data.user));
    localStorage.setItem('prompt_this_token', data.access_token);
    return data.user;
  };

  const signup = async (username, password) => {
    const response = await fetch(`${API_URL}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Signup failed');
    }
    setUser(data.user);
    setToken(data.access_token);
    setIsAuthenticated(true);
localStorage.setItem('prompt_this_user', JSON.stringify(data.user));
localStorage.setItem('prompt_this_token', data.access_token);
return data.user;
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
    localStorage.removeItem('prompt_this_user');
// Progress functions (no change needed here)
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

// When logging out or cleaning up, remove the token:
localStorage.removeItem('prompt_this_token');
  };

  const value = {
    user,
    token,
    isAuthenticated,
    progress,
    login,
{
  signup,
  logout,
  completeExercise,
  completeTutorial
}
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
