import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function JobDetailScreen({ route }: { route: any }) {
  const { jobId } = route.params;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Job Details</Text>
      <Text style={styles.subtitle}>Job ID: {jobId}</Text>
      <Text style={styles.content}>Job detail view would go here.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 24,
  },
  content: {
    fontSize: 16,
    color: '#666',
  },
});
