/**
 * Health data tab - MyNumber Portal imports
 */

import { View, Text, FlatList, TouchableOpacity, Alert, StyleSheet } from 'react-native';
import { useHealthDocuments } from '@/contexts/HealthDocumentContext';
import { Ionicons } from '@expo/vector-icons';
import { useState, useCallback, useEffect } from 'react';
import { RefreshControl } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import HealthDocumentCard from '@/components/HealthDocumentCard';
import HealthSummaryCard from '@/components/HealthSummaryCard';
import DocumentDetailModal from '@/components/DocumentDetailModal';

export default function HealthScreen() {
  const {
    documents,
    isLoading,
    loadDocuments,
    importDocuments,
    deleteDocument,
  } = useHealthDocuments();

  const [refreshing, setRefreshing] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<any>(null);
  const [showingImporter, setShowingImporter] = useState(false);

  const loadDocumentsData = useCallback(async () => {
    try {
      await loadDocuments();
    } catch (error) {
      console.error('Failed to load documents:', error);
    }
  }, [loadDocuments]);

  useEffect(() => {
    loadDocumentsData();
  }, [loadDocumentsData]);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await loadDocumentsData();
    setRefreshing(false);
  }, [loadDocumentsData]);

  const handleImport = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/pdf', 'image/*'],
        multiple: true,
        copyToCacheDirectory: true,
      });

      if (result.canceled) return;

      const fileUris = result.assets.map((asset) => asset.uri);
      await importDocuments(fileUris);
      await loadDocumentsData();
    } catch (error) {
      console.error('Import failed:', error);
      Alert.alert('エラー', 'ドキュメントのインポートに失敗しました');
    }
  };

  const handleDelete = (docId: string) => {
    Alert.alert(
      'ドキュメントを削除',
      'このドキュメントを削除しますか？',
      [
        { text: 'キャンセル', style: 'cancel' },
        {
          text: '削除',
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteDocument(docId);
              await loadDocumentsData();
            } catch (error) {
              Alert.alert('エラー', '削除に失敗しました');
            }
          },
        },
      ]
    );
  };

  return (
    <View style={{ flex: 1, backgroundColor: '#F2F2F7' }}>
      {/* Header */}
      <View style={{
        backgroundColor: '#fff',
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#E5E5EA',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <Text style={{ fontSize: 28, fontWeight: 'bold' }}>健康データ</Text>
      </View>

      <FlatList
        ListHeaderComponent={
          <View style={{ padding: 16 }}>
            <HealthSummaryCard />

            <TouchableOpacity
              style={styles.importButton}
              onPress={handleImport}
            >
              <Ionicons name="add-circle" size={20} color="#007AFF" />
              <Text style={styles.importButtonText}>
                MyNumber Portalからインポート
              </Text>
            </TouchableOpacity>
          </View>
        }
        data={documents}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <HealthDocumentCard
            document={item}
            onPress={() => setSelectedDoc(item)}
          />
        )}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={{ padding: 16 }}
        ListEmptyComponent={
          <View style={{ alignItems: 'center', padding: 32 }}>
            <Ionicons name="document-outline" size={60} color="#999" />
            <Text style={{ marginTop: 16, fontSize: 16, color: '#999' }}>
              健康データがありません
            </Text>
            <Text style={{ marginTop: 8, fontSize: 14, color: '#BBB' }}>
              MyNumber PortalからダウンロードしたPDFをインポートできます
            </Text>
          </View>
        }
      />

      {/* Document Detail Modal */}
      <DocumentDetailModal
        visible={!!selectedDoc}
        document={selectedDoc}
        onClose={() => setSelectedDoc(null)}
        onDelete={() => {
          if (selectedDoc) {
            handleDelete(selectedDoc.id);
            setSelectedDoc(null);
          }
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  importButton: {
    flexDirection: 'row' as const,
    alignItems: 'center' as const,
    backgroundColor: '#F0F8FF',
    padding: 12,
    borderRadius: 8,
    marginTop: 12,
  },
  importButtonText: {
    marginLeft: 8,
    color: '#007AFF',
    fontSize: 14,
    fontWeight: '600' as const,
  },
});
