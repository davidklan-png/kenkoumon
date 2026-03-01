/**
 * API Service for backend communication
 */

import * as SecureStore from 'expo-secure-store';
import { API_URL, API_VERSION } from '@/constants/api';

export const api = {
  // Get auth header
  getAuthHeader: async () => {
    const token = await SecureStore.getItemAsync('authToken');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  },

  // Helper to handle response
  handleResponse: async (response: Response) => {
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('認証に失敗しました');
      }
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || 'Request failed');
    }
    return response.json();
  },
};

export const authApi = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${API_URL}/api/${API_VERSION}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return api.handleResponse(response);
  },

  register: async (email: string, password: string, fullName?: string) => {
    const response = await fetch(`${API_URL}/api/${API_VERSION}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name: fullName }),
    });
    return api.handleResponse(response);
  },

  getMe: async () => {
    const token = await SecureStore.getItemAsync('authToken');
    const response = await fetch(`${API_URL}/api/${API_VERSION}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return api.handleResponse(response);
  },
};
