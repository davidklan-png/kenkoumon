/**
 * RecordingLevelIndicator - Visual audio level meter during recording
 */

import { View, StyleSheet } from 'react-native';

interface RecordingLevelIndicatorProps {
  level: number; // 0-100
}

export default function RecordingLevelIndicator({ level }: RecordingLevelIndicatorProps) {
  // Create 20 bars for the level meter
  const bars = Array.from({ length: 20 }, (_, i) => {
    const barThreshold = (i / 20) * 100;
    const isActive = level >= barThreshold;

    // Color based on level (green -> yellow -> red)
    let barColor = '#34C759';
    if (i >= 14) {
      barColor = '#FF3B30';
    } else if (i >= 7) {
      barColor = '#FFCC00';
    }

    return (
      <View
        key={i}
        style={[
          styles.bar,
          { backgroundColor: isActive ? barColor : '#E5E5EA' },
        ]}
      />
    );
  });

  return (
    <View style={styles.container}>
      <View style={styles.meterContainer}>
        {bars}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginVertical: 24,
  },
  meterContainer: {
    flexDirection: 'row',
    height: 40,
    alignItems: 'flex-end',
    gap: 2,
  },
  bar: {
    width: 6,
    borderRadius: 3,
  },
});
