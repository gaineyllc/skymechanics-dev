import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator, RefreshControl } from 'react-native';
import { jobs } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

interface Job {
  id: string;
  title: string;
  status: string;
  customer: string;
  aircraft: string;
  created_at: string;
}

export default function JobListScreen() {
  const [jobsList, setJobsList] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      const response = await jobs.list();
      setJobsList(response.data);
    } catch (error) {
      console.error('Error loading jobs:', error);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  const onRefresh = () => {
    setIsRefreshing(true);
    loadJobs();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return '#ffc107';
      case 'in_progress': return '#2196f3';
      case 'completed': return '#4caf50';
      case 'cancelled': return '#f44336';
      default: return '#666';
    }
  };

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#007bff" />
        <Text style={styles.loadingText}>Loading your jobs...</Text>
      </View>
    );
  }

  return (
    <FlatList
      style={styles.container}
      data={jobsList}
      keyExtractor={(item) => item.id}
      refreshControl={
        <RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} />
      }
      ItemSeparatorComponent={() => <View style={styles.separator} />}
      ListHeaderComponent={() => (
        <View style={styles.header}>
          <Text style={styles.title}>Your Jobs</Text>
          <Text style={styles.subtitle}>{jobsList.length} active jobs</Text>
        </View>
      )}
      renderItem={({ item }) => (
        <View style={styles.jobCard}>
          <View style={styles.jobHeader}>
            <Text style={styles.jobTitle}>{item.title}</Text>
            <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
              <Text style={styles.statusText}>{item.status}</Text>
            </View>
          </View>
          <View style={styles.jobInfo}>
            <Text style={styles.jobCustomer}>👤 {item.customer}</Text>
            <Text style={styles.jobAircraft}>✈️ {item.aircraft}</Text>
            <Text style={styles.jobDate}>{new Date(item.created_at).toLocaleDateString()}</Text>
          </View>
        </View>
      )}
      ListEmptyComponent={
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>No jobs found</Text>
          <Text style={styles.emptySubtitle}>New jobs will appear here</Text>
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
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    color: '#666',
    fontSize: 14,
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
  jobCard: {
    padding: 16,
    backgroundColor: '#fff',
  },
  jobHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  jobTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    flex: 1,
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginLeft: 8,
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  jobInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  jobCustomer: {
    fontSize: 14,
    color: '#666',
  },
  jobAircraft: {
    fontSize: 14,
    color: '#666',
  },
  jobDate: {
    fontSize: 14,
    color: '#999',
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
  emptySubtitle: {
    fontSize: 14,
    color: '#999',
    marginTop: 8,
  },
});
