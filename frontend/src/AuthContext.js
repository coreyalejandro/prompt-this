import React, { createContext, useContext, useState, useEffect } from 'react';

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

  useEffect(() => {
    const savedUser = localStorage.getItem('prompt_this_user');
    const savedToken = localStorage.getItem('prompt_this_token');
    if (savedUser && savedToken) {
      setUser(JSON.parse(savedUser));
      setToken(savedToken);
      setIsAuthenticated(true);
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
    localStorage.removeItem('prompt_this_token');
  };

  const value = {
    user,
    token,
    isAuthenticated,
    login,
    signup,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
