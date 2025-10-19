import { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { customerService } from '../services/customerService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check authentication on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      if (authService.isAuthenticated()) {
        const userData = await authService.getCurrentUser();
        setUser(userData);
        setIsAuthenticated(true);

        // Fetch customer profile
        try {
          const profileData = await customerService.getProfile();
          setProfile(profileData);
        } catch (error) {
          console.error('Profile fetch error:', error);
        }
      }
    } catch (error) {
      console.error('Auth check error:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      const data = await authService.login(credentials);
      await checkAuth();
      return { success: true, data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      };
    }
  };

  const register = async (userData) => {
    try {
      const data = await authService.register(userData);
      await checkAuth();
      return { success: true, data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || 'Registration failed'
      };
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setProfile(null);
      setIsAuthenticated(false);
      localStorage.removeItem('cart');
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const updatedProfile = await customerService.updateProfile(profileData);
      setProfile(updatedProfile);
      return { success: true, data: updatedProfile };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || 'Update failed'
      };
    }
  };

  const value = {
    user,
    profile,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    updateProfile,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
