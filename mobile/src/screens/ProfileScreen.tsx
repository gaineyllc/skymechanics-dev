import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

export default function ProfileScreen() {
  const user = {
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    rating: 4.8,
    jobsCompleted: 124,
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.profileHeader}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>JD</Text>
        </View>
        <Text style={styles.profileName}>{user.name}</Text>
        <Text style={styles.profileEmail}>{user.email}</Text>
        <View style={styles.ratingContainer}>
          <Text style={styles.ratingValue}>{user.rating}</Text>
          <Text style={styles.ratingLabel}>⭐ ({user.jobsCompleted} jobs)</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Contact Information</Text>
        <View style={styles.infoCard}>
          <Text style={styles.infoLabel}>Phone</Text>
          <Text style={styles.infoValue}>{user.phone}</Text>
        </View>
        <View style={styles.infoCard}>
          <Text style={styles.infoLabel}>Email</Text>
          <Text style={styles.infoValue}>{user.email}</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Preferences</Text>
        <View style={styles.settingCard}>
          <Text style={styles.settingLabel}>Notifications</Text>
          <Text style={styles.settingValue}>Enabled</Text>
        </View>
        <View style={styles.settingCard}>
          <Text style={styles.settingLabel}>Location Tracking</Text>
          <Text style={styles.settingValue}>Enabled</Text>
        </View>
        <View style={styles.settingCard}>
          <Text style={styles.settingLabel}>Language</Text>
          <Text style={styles.settingValue}>English</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  profileHeader: {
    padding: 32,
    alignItems: 'center',
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#007bff',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  avatarText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  profileName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  profileEmail: {
    fontSize: 14,
    color: '#666',
    marginBottom: 16,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ratingValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffc107',
    marginRight: 8,
  },
  ratingLabel: {
    fontSize: 14,
    color: '#666',
  },
  section: {
    padding: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#333',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  infoCard: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  infoLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  infoValue: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  settingCard: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  settingLabel: {
    fontSize: 16,
    color: '#333',
  },
  settingValue: {
    fontSize: 14,
    color: '#999',
  },
});
