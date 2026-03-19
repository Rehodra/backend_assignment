import { createContext, useContext, useState, useEffect } from 'react';
import { api, apiPrivate } from '../api/axios';
import {jwtDecode} from 'jwt-decode';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check token on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          // Verify token structure
          const decoded = jwtDecode(token);
          // Fetch full profile to ensure they're still active/exist
          const response = await apiPrivate.get('/auth/me');
          setUser(response.data);
        } catch (error) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setUser(null);
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    const { access_token, refresh_token } = response.data;
    
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    
    const profileResponse = await apiPrivate.get('/auth/me');
    setUser(profileResponse.data);
  };

  const register = async (username, email, password) => {
    // After registration, log them in automatically
    await login(email, password);
  };

  const googleLogin = async (credential) => {
    const response = await api.post('/auth/google', { credential });
    const { access_token, refresh_token } = response.data;
    
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    
    const profileResponse = await apiPrivate.get('/auth/me');
    setUser(profileResponse.data);
  };

  const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await api.post('/auth/logout', { refresh_token: refreshToken });
      } catch (e) {
        console.error("Logout error", e);
      }
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, googleLogin, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
