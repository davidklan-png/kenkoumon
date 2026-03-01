/**
 * Authentication Context
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

interface User {
  id: string;
  email: string;
  full_name?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const API_URL = 'http://localhost:8000';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const isSecureStoreAvailable = Platform.OS !== 'web';

// Simple in-memory storage for web
let webToken: string | null = null;
let webUser: User | null = null;

const getToken = async (): Promise<string | null> => {
  if (isSecureStoreAvailable) {
    return await SecureStore.getItemAsync('authToken');
  }
  return webToken;
};

const setToken = async (token: string): Promise<void> => {
  if (isSecureStoreAvailable) {
    await SecureStore.setItemAsync('authToken', token);
  } else {
    webToken = token;
  }
};

const deleteToken = async (): Promise<void> => {
  if (isSecureStoreAvailable) {
    await SecureStore.deleteItemAsync('authToken');
  } else {
    webToken = null;
  }
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    setIsLoading(true);
    try {
      const token = await getToken();
      if (token) {
        try {
          const response = await fetch(`${API_URL}/api/v1/auth/me`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (response.ok) {
            const userData = await response.json();
            setUser(userData);
          }
        } catch (err) {
          // Backend might not be running, that's ok for dev
          console.warn('Auth check failed (backend may not be running)', err);
        }
      }
    } catch (error) {
      console.error('Auth check failed', error);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (email: string, password: string, fullName?: string) => {
    const response = await fetch(`${API_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name: fullName }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Registration failed' }));
      throw new Error(error.detail || 'Registration failed');
    }

    const data = await response.json();
    await setToken(data.access_token);
    setUser(data.user || { id: data.id, email: data.email, full_name: fullName });
  };

  const login = async (email: string, password: string) => {
    const response = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    await setToken(data.access_token);
    setUser(data.user || { id: data.id, email: email });
  };

  const logout = async () => {
    await deleteToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
