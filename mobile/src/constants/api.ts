/**
 * API Constants
 */

export const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';
export const API_VERSION = process.env.EXPO_PUBLIC_API_VERSION || 'v1';

// AI Sources
export const TRANSCRIPTION_SOURCE = process.env.EXPO_PUBLIC_DEFAULT_TRANSCRIPTION_SOURCE || 'cloud';
export const LLM_SOURCE = process.env.EXPO_PUBLIC_DEFAULT_LLM_SOURCE || 'cloud';

// User-hosted AI
export const OLLAMA_URL = process.env.EXPO_PUBLIC_OLLAMA_URL || 'http://localhost:11434';
