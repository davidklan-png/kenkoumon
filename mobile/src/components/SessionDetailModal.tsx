/**
 * SessionDetailModal - Displays full session details
 */

import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SessionStatus } from '@/types';

interface SessionDetailModalProps {
  visible: boolean;
  session: {
    id: string;
    date: string;
    transcript_ja: string | null;
    report_ja: string | null;
    patient_notes: string | null;
    status: SessionStatus;
  } | null;
  onClose: () => void;
  onDelete: () => void;
}

const statusLabels: Record<SessionStatus, string> = {
  [SessionStatus.UPLOADING]: 'アップロード中',
  [SessionStatus.UPLOADED]: 'アップロード完了',
  [SessionStatus.TRANSCRIBING]: '文字起こし中',
  [SessionStatus.TRANSCRIBED]: '文字起こし完了',
  [SessionStatus.GENERATING]: 'レポート生成中',
  [SessionStatus.COMPLETE]: '完了',
  [SessionStatus.FAILED]: '失敗',
  [SessionStatus.TRANSCRIPTION_FAILED]: '文字起こし失敗',
  [SessionStatus.GENERATION_FAILED]: 'レポート生成失敗',
};

export default function SessionDetailModal({
  visible,
  session,
  onClose,
  onDelete,
}: SessionDetailModalProps) {
  if (!session) return null;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const isInProgress = [
    SessionStatus.UPLOADING,
    SessionStatus.TRANSCRIBING,
    SessionStatus.GENERATING,
  ].includes(session.status);

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={onClose} style={styles.headerButton}>
            <Text style={styles.headerButtonText}>閉じる</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>セッション詳細</Text>
          <TouchableOpacity onPress={onDelete} style={styles.headerButton}>
            <Ionicons name="trash-outline" size={24} color="#FF3B30" />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.content}>
          {/* Status */}
          <View style={styles.section}>
            <View style={styles.statusContainer}>
              <Text style={styles.statusLabel}>ステータス</Text>
              <Text style={styles.statusValue}>{statusLabels[session.status]}</Text>
            </View>
            {isInProgress && (
              <ActivityIndicator style={{ marginTop: 16 }} color="#007AFF" />
            )}
          </View>

          {/* Date */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>日時</Text>
            <Text style={styles.sectionContent}>{formatDate(session.date)}</Text>
          </View>

          {/* Transcript */}
          {session.transcript_ja && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>文字起こし</Text>
              <Text style={styles.sectionContent}>{session.transcript_ja}</Text>
            </View>
          )}

          {/* Report */}
          {session.report_ja && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>レポート</Text>
              <Text style={styles.sectionContent}>{session.report_ja}</Text>
            </View>
          )}

          {/* Patient Notes */}
          {session.patient_notes && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>メモ</Text>
              <Text style={styles.sectionContent}>{session.patient_notes}</Text>
            </View>
          )}
        </ScrollView>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F7',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  headerButton: {
    padding: 8,
  },
  headerButtonText: {
    fontSize: 16,
    color: '#007AFF',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  sectionContent: {
    fontSize: 16,
    lineHeight: 24,
  },
  statusContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusLabel: {
    fontSize: 16,
    fontWeight: '600',
  },
  statusValue: {
    fontSize: 16,
    color: '#007AFF',
  },
});
