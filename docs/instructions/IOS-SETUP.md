# iOS App Setup Guide

Complete guide for setting up and running the Kenkoumon iOS app.

## Prerequisites

- macOS 14 (Sonoma) or later
- Xcode 15.0 or later
- iOS 17.0+ deployment target
- (Optional) Apple Developer Account ($99/year) for App Store distribution

---

## Installation

### 1. Clone Repository

```bash
git clone git@github.com:davidklan-png/kenkoumon.git
cd kenkoumon
```

### 2. Open Xcode Project

```bash
open ios/Kenkoumon.xcodeproj
# or
open ios/Kenkoumon.xcworkspace
```

### 3. Configure Development Team

1. Select the **Kenkoumon** project in the navigator
2. Select the **Kenkoumon** target
3. Go to **Signing & Capabilities**
4. Select your development team:
   - For personal development: Use your Apple ID (free)
   - For App Store: Use your paid developer account
5. Xcode will automatically manage provisioning profiles

---

## Configuration

### API Endpoint

Edit `ios/Shared/Configuration.swift`:

```swift
struct APIConfig {
    static let baseURL = "http://localhost:8000"  // Development
    // static let baseURL = "https://api.kenkoumon.example.com"  // Production
}
```

### AI Settings

Edit `ios/Shared/AIConfiguration.swift`:

```swift
struct AIConfiguration {
    // Primary AI source
    static let transcriptionSource: AISource = .cloud  // or .onDevice, .userHosted
    static let llmSource: AISource = .cloud

    // Cloud API Keys (store in Keychain in production)
    static var openAIKey: String? = nil
    static var anthropicKey: String? = nil

    // User-hosted endpoint
    static var ollamaURL: String? = "http://localhost:11434"
}
```

---

## Building

### iOS Simulator

1. Select a simulator device (iPhone 15 recommended)
2. Press `Cmd + R` or click the Run button
3. App will launch in the simulator

### Physical Device

1. Connect your iPhone via USB
2. Trust the computer on your device
3. Select your device from the scheme selector
4. Press `Cmd + R` to build and run

### Archive (for TestFlight/App Store)

1. Select **Any iOS Device** as the target
2. Go to **Product > Archive**
3. Window will open with archive options
4. Choose **Distribute App**

---

## On-Device AI Setup

### Whisper for Transcription

**Using CoreML (Recommended):**

1. Download Whisper CoreML model:
   - Visit [Hugging Face Whisper CoreML](https://huggingface.co/models?library=coreml&other=whisper)
   - Download `whisper-large-v3-coreml.zip`

2. Add to Xcode project:
   - Drag model files to `ios/Models/`
   - Check "Copy items if needed"
   - Add to Kenkoumon target

3. Compile model (first run only):
   ```swift
   // TranscriptionService.swift will auto-compile on first use
   ```

### Llama for Report Generation

**Using llama.cpp:**

1. Add llama.swift as package dependency:
   - File > Add Package Dependencies
   - URL: `https://github.com/ggerganov/llama.swift`
   - Version: Up to Next Major

2. Download model:
   - Visit [Hugging Face GGUF](https://huggingface.co/models?library=gguf)
   - Download `llama-3.1-8b-instruct-q4_0.gguf`

3. Add to app bundle:
   - Drag to `ios/Models/`
   - Add to Kenkoumon target

---

## Development

### Project Structure

```
ios/
├── Kenkoumon/
│   ├── App/
│   │   ├── KenkoumonApp.swift      # App entry point
│   │   └── AppDelegate.swift
│   ├── Views/
│   │   ├── RecordingView.swift     # F1: Audio recording
│   │   ├── SessionListView.swift   # F6: Session history
│   │   ├── ReportView.swift        # F4: Report review
│   │   ├── SettingsView.swift      # Settings
│   │   └── ShareView.swift         # F5: Secure sharing
│   ├── ViewModels/
│   │   ├── RecordingViewModel.swift
│   │   ├── SessionViewModel.swift
│   │   └── SettingsViewModel.swift
│   ├── Services/
│   │   ├── APIService.swift        # Backend communication
│   │   ├── TranscriptionService.swift
│   │   ├── ReportService.swift
│   │   └── KeychainService.swift   # Secure storage
│   ├── Models/
│   │   ├── Session.swift
│   │   ├── Report.swift
│   │   └── Entity.swift
│   └── Resources/
│       ├── Sounds/                 # Audio feedback
│       └── Fonts/
└── Tests/
    └── KenkoumonTests/
        ├── RecordingTests.swift
        └── APITests.swift
```

### Running Tests

```bash
# Command line
xcodebuild test \
  -scheme Kenkoumon \
  -destination 'platform=iOS Simulator,name=iPhone 15'

# Or in Xcode: Cmd + U
```

---

## Troubleshooting

### Build Errors

**Missing Provisioning Profile:**
1. Go to Signing & Capabilities
2. Check "Automatically manage signing"
3. Select your team

**Minimum OS Version:**
- Project requires iOS 17.0+
- Check deployment target in project settings

### Runtime Errors

**API Connection Failed:**
1. Ensure backend is running: `curl http://localhost:8000/health`
2. Check `APIConfig.baseURL` matches backend address
3. For physical device, use your Mac's IP address:
   ```swift
   static let baseURL = "http://192.168.1.100:8000"
   ```

**Keychain Access Denied:**
1. Enable Keychain capability in Signing & Capabilities
2. Clean build folder: `Cmd + Shift + K`
3. Rebuild

### On-Device AI Issues

**Model Loading Failed:**
1. Verify model file is added to app bundle
2. Check "Copy Bundle Resources" in Build Phases
3. Ensure file size fits device storage

**Out of Memory:**
1. Use quantized models (Q4_0 or Q4_K_M)
2. Reduce context window size
3. Close other apps

---

## Distribution

### TestFlight (Internal Testing)

1. Archive the app
2. Select "Distribute App"
3. Choose TestFlight & App Store
4. Upload to App Store Connect
5. Add internal testers
6. Send test invitations

### App Store (Public Release)

1. Complete App Store listing:
   - App name, description, keywords
   - Screenshots (all iPhone sizes)
   - Privacy policy URL
   - App category: Medical

2. Submit for review:
   - Medical apps require additional documentation
   - Include disclaimer about wellness vs medical diagnosis
   - Provide demo account if applicable

3. Wait for approval (typically 1-3 days for medical apps)

---

## Code Signing

### Development Build

- Uses automatic signing with free Apple ID
- Valid for 7 days
- Must reinstall weekly

### Ad-Hoc Distribution

- Requires paid developer account
- Can install on up to 100 devices
- Valid for 1 year

### App Store Distribution

- Requires paid developer account
- Unlimited installs
- Subject to Apple review

---

## Privacy & Permissions

### Required Permissions

Add to `Info.plist`:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>Kenkoumon needs access to the microphone to record your medical consultations.</string>

<key>NSLocalNetworkUsageDescription</key>
<string>Kenkoumon uses local network to communicate with your self-hosted AI services.</string>
```

### App Privacy

In App Store Connect, disclose:
- Data collection: Audio recordings, transcripts, reports
- Data usage: Processing by AI, storage, sharing
- Data encryption: AES-256 at rest, TLS 1.3 in transit
- Third-party sharing: None (unless user-hosted AI configured)

---

## Next Steps

- [ ] Configure development team and code signing
- [ ] Set up backend API endpoint
- [ ] Configure AI source (on-device, user-hosted, or cloud)
- [ ] Run on iOS Simulator
- [ ] Test on physical device
- [ ] Set up TestFlight distribution
