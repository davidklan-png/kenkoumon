//
//  RecordingView.swift
//  Kenkoumon
//
//  Audio recording view.
//

import SwiftUI
import AVFoundation

struct RecordingView: View {
    @StateObject private var recorder = AudioRecorder()
    @EnvironmentObject var sessionManager: SessionManager
    @EnvironmentObject var settingsManager: SettingsManager
    @State private var isProcessing = false

    var body: some View {
        VStack(spacing: 32) {
            Text("録音")
                .font(.largeTitle)
                .fontWeight(.bold)

            // Mascot
            Image("Mascot")
                .resizable()
                .scaledToFit()
                .frame(width: 150, height: 150)

            // Timer
            if recorder.isRecording {
                Text(recorder.elapsedTimeFormatted)
                    .font(.system(size: 48, weight: .light, design: .monospaced))
                    .foregroundStyle(.primary)
            } else {
                Text("00:00")
                    .font(.system(size: 48, weight: .light, design: .monospaced))
                    .foregroundStyle(.secondary)
            }

            // Recording Button
            Button {
                if recorder.isRecording {
                    recorder.stopRecording()
                } else {
                    recorder.startRecording()
                }
            } label: {
                ZStack {
                    Circle()
                        .fill(recorder.isRecording ? .red : .blue)
                        .frame(width: 80, height: 80)

                    Image(systemName: recorder.isRecording ? "stop.fill" : "mic.fill")
                        .font(.system(size: 30))
                        .foregroundStyle(.white)
                }
            }
            .disabled(isProcessing)

            // Recording Level Indicator
            if recorder.isRecording {
                RecordingLevelView(level: recorder.recordingLevel)
            }

            // Process Button
            if recorder.hasRecording && !recorder.isRecording {
                Button {
                    Task {
                        await processRecording()
                    }
                } label: {
                    if isProcessing {
                        HStack {
                            ProgressView()
                            Text("処理中...")
                        }
                    } else {
                        Text("今すぐ処理")
                    }
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)
            }

            Spacer()

            // Instructions
            VStack(spacing: 8) {
                Text("録音のヒント")
                    .font(.headline)
                Text("• 医師の許可を得てから録音を開始してください")
                Text("• iPhoneを机の上、医師との間に置いてください")
                Text("• 録音はm4a形式で保存されます")
            }
            .font(.caption)
            .foregroundStyle(.secondary)
            .padding()
        }
        .padding()
        .onAppear {
            recorder.requestPermission()
        }
        .alert("処理完了", isPresented: $recorder.showingSuccess) {
            Button("セッションを見る") { }
        } message: {
            Text("レポートが生成されました")
        }
        .alert("エラー", isPresented: $recorder.showingError) {
            Button("OK") { }
        } message: {
            Text(recorder.errorMessage ?? "不明なエラー")
        }
    }

    private func processRecording() async {
        guard let audioURL = recorder.audioFileURL else { return }

        isProcessing = true
        defer { isProcessing = false }

        do {
            // Create session
            try await sessionManager.createSession()

            // Upload audio
            let source = settingsManager.transcriptionSource.rawValue
            try await sessionManager.uploadAudio(fileURL: audioURL, source: source)

            // Transcribe
            try await sessionManager.transcribe(source: source)

            // Generate report
            let provider = settingsManager.cloudLLMProvider == .claude ? "claude" : "gpt"
            try await sessionManager.generateReport(
                source: settingsManager.llmSource.rawValue,
                provider: provider
            )

            recorder.showingSuccess = true
        } catch {
            recorder.errorMessage = error.localizedDescription
            recorder.showingError = true
        }
    }
}

// MARK: - Audio Recorder

@MainActor
class AudioRecorder: NSObject, ObservableObject {
    @Published var isRecording = false
    @Published var hasRecording = false
    @Published var elapsedTime: TimeInterval = 0
    @Published var recordingLevel: Float = 0
    @Published var showingSuccess = false
    @Published var showingError = false
    @Published var errorMessage: String?

    private var audioRecorder: AVAudioRecorder?
    private var timer: Timer?
    private var audioLevelTimer: Timer?

    var audioFileURL: URL? {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        return documentsPath.appendingPathComponent("recording.m4a")
    }

    var elapsedTimeFormatted: String {
        let minutes = Int(elapsedTime) / 60
        let seconds = Int(elapsedTime) % 60
        return String(format: "%02d:%02d", minutes, seconds)
    }

    override init() {
        super.init()
    }

    func requestPermission() {
        AVAudioSession.sharedInstance().requestRecordPermission { _ in }
    }

    func startRecording() {
        guard let url = audioFileURL else { return }

        let settings: [String: Any] = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 44100.0,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]

        do {
            audioRecorder = try AVAudioRecorder(url: url, settings: settings)
            audioRecorder?.delegate = self
            audioRecorder?.isMeteringEnabled = true
            audioRecorder?.record()

            isRecording = true
            hasRecording = false
            elapsedTime = 0

            // Start timer
            timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
                self.elapsedTime += 0.1
            }

            // Start audio level timer
            audioLevelTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
                self?.audioRecorder?.updateMeters()
                self?.recordingLevel = self?.audioRecorder?.averagePower(forChannel: 0) ?? 0
            }

        } catch {
            errorMessage = error.localizedDescription
            showingError = true
        }
    }

    func stopRecording() {
        audioRecorder?.stop()
        timer?.invalidate()
        timer = nil
        audioLevelTimer?.invalidate()
        audioLevelTimer = nil

        isRecording = false
        hasRecording = true
    }
}

extension AudioRecorder: AVAudioRecorderDelegate {
    func audioRecorderDidFinishRecording(_ recorder: AVAudioRecorder, successfully flag: Bool) {
        if !flag {
            errorMessage = "録音に失敗しました"
            showingError = true
        }
    }
}

// MARK: - Recording Level View

struct RecordingLevelView: View {
    let level: Float

    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<20) { i in
                RoundedRectangle(cornerRadius: 2)
                    .fill(barColor(for: i))
                    .frame(width: 4, height: 20)
            }
        }
        .frame(height: 20)
    }

    private func barColor(for index: Int) -> Color {
        let threshold = Float(index) * 3 - 60
        if level > threshold {
            return .green
        } else if level > threshold - 10 {
            return .yellow
        } else {
            return .gray.opacity(0.3)
        }
    }
}
