/**
 * HealthSummaryCard - Displays aggregated health data summary
 */

import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface HealthSummaryCardProps {
  summary?: {
    latest_height?: number;
    latest_weight?: number;
    latest_bmi?: number;
    latest_blood_pressure_systolic?: number;
    latest_blood_pressure_diastolic?: number;
    latest_blood_sugar?: number;
    latest_hba1c?: number;
  };
}

export default function HealthSummaryCard({ summary }: HealthSummaryCardProps) {
  const metrics = [
    {
      label: '身長',
      value: summary?.latest_height
        ? `${summary.latest_height.toFixed(1)} cm`
        : '-',
      icon: 'resize-outline',
      color: '#007AFF',
    },
    {
      label: '体重',
      value: summary?.latest_weight
        ? `${summary.latest_weight.toFixed(1)} kg`
        : '-',
      icon: 'scale-outline',
      color: '#34C759',
    },
    {
      label: 'BMI',
      value: summary?.latest_bmi
        ? summary.latest_bmi.toFixed(1)
        : '-',
      icon: 'body-outline',
      color: '#FF9500',
    },
    {
      label: '血圧',
      value:
        summary?.latest_blood_pressure_systolic && summary?.latest_blood_pressure_diastolic
          ? `${summary.latest_blood_pressure_systolic}/${summary.latest_blood_pressure_diastolic}`
          : '-',
      icon: 'heart-outline',
      color: '#FF3B30',
    },
    {
      label: '血糖',
      value: summary?.latest_blood_sugar
        ? `${summary.latest_blood_sugar.toFixed(0)} mg/dL`
        : '-',
      icon: 'water-outline',
      color: '#5856D6',
    },
    {
      label: 'HbA1c',
      value: summary?.latest_hba1c
        ? `${summary.latest_hba1c.toFixed(1)}%`
        : '-',
      icon: 'bandage-outline',
      color: '#FF2D55',
    },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>健康データサマリー</Text>
      <View style={styles.metricsGrid}>
        {metrics.map((metric, index) => (
          <View key={index} style={styles.metricItem}>
            <View style={[styles.metricIcon, { backgroundColor: `${metric.color}20` }]}>
              <Ionicons name={metric.icon as any} size={20} color={metric.color} />
            </View>
            <Text style={styles.metricLabel}>{metric.label}</Text>
            <Text style={styles.metricValue}>{metric.value}</Text>
          </View>
        ))}
      </View>
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
  title: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 16,
  },
  metricsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -4,
  },
  metricItem: {
    width: '33%',
    alignItems: 'center',
    padding: 8,
  },
  metricIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  metricLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  metricValue: {
    fontSize: 14,
    fontWeight: '600',
  },
});
