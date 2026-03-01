/**
 * SettingsRow - Individual settings row with optional chevron
 */

import { View, Text, StyleSheet, TouchableOpacity, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface SettingsRowProps {
  label: string;
  value?: string;
  onPress?: () => void;
  icon?: keyof typeof Ionicons.glyphMap;
  textColor?: string;
  style?: ViewStyle;
}

export default function SettingsRow({
  label,
  value,
  onPress,
  icon,
  textColor = '#000',
  style,
}: SettingsRowProps) {
  const content = (
    <>
      <Text style={[styles.label, { flex: 1 }]}>{label}</Text>
      {value && <Text style={[styles.value, { color: '#666' }]}>{value}</Text>}
      {icon && <Ionicons name={icon} size={20} color="#C7C7CC" />}
    </>
  );

  return (
    <View style={[styles.container, style]}>
      {onPress ? (
        <TouchableOpacity style={styles.row} onPress={onPress}>
          {content}
        </TouchableOpacity>
      ) : (
        <View style={styles.row}>
          <Text style={[styles.label, { flex: 1, color: textColor }]}>{label}</Text>
          {value && <Text style={[styles.value, { color: '#666' }]}>{value}</Text>}
          {icon && <Ionicons name={icon} size={20} color="#C7C7CC" />}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#E5E5EA',
  },
  label: {
    fontSize: 16,
  },
  value: {
    fontSize: 16,
    marginRight: 8,
  },
});
