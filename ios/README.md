# Kenkoumon iOS App

Patient-owned medical consultation recording app for expats in Japan.

## Requirements

- macOS 14+ (Sonoma)
- Xcode 15.0+
- iOS 17.0+ deployment target
- Apple Developer Account

## Quick Start

1. **Open in Xcode**
   ```bash
   open ios/Kenkoumon.xcodeproj
   ```

2. **Configure Signing**
   - Select Kenkoumon project
   - Go to Signing & Capabilities
   - Select your Development Team

3. **Run**
   - Select iOS Simulator or device
   - Press Cmd + R

## Project Structure

```
Kenkoumon/
├── App/
│   └── KenkoumonApp.swift       # App entry point
├── Views/
│   ├── ContentView.swift         # Root view router
│   ├── AuthView.swift            # Login/Register
│   ├── RecordingView.swift       # Audio recording (F1)
│   ├── SessionListView.swift     # Session history (F6)
│   ├── SessionDetailView.swift   # Report viewing (F4)
│   └── SettingsView.swift        # App settings
├── Models/
│   ├── Configuration.swift        # Environment config
│   ├── AIConfiguration.swift      # AI source config
│   ├── Session.swift              # Session model
│   └── Report.swift               # Report & entities
├── Services/
│   ├── AuthManager.swift          # Authentication state
│   ├── APIService.swift           # HTTP client
│   ├── SessionManager.swift       # Session CRUD
│   ├── SettingsManager.swift      # App settings
│   ├── KeychainService.swift      # Secure storage
│   └── AudioPermissionManager.swift
└── Resources/
    └── Assets.xcassets/           # Images, colors
```

## Features

- **F1: Audio Recording** - Record consultations in m4a format
- **F2: Transcription** - Japanese audio → text (Whisper)
- **F3: Report Generation** - Text → structured report (Llama/Claude/GPT)
- **F4: Patient Review** - View and add notes to reports
- **F5: Secure Sharing** - Generate expiring share links
- **F6: Session History** - Browse all recordings

## AI Configuration

The app supports three AI sources:

| Source | Description | Requirements |
|--------|-------------|--------------|
| **On-Device** | Runs locally on phone | iPhone 14+, 4GB+ models |
| **User-Hosted** | Your home server (Ollama) | Ollama URL |
| **Cloud** | API services (OpenAI, Anthropic) | API keys in Settings |

Configure in **Settings** > **AI設定**.

## Development

### Running Tests

```bash
xcodebuild test \
  -scheme Kenkoumon \
  -destination 'platform=iOS Simulator,name=iPhone 15'
```

### Adding Dependencies

This project uses Swift Package Manager. To add:

1. File > Add Package Dependencies
2. Enter package URL
3. Select version rules

## Deployment

### TestFlight

1. Product > Archive
2. Distribute App > TestFlight & App Store
3. Upload to App Store Connect

### App Store

1. Complete App Store listing
2. Submit for review
3. Wait for approval (medical apps: 1-3 days)

## Privacy

- **Microphone**: Required for recording consultations
- **Local Network**: Optional, for user-hosted AI
- **Keychain**: Stores API keys securely

All processing can be done on-device for maximum privacy.
