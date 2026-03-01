/**
 * Recording tab - Audio recording interface
 */

import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { Audio } from 'expo-av';
import { useEffect, useState, useRef } from 'react';
import * as FileSystem from 'expo-file-system';
import { Ionicons } from '@expo/vector-icons';
import { useSessions } from '@/contexts/SessionContext';
import { useSettings } from '@/contexts/SettingsContext';
import RecordingLevelIndicator from '@/components/RecordingLevelIndicator';

export default function RecordingScreen() {
  const router = useRouter();
  const { createSession, uploadAudio, transcribe, generateReport } = useSessions();
  const settings = useSettings();

  const [isRecording, setIsRecording] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [recordingLevel, setRecordingLevel] = useState(0);
  const [hasRecording, setHasRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const recording = useRef<Audio.Recording>();
  const audioUri = useRef<string | undefined>(undefined);
  const intervalRef = useRef<NodeJS.Timeout>();
  const analysisIntervalRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (analysisIntervalRef.current) clearInterval(analysisIntervalRef.current);
    };
  }, []);

  const startRecording = async () => {
    try {
      const { status } = await Audio.requestPermissionsAsync();
      if (status !== 'granted') {
        alert('マイクのアクセス許可が必要です');
        return;
      }

      // Recording configuration for m4a
      const recordingOptions: Audio.RecordingOptions = {
        android: {
          extension: '.m4a',
          outputFormat: Audio.AndroidOutputFormat.MPEG_4,
          audioEncoder: Audio.AndroidAudioEncoder.AAC,
          sampleRate: 44100,
          numberOfChannels: 1,
          bitRate: 128000,
        },
        ios: {
          extension: '.m4a',
          outputFormat: Audio.IOSOutputFormat.MPEG4AAC,
          audioQuality: Audio.IOSAudioQuality.HIGH,
          sampleRate: 44100,
          numberOfChannels: 1,
          bitRate: 128000,
          linearPCMBitDepth: 16,
        },
        web: {
          mimeType: 'audio/webm',
          bitsPerSecond: 128000,
        },
      };

      const newRecording = new Audio.Recording();
      await newRecording.prepareToRecordAsync(recordingOptions);
      await newRecording.startAsync();

      recording.current = newRecording;
      audioUri.current = newRecording.getURI() || undefined;

      setIsRecording(true);
      setHasRecording(false);
      setRecordingDuration(0);

      // Update timer
      intervalRef.current = setInterval(() => {
        setRecordingDuration((d) => d + 0.1);
      }, 100);

      // Update audio level meter
      analysisIntervalRef.current = setInterval(() => {
        if (recording.current) {
          recording.current.getStatusAsync().then((status: Audio.RecordingStatus) => {
            if (status.canRecord) {
              // Audio level simulation - in production use Audio.Analysis
              setRecordingLevel(Math.random() * 100);
            }
          });
        }
      }, 100);

    } catch (error) {
      console.error('Failed to start recording', error);
      alert('録音の開始に失敗しました');
    }
  };

  const stopRecording = async () => {
    if (!recording.current) return;

    try {
      await recording.current.stopAndUnloadAsync();
      setIsRecording(false);
      setHasRecording(true);
      setRecordingLevel(0);

      if (intervalRef.current) clearInterval(intervalRef.current);
      if (analysisIntervalRef.current) clearInterval(analysisIntervalRef.current);
    } catch (error) {
      console.error('Failed to stop recording', error);
    }
  };

  const processRecording = async () => {
    if (!audioUri.current) return;

    setIsProcessing(true);
    try {
      // 1. Create session
      const session = await createSession();

      // 2. Upload audio
      const formData = new FormData();
      formData.append('file', {
        uri: audioUri.current,
        type: 'audio/m4a',
        name: 'audio.m4a',
      } as any);

      await uploadAudio(session.id, formData, settings.transcriptionSource);

      // 3. Transcribe
      await transcribe(session.id, settings.transcriptionSource);

      // 4. Generate report
      await generateReport(session.id, settings.llmSource, settings.cloudLLMProvider);

      alert('処理が完了しました');
      router.push('/sessions');
    } catch (error) {
      console.error('Processing failed', error);
      alert('処理に失敗しました: ' + (error as Error).message);
    } finally {
      setIsProcessing(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>録音</Text>
      </View>

      {/* Mascot */}
      <View style={styles.mascotContainer}>
        <Image
          source={require('@/assets/images/mascot.png')}
          style={styles.mascot}
          resizeMode="contain"
        />
      </View>

      {/* Timer */}
      <Text style={styles.timer}>{formatTime(recordingDuration)}</Text>

      {/* Audio Level Indicator */}
      {isRecording && (
        <RecordingLevelIndicator level={recordingLevel} />
      )}

      {/* Record/Stop Button */}
      <TouchableOpacity
        style={[
          styles.recordButton,
          isRecording && styles.recordButtonActive,
        ]}
        onPress={isRecording ? stopRecording : startRecording}
        disabled={isProcessing}
      >
        <Ionicons
          name={isRecording ? 'stop' : 'mic'}
          size={32}
          color="#fff"
        />
      </TouchableOpacity>

      {/* Process Button */}
      {hasRecording && !isRecording && (
        <TouchableOpacity
          style={styles.processButton}
          onPress={processRecording}
          disabled={isProcessing}
        >
          {isProcessing ? (
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <ActivityIndicator size="small" color="#fff" />
              <Text style={{ marginLeft: 8, color: '#fff' }}>処理中...</Text>
            </View>
          ) : (
            <Text style={styles.processButtonText}>今すぐ処理</Text>
          )}
        </TouchableOpacity>
      )}

      {/* Instructions */}
      <View style={styles.instructions}>
        <Text style={styles.instructionTitle}>録音のヒント</Text>
        <Text style={styles.instructionText}>
          • 医師の許可を得てから録音を開始してください
        </Text>
        <Text style={styles.instructionText}>
          • iPhoneを机の上、医師との間に置いてください
        </Text>
        <Text style={styles.instructionText}>
          • 録音はm4a形式で保存されます
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F7',
  },
  header: {
    backgroundColor: '#fff',
    paddingHorizontal: 16,
    paddingVertical: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  mascotContainer: {
    alignItems: 'center',
    marginVertical: 24,
  },
  mascot: {
    width: 150,
    height: 150,
  },
  timer: {
    fontSize: 48,
    fontWeight: '200',
    textAlign: 'center',
    marginVertical: 24,
  },
  recordButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    alignSelf: 'center',
    marginBottom: 24,
  },
  recordButtonActive: {
    backgroundColor: '#FF3B30',
  },
  processButton: {
    backgroundColor: '#34C759',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 12,
    alignSelf: 'center',
    marginHorizontal: 16,
  },
  processButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  instructions: {
    backgroundColor: '#fff',
    margin: 16,
    padding: 16,
    borderRadius: 12,
  },
  instructionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  instructionText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
});
