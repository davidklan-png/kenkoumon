/**
 * DocumentDetailModal - Displays full health document details
 */

import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { DocumentCategory, ExtractedHealthData } from '@/types';

interface DocumentDetailModalProps {
  visible: boolean;
  document: {
    id: string;
    file_name: string;
    upload_date: string;
    document_date: string | null;
    category: DocumentCategory;
    summary: string | null;
    extracted_data: ExtractedHealthData | null;
  } | null;
  onClose: () => void;
  onDelete: () => void;
}

const categoryLabels: Record<DocumentCategory, string> = {
  [DocumentCategory.HEALTH_CHECKUP]: '健康診断',
  [DocumentCategory.MEDICATION]: 'お薬',
  [DocumentCategory.VACCINATION]: 'ワクチン',
  [DocumentCategory.LAB_RESULTS]: '検査結果',
  [DocumentCategory.MEDICAL_CERTIFICATE]: '診断書',
  [DocumentCategory.OTHER]: 'その他',
};

export default function DocumentDetailModal({
  visible,
  document,
  onClose,
  onDelete,
}: DocumentDetailModalProps) {
  if (!document) return null;

  const formatDate = (dateString: string | null) => {
    if (!dateString) return '日付不明';
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const renderExtractedData = (data: ExtractedHealthData | null) => {
    if (!data) return null;

    const items = [
      { label: '身長', value: data.height, unit: 'cm' },
      { label: '体重', value: data.weight, unit: 'kg' },
      { label: 'BMI', value: data.bmi, unit: '' },
      { label: '血圧(収縮期)', value: data.blood_pressure_systolic, unit: 'mmHg' },
      { label: '血圧(拡張期)', value: data.blood_pressure_diastolic, unit: 'mmHg' },
      { label: '血糖', value: data.blood_sugar, unit: 'mg/dL' },
      { label: 'HbA1c', value: data.hba1c, unit: '%' },
      { label: 'LDLコレステロール', value: data.ldl_cholesterol, unit: 'mg/dL' },
      { label: 'HDLコレステロール', value: data.hdl_cholesterol, unit: 'mg/dL' },
      { label: '中性脂肪', value: data.triglycerides, unit: 'mg/dL' },
      { label: 'AST', value: data.ast, unit: 'U/L' },
      { label: 'ALT', value: data.alt, unit: 'U/L' },
      { label: 'γ-GTP', value: data.gamma_gtp, unit: 'U/L' },
    ].filter(item => item.value !== undefined);

    if (items.length === 0) return null;

    return (
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>抽出データ</Text>
        <View style={styles.dataGrid}>
          {items.map((item, index) => (
            <View key={index} style={styles.dataItem}>
              <Text style={styles.dataLabel}>{item.label}</Text>
              <Text style={styles.dataValue}>
                {item.value?.toFixed(1)}{item.unit}
              </Text>
            </View>
          ))}
        </View>
      </View>
    );
  };

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
          <Text style={styles.headerTitle}>ドキュメント詳細</Text>
          <TouchableOpacity onPress={onDelete} style={styles.headerButton}>
            <Ionicons name="trash-outline" size={24} color="#FF3B30" />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.content}>
          {/* Category */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>カテゴリ</Text>
            <Text style={styles.sectionContent}>{categoryLabels[document.category]}</Text>
          </View>

          {/* Document Date */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>文書日付</Text>
            <Text style={styles.sectionContent}>{formatDate(document.document_date)}</Text>
          </View>

          {/* File Name */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>ファイル名</Text>
            <Text style={styles.sectionContent}>{document.file_name}</Text>
          </View>

          {/* Summary */}
          {document.summary && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>サマリー</Text>
              <Text style={styles.sectionContent}>{document.summary}</Text>
            </View>
          )}

          {/* Extracted Data */}
          {renderExtractedData(document.extracted_data)}
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
  dataGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -4,
  },
  dataItem: {
    width: '50%',
    paddingHorizontal: 4,
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#F2F2F7',
  },
  dataLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  dataValue: {
    fontSize: 16,
    fontWeight: '600',
  },
});
