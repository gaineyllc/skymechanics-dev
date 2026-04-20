import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { PaperProvider } from 'react-native-paper';

// Screens
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import JobListScreen from './src/screens/JobListScreen';
import JobDetailScreen from './src/screens/JobDetailScreen';
import ProfileScreen from './src/screens/ProfileScreen';
import MechanicsListScreen from './src/screens/MechanicsListScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Login">
          <Stack.Screen name="Login" component={LoginScreen} options={{ title: 'Sign In' }} />
          <Stack.Screen name="Register" component={RegisterScreen} options={{ title: 'Create Account' }} />
          <Stack.Screen name="Dashboard" component={DashboardScreen} options={{ title: 'Home' }} />
          <Stack.Screen name="JobList" component={JobListScreen} options={{ title: 'Jobs' }} />
          <Stack.Screen name="JobDetail" component={JobDetailScreen} options={{ title: 'Job Details' }} />
          <Stack.Screen name="Profile" component={ProfileScreen} options={{ title: 'Profile' }} />
          <Stack.Screen name="Mechanics" component={MechanicsListScreen} options={{ title: 'Mechanics' }} />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
