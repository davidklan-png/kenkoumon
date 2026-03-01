/**
 * Sessions tab - List of recording sessions
 */

import { View, Text, FlatList, TouchableOpacity, Alert, ActivityIndicator, RefreshControl } from 'react-native';
import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'expo-router';
import { useSessions } from '@/contexts/SessionContext';
import { useAuth } from '@/contexts/AuthContext';
import { Ionicons } from '@expo/vector-icons';
import SessionListItem from '@/components/SessionListItem';
import SessionDetailModal from '@/components/SessionDetailModal';

export default function SessionsScreen() {
  const router = useRouter();
  const { user } = useAuth();
  const { sessions, isLoading, loadSessions, deleteSession } = useSessions();
  const [refreshing, setRefreshing] = useState(false);
  const [selectedSession, setSelectedSession] = useState<any>(null);

  const loadSessionsData = useCallback(async () => {
    try {
      await loadSessions(user?.id);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  }, [user?.id, loadSessions]);

  useEffect(() => {
    loadSessionsData();
  }, [loadSessionsData]);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await loadSessionsData();
    setRefreshing(false);
  }, [loadSessionsData]);

  const handleDelete = (sessionId: string) => {
    Alert.alert(
      'セッションを削除',
      'このセッションを削除しますか？',
      [
        { text: 'キャンセル', style: 'cancel' },
        {
          text: '削除',
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteSession(sessionId);
              await loadSessionsData();
            } catch (error) {
              Alert.alert('エラー', '削除に失敗しました');
            }
          },
        },
      ]
    );
  };

  const renderSession = ({ item }: any) => (
    <SessionListItem
      session={item}
      onPress={() => setSelectedSession(item)}
    />
  );

  return (
    <View style={{ flex: 1, backgroundColor: '#F2F2F7' }}>
      {/* Header */}
      <View style={{
        backgroundColor: '#fff',
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#E5E5EA',
      }}>
        <Text style={{ fontSize: 28, fontWeight: 'bold' }}>セッション</Text>
      </View>

      {/* Content */}
      {isLoading && sessions.length === 0 ? (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <ActivityIndicator size="large" />
        </View>
      ) : sessions.length === 0 ? (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 32 }}>
          <Ionicons name="document-outline" size={60} color="#999" />
          <Text style={{ marginTop: 16, fontSize: 16, color: '#999' }}>録音がありません</Text>
          <TouchableOpacity
            style={{
              marginTop: 16,
              backgroundColor: '#007AFF',
              paddingHorizontal: 24,
              paddingVertical: 12,
              borderRadius: 8,
            }}
            onPress={() => router.push('/recording')}
          >
            <Text style={{ color: '#fff', fontWeight: '600' }}>録音を開始</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <FlatList
          data={sessions}
          keyExtractor={(item) => item.id}
          renderItem={renderSession}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          contentContainerStyle={{ padding: 16 }}
        />
      )}

      {/* Session Detail Modal */}
      <SessionDetailModal
        visible={!!selectedSession}
        session={selectedSession}
        onClose={() => setSelectedSession(null)}
        onDelete={() => {
          if (selectedSession) {
            handleDelete(selectedSession.id);
            setSelectedSession(null);
          }
        }}
      />
    </View>
  );
}
