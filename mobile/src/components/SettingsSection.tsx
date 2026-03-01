/**
 * SettingsSection - Grouped settings section with title
 */

import { View, Text, StyleSheet, ViewStyle } from 'react-native';

interface SettingsSectionProps {
  title: string;
  children: React.ReactNode;
  style?: ViewStyle;
}

export default function SettingsSection({ title, children, style }: SettingsSectionProps) {
  return (
    <View style={[styles.container, style]}>
      <Text style={styles.title}>{title}</Text>
      <View style={styles.content}>{children}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 24,
    paddingHorizontal: 16,
  },
  title: {
    fontSize: 13,
    color: '#666',
    marginBottom: 8,
    marginLeft: 16,
    textTransform: 'uppercase',
  },
  content: {
    backgroundColor: '#fff',
    borderRadius: 12,
    overflow: 'hidden',
  },
});
