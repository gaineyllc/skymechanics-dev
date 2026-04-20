import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

interface Mechanic {
  id: string;
  name: string;
  rating: number;
  location: string;
  available: boolean;
}

export default function MechanicsListScreen() {
  const mechanics: Mechanic[] = [
    { id: '1', name: 'Alice Williams', rating: 4.9, location: 'Downtown', available: true },
    { id: '2', name: 'Charlie Brown', rating: 4.7, location: 'Airport', available: true },
    { id: '3', name: 'Diana Prince', rating: 4.8, location: 'Eastside', available: false },
  ];

  const getStatusColor = (available: boolean) => available ? '#4caf50' : '#f44336';

  return (
    <FlatList
      style={styles.container}
      data={mechanics}
      keyExtractor={(item) => item.id}
      ItemSeparatorComponent={() => <View style={styles.separator} />}
      ListHeaderComponent={() => (
        <View style={styles.header}>
          <Text style={styles.title}>Available Mechanics</Text>
          <Text style={styles.subtitle}>{mechanics.length} mechanics found</Text>
        </View>
      )}
      renderItem={({ item }) => (
        <View style={styles.mechanicCard}>
          <View style={styles.mechanicHeader}>
            <Text style={styles.mechanicName}>{item.name}</Text>
            <View style={[styles.availableBadge, { backgroundColor: getStatusColor(item.available) }]}>
              <Text style={styles.availableText}>{item.available ? 'Available' : 'Busy'}</Text>
            </View>
          </View>
          <View style={styles.mechanicInfo}>
            <Text style={styles.mechanicLocation}>📍 {item.location}</Text>
            <Text style={styles.mechanicRating}>⭐ {item.rating}/5.0</Text>
          </View>
        </View>
      )}
      ListEmptyComponent={
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>No mechanics found</Text>
        </View>
      }
    />
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 24,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  separator: {
    height: 1,
    backgroundColor: '#eee',
    marginLeft: 16,
    marginRight: 16,
  },
  mechanicCard: {
    padding: 16,
    backgroundColor: '#fff',
  },
  mechanicHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  mechanicName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    flex: 1,
  },
  availableBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginLeft: 8,
  },
  availableText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  mechanicInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  mechanicLocation: {
    fontSize: 14,
    color: '#666',
  },
  mechanicRating: {
    fontSize: 14,
    color: '#ffc107',
  },
  emptyContainer: {
    padding: 48,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
  },
});
