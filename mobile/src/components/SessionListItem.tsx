/**
 * SessionListItem - Displays a single session in the sessions list
 */

import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SessionStatus } from '@/types';

interface SessionListItemProps {
  session: {
    id: string;
    date: string;
    transcript_ja: string | null;
    report_ja: string | null;
    status: SessionStatus;
  };
  onPress: () => void;
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

const statusColors: Record<SessionStatus, string> = {
  [SessionStatus.UPLOADING]: '#FF9500',
  [SessionStatus.UPLOADED]: '#007AFF',
  [SessionStatus.TRANSCRIBING]: '#FF9500',
  [SessionStatus.TRANSCRIBED]: '#007AFF',
  [SessionStatus.GENERATING]: '#FF9500',
  [SessionStatus.COMPLETE]: '#34C759',
  [SessionStatus.FAILED]: '#FF3B30',
  [SessionStatus.TRANSCRIPTION_FAILED]: '#FF3B30',
  [SessionStatus.GENERATION_FAILED]: '#FF3B30',
};

export default function SessionListItem({ session, onPress }: SessionListItemProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.date}>{formatDate(session.date)}</Text>
        <View style={[styles.statusBadge, { backgroundColor: statusColors[session.status] }]}>
          <Text style={styles.statusText}>{statusLabels[session.status]}</Text>
        </View>
      </View>

      {session.transcript_ja && (
        <View style={styles.row}>
          <Ionicons name="document-text-outline" size={16} color="#666" />
          <Text style={styles.label}>文字起こし</Text>
          <Ionicons name="checkmark-circle" size={16} color="#34C759" />
        </View>
      )}

      {session.report_ja && (
        <View style={styles.row}>
          <Ionicons name="newspaper-outline" size={16} color="#666" />
          <Text style={styles.label}>レポート</Text>
          <Ionicons name="checkmark-circle" size={16} color="#34C759" />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  date: {
    fontSize: 16,
    fontWeight: '600',
    flex: 1,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    fontSize: 12,
    color: '#fff',
    fontWeight: '600',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
  },
  label: {
    flex: 1,
    marginLeft: 8,
    fontSize: 14,
    color: '#666',
  },
});
