/**
 * Kenkoumon - Patient-owned medical consultation recording app
 *
 * Main entry point using Expo Router
 */

import { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import * as SplashScreen from 'expo-splash-screen';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

import { AuthProvider } from '@/contexts/AuthContext';
import { SettingsProvider } from '@/contexts/SettingsContext';
import { SessionProvider } from '@/contexts/SessionContext';
import { HealthDocumentProvider } from '@/contexts/HealthDocumentContext';

// Navigation (using Expo Router)
import { Slot } from 'expo-router';

// Prevent native splash screen from autohiding
SplashScreen.preventAutoHideAsync();

export default function Root() {
  useEffect(() => {
    async function prepare() {
      try {
        await SplashScreen.hideAsync();
      } catch (e) {
        console.warn('Failed to hide splash screen', e);
      }
    }

    prepare();
  }, []);

  return (
    <SafeAreaProvider>
      <AuthProvider>
        <SettingsProvider>
          <SessionProvider>
            <HealthDocumentProvider>
              <GestureHandlerRootView style={{ flex: 1 }}>
                <Slot />
                <StatusBar style="auto" />
              </GestureHandlerRootView>
            </HealthDocumentProvider>
          </SessionProvider>
        </SettingsProvider>
      </AuthProvider>
    </SafeAreaProvider>
  );
}
