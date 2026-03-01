/**
 * HealthDocumentCard - Displays a health document in the list
 */

import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { DocumentCategory } from '@/types';
import { HealthDocument } from '@/contexts/HealthDocumentContext';

interface HealthDocumentCardProps {
  document: HealthDocument;
  onPress: () => void;
}

const categoryLabels: Record<DocumentCategory, string> = {
  [DocumentCategory.HEALTH_CHECKUP]: '健康診断',
  [DocumentCategory.MEDICATION]: 'お薬',
  [DocumentCategory.VACCINATION]: 'ワクチン',
  [DocumentCategory.LAB_RESULTS]: '検査結果',
  [DocumentCategory.MEDICAL_CERTIFICATE]: '診断書',
  [DocumentCategory.OTHER]: 'その他',
};

const categoryIcons: Record<DocumentCategory, string> = {
  [DocumentCategory.HEALTH_CHECKUP]: 'heart-outline',
  [DocumentCategory.MEDICATION]: 'medical-outline',
  [DocumentCategory.VACCINATION]: 'shield-outline',
  [DocumentCategory.LAB_RESULTS]: 'flask-outline',
  [DocumentCategory.MEDICAL_CERTIFICATE]: 'document-text-outline',
  [DocumentCategory.OTHER]: 'document-outline',
};

export default function HealthDocumentCard({ document, onPress }: HealthDocumentCardProps) {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return '日付不明';
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getCategoryLabel = () => {
    const cat = document.category as DocumentCategory;
    return categoryLabels[cat] || document.category;
  };

  const getCategoryIcon = () => {
    const cat = document.category as DocumentCategory;
    return categoryIcons[cat] || 'document-outline';
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.iconContainer}>
          <Ionicons
            name={getCategoryIcon() as any}
            size={24}
            color="#007AFF"
          />
        </View>
        <View style={styles.headerText}>
          <Text style={styles.fileName} numberOfLines={1}>
            {document.file_name}
          </Text>
          <Text style={styles.date}>{formatDate(document.document_date)}</Text>
        </View>
        <Ionicons name="chevron-forward" size={20} color="#999" />
      </View>

      <View style={styles.categoryBadge}>
        <Text style={styles.categoryText}>{getCategoryLabel()}</Text>
      </View>

      {document.summary && (
        <Text style={styles.summary} numberOfLines={2}>
          {document.summary}
        </Text>
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
    alignItems: 'center',
    marginBottom: 12,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F0F8FF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  headerText: {
    flex: 1,
  },
  fileName: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 4,
  },
  date: {
    fontSize: 14,
    color: '#666',
  },
  categoryBadge: {
    alignSelf: 'flex-start',
    backgroundColor: '#F2F2F7',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginBottom: 8,
  },
  categoryText: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
  },
  summary: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
});
