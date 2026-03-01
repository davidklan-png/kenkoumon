/**
 * Health Document Context - MyNumber Portal imports
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import * as DocumentPicker from 'expo-document-picker';
import { API_URL } from '@/constants/api';

export interface HealthDocument {
  id: string;
  patient_id: string;
  file_name: string;
  file_type: string;
  upload_date: string;
  document_date: string | null;
  category: string;
  summary: string | null;
  extracted_data: any;
}

interface HealthDocumentContextType {
  documents: HealthDocument[];
  isLoading: boolean;
  loadDocuments: () => Promise<void>;
  importDocuments: (fileUris: string[]) => Promise<void>;
  updateDocument: (docId: string, updates: any) => Promise<void>;
  deleteDocument: (docId: string) => Promise<void>;
}

const HealthDocumentContext = createContext<HealthDocumentContextType | undefined>(undefined);

export function HealthDocumentProvider({ children }: { children: React.ReactNode }) {
  const [documents, setDocuments] = useState<HealthDocument[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const getAuthHeader = async () => {
    const token = await SecureStore.getItemAsync('authToken');
    return { Authorization: `Bearer ${token}` };
  };

  const loadDocuments = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/health-documents`, {
        headers: await getAuthHeader(),
      });
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const importDocuments = async (fileUris: string[]) => {
    for (const uri of fileUris) {
      try {
        const formData = new FormData();
        formData.append('file', {
          uri,
          name: 'file',
          type: 'application/pdf',
        } as any);

        const response = await fetch(`${API_URL}/api/v1/health-documents`, {
          method: 'POST',
          headers: await getAuthHeader(),
          body: formData,
        });

        if (response.ok) {
          const doc = await response.json();
          setDocuments([doc, ...documents]);
        }
      } catch (error) {
        console.error('Failed to import document:', error);
      }
    }
  };

  const updateDocument = async (docId: string, updates: any) => {
    const response = await fetch(`${API_URL}/api/v1/health-documents/${docId}`, {
      method: 'PATCH',
      headers: {
        ...(await getAuthHeader()),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
    });

    if (response.ok) {
      const updated = await response.json();
      setDocuments(documents.map((d) => d.id === docId ? updated : d));
    }
  };

  const deleteDocument = async (docId: string) => {
    const response = await fetch(`${API_URL}/api/v1/health-documents/${docId}`, {
      method: 'DELETE',
      headers: await getAuthHeader(),
    });

    if (response.ok) {
      setDocuments(documents.filter((d) => d.id !== docId));
    }
  };

  return (
    <HealthDocumentContext.Provider
      value={{
        documents,
        isLoading,
        loadDocuments,
        importDocuments,
        updateDocument,
        deleteDocument,
      }}
    >
      {children}
    </HealthDocumentContext.Provider>
  );
}

export const useHealthDocuments = () => {
  const context = useContext(HealthDocumentContext);
  if (!context) {
    throw new Error('useHealthDocuments must be used within HealthDocumentProvider');
  }
  return context;
};
