/**
 * Settings tab - App configuration
 */

import { View, Text, ScrollView, TouchableOpacity, Alert, Switch } from 'react-native';
import { useAuth } from '@/contexts/AuthContext';
import { useSettings } from '@/contexts/SettingsContext';
import { Ionicons } from '@expo/vector-icons';
import * as SecureStore from 'expo-secure-store';
import SettingsSection from '@/components/SettingsSection';
import SettingsRow from '@/components/SettingsRow';

export default function SettingsScreen() {
  const { user, logout } = useAuth();
  const settings = useSettings();

  const handleLogout = () => {
    Alert.alert(
      'ログアウト',
      'ログアウトしますか？',
      [
        { text: 'キャンセル', style: 'cancel' },
        {
          text: 'ログアウト',
          style: 'destructive',
          onPress: logout,
        },
      ]
    );
  };

  const getTranscriptionLabel = () => {
    if (settings.transcriptionSource === 'cloud') return 'クラウド';
    if (settings.transcriptionSource === 'user-hosted') return 'ユーザー登録';
    return 'オンデバイス';
  };

  const getLLMLabel = () => {
    if (settings.llmSource === 'cloud') return 'クラウド';
    if (settings.llmSource === 'user-hosted') return 'ユーザー登録';
    return 'オンデバイス';
  };

  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#F2F2F7' }}>
      {/* Header */}
      <View style={{
        backgroundColor: '#fff',
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#E5E5EA',
      }}>
        <Text style={{ fontSize: 28, fontWeight: 'bold' }}>設定</Text>
      </View>

      {/* Account Section */}
      <SettingsSection title="アカウント">
        <SettingsRow
          label="メール"
          value={user?.email}
        />
        <SettingsRow
          label="お名前"
          value={user?.fullName || '未設定'}
        />
        <SettingsRow
          label="ログアウト"
          onPress={handleLogout}
          textColor="#FF3B30"
          icon="log-out-outline"
        />
      </SettingsSection>

      {/* AI Configuration */}
      <SettingsSection title="AI設定">
        <SettingsRow
          label="文字起こし"
          value={getTranscriptionLabel()}
          onPress={() => {}}
          icon="chevron-forward"
        />
        <SettingsRow
          label="レポート生成"
          value={getLLMLabel()}
          onPress={() => {}}
          icon="chevron-forward"
        />
        {settings.llmSource === 'cloud' && (
          <SettingsRow
            label="AIプロバイダー"
            value={settings.cloudLLMProvider === 'claude' ? 'Claude' : 'GPT-4'}
            onPress={() => {}}
            icon="chevron-forward"
          />
        )}
        {settings.transcriptionSource === 'user-hosted' ||
         settings.llmSource === 'user-hosted' ? (
          <SettingsRow
            label="Ollama URL"
            value={settings.ollamaUrl || '未設定'}
            onPress={() => {}}
            icon="chevron-forward"
          />
        ) : null}
      </SettingsSection>

      {/* API Keys */}
      <SettingsSection title="APIキー">
        <SettingsRow
          label="OpenAI API Key"
          value={settings.hasOpenAIKey ? '設定済み' : '未設定'}
          onPress={() => {}}
          icon="chevron-forward"
        />
        <SettingsRow
          label="Anthropic API Key"
          value={settings.hasAnthropicKey ? '設定済み' : '未設定'}
          onPress={() => {}}
          icon="chevron-forward"
        />
      </SettingsSection>

      {/* Storage */}
      <SettingsSection title="ストレージ">
        <SettingsRow
          label="音声の自動削除"
          value="オフ"
          onPress={() => {}}
        />
      </SettingsSection>

      {/* About */}
      <SettingsSection title="Kenkoumonについて">
        <SettingsRow label="バージョン" value="0.1.0" />
        <SettingsRow
          label="利用規約"
          onPress={() => {}}
          icon="chevron-forward"
        />
        <SettingsRow
          label="プライバシーポリシー"
          onPress={() => {}}
          icon="chevron-forward"
        />
      </SettingsSection>
    </ScrollView>
  );
}
