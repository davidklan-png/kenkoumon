# EAS Build Configuration
# Your Expo.dev credentials go here for automated builds

## EAS Login (Run this once locally)
eas login

## EAS Project Setup
eas project:info

## Environment Variables for EAS Builds
# Store sensitive values in EAS secrets, not here:

eas secret:create OPENAI_API_KEY
eas secret:create ANTHROPIC_API_KEY
eas secret:create EXPO_PUBLIC_API_URL --value "https://api.kenkoumon.example.com"

## View Current Credentials
eas credentials:list

## Build Commands
# Development build
eas build --profile development --platform ios

# Preview build
eas build --profile preview --platform ios

# Production build
eas build --profile production --platform ios
eas build --profile production --platform android

## Submit to App Stores
eas submit --platform ios
eas submit --platform android
