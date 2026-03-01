/**
 * Authentication Screen
 */

import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/contexts/AuthContext';
import { Ionicons } from '@expo/vector-icons';

export default function AuthScreen() {
  const { isAuthenticated, isLoading, register, login } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');

  const handleSubmit = async () => {
    if (!email || !password) {
      Alert.alert('エラー', 'メールアドレスとパスワードを入力してください');
      return;
    }

    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password, fullName || undefined);
      }
      router.replace('/(tabs)');
    } catch (error: any) {
      Alert.alert('エラー', error.message || '認証に失敗しました');
    }
  };

  if (isAuthenticated) {
    router.replace('/(tabs)');
  }

  return (
    <View style={styles.container}>
      {/* Mascot */}
      <View style={styles.mascotContainer}>
        <View style={styles.mascotPlaceholder}>
          <Ionicons name="heart-outline" size={80} color="#007AFF" />
        </View>
        <Text style={styles.appName}>Kenkoumon</Text>
        <Text style={styles.appNameJapanese}>健康モニター</Text>
      </View>

      {/* Form */}
      <View style={styles.form}>
        {!isLogin && (
          <TextInput
            style={styles.input}
            placeholder="お名前 (任意)"
            value={fullName}
            onChangeText={setFullName}
            autoCapitalize="words"
          />
        )}

        <TextInput
          style={styles.input}
          placeholder="メールアドレス"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />

        <TextInput
          style={styles.input}
          placeholder="パスワード (8文字以上)"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <TouchableOpacity
          style={[styles.button, styles.primaryButton]}
          onPress={handleSubmit}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>
              {isLogin ? 'ログイン' : '新規登録'}
            </Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => setIsLogin(!isLogin)}
          style={styles.switchButton}
        >
          <Text style={styles.switchButtonText}>
            {isLogin ? 'アカウントをお持ちでない方' : 'すでにアカウントをお持ちの方'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Disclaimer */}
      <View style={styles.disclaimer}>
        <Text style={styles.disclaimerText}>
          Kenkoumonはウェルネスツールです。医療的アドバイスを提供するものではありません。
        </Text>
      </View>

      {/* GitHub link for project info */}
      <TouchableOpacity
        style={styles.githubLink}
        onPress={() => {}}
      >
        <Text style={styles.githubLinkText}>Powered by Kenkoumon</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F7',
    justifyContent: 'center',
    padding: 24,
  },
  mascotContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  mascotPlaceholder: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#F0F8FF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  appName: {
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: 16,
  },
  appNameJapanese: {
    fontSize: 16,
    color: '#666',
  },
  form: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    marginBottom: 24,
  },
  input: {
    backgroundColor: '#F2F2F7',
    borderRadius: 8,
    padding: 16,
    fontSize: 16,
    marginBottom: 12,
  },
  button: {
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  primaryButton: {
    backgroundColor: '#007AFF',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  switchButton: {
    marginTop: 16,
  },
  switchButtonText: {
    color: '#007AFF',
    fontSize: 14,
    textAlign: 'center',
  },
  disclaimer: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  disclaimerText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
    lineHeight: 18,
  },
  githubLink: {
    alignItems: 'center',
  },
  githubLinkText: {
    fontSize: 12,
    color: '#BBB',
  },
});
