/**
 * Settings Context
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface AppSettings {
  transcriptionSource: 'on-device' | 'user-hosted' | 'cloud';
  llmSource: 'on-device' | 'user-hosted' | 'cloud';
  cloudLLMProvider: 'claude' | 'gpt';
  ollamaUrl: string | null;
  hasOpenAIKey: boolean;
  hasAnthropicKey: boolean;
}

interface SettingsType extends AppSettings {
  updateSettings: (updates: Partial<AppSettings>) => Promise<void>;
  saveAPIKey: (type: 'openai' | 'anthropic', key: string) => Promise<void>;
}

const SettingsContext = createContext<SettingsType | undefined>(undefined);

const TRANSCRIPTION_KEY = 'transcription_source';
const LLM_KEY = 'llm_source';
const CLOUD_PROVIDER_KEY = 'cloud_llm_provider';
const OLLAMA_URL_KEY = 'ollama_url';

export function SettingsProvider({ children }: { children: React.ReactNode }) {
  const [transcriptionSource, setTranscriptionSource] = useState<AppSettings['transcriptionSource']>('on-device');
  const [llmSource, setLLMSource] = useState<AppSettings['llmSource']>('on-device');
  const [cloudLLMProvider, setCloudLLMProvider] = useState<AppSettings['cloudLLMProvider']>('claude');
  const [ollamaUrl, setOllamaUrl] = useState<string | null>(null);
  const [hasOpenAIKey, setHasOpenAIKey] = useState(false);
  const [hasAnthropicKey, setHasAnthropicKey] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const [trans, llm, provider, ollama, openaiKey, anthropicKey] = await Promise.all([
        AsyncStorage.getItem(TRANSCRIPTION_KEY),
        AsyncStorage.getItem(LLM_KEY),
        AsyncStorage.getItem(CLOUD_PROVIDER_KEY),
        AsyncStorage.getItem(OLLAMA_URL_KEY),
        SecureStore.getItemAsync('openai_key'),
        SecureStore.getItemAsync('anthropic_key'),
      ]);

      if (trans) setTranscriptionSource(JSON.parse(trans));
      if (llm) setLLMSource(JSON.parse(llm));
      if (provider) setCloudLLMProvider(JSON.parse(provider));
      if (ollama) setOllamaUrl(JSON.parse(ollama));
      if (openaiKey) setHasOpenAIKey(true);
      if (anthropicKey) setHasAnthropicKey(true);
    } catch (error) {
      console.error('Failed to load settings', error);
    }
  };

  const updateSettings = async (updates: Partial<AppSettings>) => {
    if (updates.transcriptionSource !== undefined) {
      setTranscriptionSource(updates.transcriptionSource);
      await AsyncStorage.setItem(TRANSCRIPTION_KEY, JSON.stringify(updates.transcriptionSource));
    }
    if (updates.llmSource !== undefined) {
      setLLMSource(updates.llmSource);
      await AsyncStorage.setItem(LLM_KEY, JSON.stringify(updates.llmSource));
    }
    if (updates.cloudLLMProvider !== undefined) {
      setCloudLLMProvider(updates.cloudLLMProvider);
      await AsyncStorage.setItem(CLOUD_PROVIDER_KEY, JSON.stringify(updates.cloudLLMProvider));
    }
    if (updates.ollamaUrl !== undefined) {
      setOllamaUrl(updates.ollamaUrl);
      await AsyncStorage.setItem(OLLAMA_URL_KEY, JSON.stringify(updates.ollamaUrl));
    }
  };

  const saveAPIKey = async (type: 'openai' | 'anthropic', key: string) => {
    if (key) {
      await SecureStore.setItemAsync(`${type}_key`, key);
      if (type === 'openai') setHasOpenAIKey(true);
      if (type === 'anthropic') setHasAnthropicKey(true);
    } else {
      await SecureStore.deleteItemAsync(`${type}_key`);
      if (type === 'openai') setHasOpenAIKey(false);
      if (type === 'anthropic') setHasAnthropicKey(false);
    }
  };

  const settings: AppSettings = {
    transcriptionSource,
    llmSource,
    cloudLLMProvider,
    ollamaUrl,
    hasOpenAIKey,
    hasAnthropicKey,
  };

  return (
    <SettingsContext.Provider
      value={{
        ...settings,
        updateSettings,
        saveAPIKey,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

export const useSettings = () => {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettings must be used within SettingsProvider');
  }
  return context;
};
