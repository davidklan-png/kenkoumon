/**
 * Session Context - Recording session management
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import { API_URL } from '@/constants/api';

interface Session {
  id: string;
  patient_id: string;
  date: string;
  transcript_ja: string | null;
  report_ja: string | null;
  patient_notes: string | null;
  status: string;
  created_at: string;
}

interface SessionContextType {
  sessions: Session[];
  isLoading: boolean;
  loadSessions: (patientId: string) => Promise<void>;
  createSession: () => Promise<Session>;
  updateSession: (sessionId: string, updates: any) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  uploadAudio: (sessionId: string, formData: FormData, source: string) => Promise<void>;
  transcribe: (sessionId: string, source: string) => Promise<void>;
  generateReport: (sessionId: string, source: string, provider: string) => Promise<void>;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export function SessionProvider({ children }: { children: React.ReactNode }) {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const getAuthHeader = async () => {
    const token = await SecureStore.getItemAsync('authToken');
    return { Authorization: `Bearer ${token}` };
  };

  const loadSessions = async (patientId: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/sessions`, {
        headers: await getAuthHeader(),
      });
      if (response.ok) {
        const data = await response.json();
        setSessions(data);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const createSession = async (): Promise<Session> => {
    const response = await fetch(`${API_URL}/api/v1/sessions`, {
      method: 'POST',
      headers: {
        ...(await getAuthHeader()),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ date: new Date().toISOString() }),
    });

    if (!response.ok) {
      throw new Error('Failed to create session');
    }

    const session = await response.json();
    setSessions([session, ...sessions]);
    return session;
  };

  const updateSession = async (sessionId: string, updates: any) => {
    const response = await fetch(`${API_URL}/api/v1/sessions/${sessionId}`, {
      method: 'PATCH',
      headers: {
        ...(await getAuthHeader()),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
    });

    if (response.ok) {
      const updated = await response.json();
      setSessions(sessions.map((s) => s.id === sessionId ? updated : s));
    }
  };

  const deleteSession = async (sessionId: string) => {
    const response = await fetch(`${API_URL}/api/v1/sessions/${sessionId}`, {
      method: 'DELETE',
      headers: await getAuthHeader(),
    });

    if (response.ok) {
      setSessions(sessions.filter((s) => s.id !== sessionId));
    }
  };

  const uploadAudio = async (sessionId: string, formData: FormData, source: string) => {
    formData.append('transcription_source', source);

    const response = await fetch(`${API_URL}/api/v1/sessions/${sessionId}/audio`, {
      method: 'POST',
      headers: await getAuthHeader(),
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload audio');
    }
  };

  const transcribe = async (sessionId: string, source: string) => {
    const response = await fetch(`${API_URL}/api/v1/sessions/${sessionId}/transcribe?source=${source}`, {
      method: 'POST',
      headers: await getAuthHeader(),
    });

    if (response.ok) {
      const updated = await response.json();
      setSessions(sessions.map((s) => s.id === sessionId ? updated : s));
    }
  };

  const generateReport = async (sessionId: string, source: string, provider: string) => {
    const response = await fetch(
      `${API_URL}/api/v1/sessions/${sessionId}/generate?source=${source}&cloud_provider=${provider}`,
      {
        method: 'POST',
        headers: await getAuthHeader(),
      }
    );

    if (response.ok) {
      const updated = await response.json();
      setSessions(sessions.map((s) => s.id === sessionId ? updated : s));
    }
  };

  return (
    <SessionContext.Provider
      value={{
        sessions,
        isLoading,
        loadSessions,
        createSession,
        updateSession,
        deleteSession,
        uploadAudio,
        transcribe,
        generateReport,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export const useSessions = () => {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error('useSessions must be used within SessionProvider');
  }
  return context;
};
