# SkyMechanics Mobile App

React Native application for iOS and Android.

## Tech Stack

- **React Native**: 0.74.2
- **React**: 18.2.0
- **Navigation**: React Navigation 6
- **UI**: React Native Paper
- **Icons**: React Native Vector Icons
- **HTTP**: Axios
- **State**: Context API

## Features

- ✅ User authentication (login/register)
- ✅ Job list and details
- ✅ Mechanic directory
- ✅ User profile
- ✅ Dashboard with metrics

## Setup

### Prerequisites

- Node.js >= 18
- React Native CLI
- iOS/Android SDK

### Installation

```bash
cd mobile
npm install
npx pod-install ios
```

### Running

```bash
# Android
npm run android

# iOS
npm run ios
```

### Development

```bash
# Start Metro bundler
npm start

# Run tests
npm test

# Lint
npm run lint
```

## Directory Structure

```
mobile/
├── App.js                    # Main app component
├── index.js                  # Entry point
├── app.json                  # App metadata
├── package.json              # Dependencies
├── .gitignore                # Git ignore rules
├── src/
│   ├── screens/              # Screen components
│   │   ├── LoginScreen.tsx
│   │   ├── RegisterScreen.tsx
│   │   ├── DashboardScreen.tsx
│   │   ├── JobListScreen.tsx
│   │   ├── JobDetailScreen.tsx
│   │   ├── ProfileScreen.tsx
│   │   └── MechanicsListScreen.tsx
│   ├── services/
│   │   └── api.ts           # API service
│   └── contexts/
│       └── AuthContext.tsx  # Auth state
└── README.md
```

## API Integration

The app connects to the backend services:

| Service | Port | Description |
|---------|------|-------------|
| Auth Service | 8200 | Authentication endpoints |
| Mechanics Service | 8201 | Mechanic profiles |
| Jobs Service | 8202 | Job management |
| Analytics Service | 8203 | Reporting metrics |

## Environment

Create `.env` file:

```env
API_BASE_URL=http://localhost:8200
```

## Build for Production

### Android

```bash
cd android
./gradlew assembleRelease
```

### iOS

```bash
# Open in Xcode
open ios/SkyMechanics.xcworkspace

# Build via Xcode UI or:
xcodebuild -scheme SkyMechanics -configuration Release -archivePath "build/SkyMechanics.xcarchive" archive
```

## Deployment

- **Distribution**: Firebase App Distribution
- **Crash Reporting**: Sentry
- **Push Notifications**: Firebase Cloud Messaging

## Development Status

- [x] Authentication screens
- [x] Dashboard
- [x] Job list
- [x] Mechanic directory
- [ ] Real-time updates (WebSocket)
- [ ] Location tracking
- [ ] Push notifications
