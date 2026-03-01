//
//  SettingsManager.swift
//  Kenkoumon
//
//  App settings persistence.
//

import Foundation
import Combine

@MainActor
class SettingsManager: ObservableObject {
    @Published var transcriptionSource: AISource {
        didSet {
            UserDefaults.standard.set(transcriptionSource.rawValue, forKey: "transcriptionSource")
        }
    }

    @Published var llmSource: AISource {
        didSet {
            UserDefaults.standard.set(llmSource.rawValue, forKey: "llmSource")
        }
    }

    @Published var cloudLLMProvider: CloudLLMProvider {
        didSet {
            UserDefaults.standard.set(cloudLLMProvider.rawValue, forKey: "cloudLLMProvider")
        }
    }

    @Published var ollamaURL: String {
        didSet {
            UserDefaults.standard.set(ollamaURL, forKey: "ollamaURL")
            AIConfiguration.ollamaURL = ollamaURL.isEmpty ? nil : ollamaURL
        }
    }

    @Published var autoDeleteAudio: AutoDeleteOption {
        didSet {
            UserDefaults.standard.set(autoDeleteOption.rawValue, forKey: "autoDeleteAudio")
        }
    }

    private var autoDeleteOption: AutoDeleteOption

    enum AutoDeleteOption: String, CaseIterable {
        case off = "off"
        case after30Days = "30"
        case after90Days = "90"

        var displayString: String {
            switch self {
            case .off: return "オフ"
            case .after30Days: return "30日後"
            case .after90Days: return "90日後"
            }
        }
    }

    init() {
        // Load from UserDefaults
        let transcriptionSourceRaw = UserDefaults.standard.string(forKey: "transcriptionSource") ?? AISource.cloud.rawValue
        self.transcriptionSource = AISource(rawValue: transcriptionSourceRaw) ?? .cloud

        let llmSourceRaw = UserDefaults.standard.string(forKey: "llmSource") ?? AISource.cloud.rawValue
        self.llmSource = AISource(rawValue: llmSourceRaw) ?? .cloud

        let cloudProviderRaw = UserDefaults.standard.string(forKey: "cloudLLMProvider") ?? CloudLLMProvider.claude.rawValue
        self.cloudLLMProvider = CloudLLMProvider(rawValue: cloudProviderRaw) ?? .claude

        self.ollamaURL = UserDefaults.standard.string(forKey: "ollamaURL") ?? ""

        let autoDeleteRaw = UserDefaults.standard.string(forKey: "autoDeleteAudio") ?? AutoDeleteOption.off.rawValue
        self.autoDeleteOption = AutoDeleteOption(rawValue: autoDeleteRaw) ?? .off
        self.autoDeleteAudio = autoDeleteOption

        // Sync with AIConfiguration
        AIConfiguration.transcriptionSource = transcriptionSource
        AIConfiguration.llmSource = llmSource
        AIConfiguration.cloudLLMProvider = cloudLLMProvider
        AIConfiguration.ollamaURL = ollamaURL.isEmpty ? nil : ollamaURL
    }

    // MARK: - API Keys

    var hasOpenAIKey: Bool {
        AIConfiguration.openAIKey != nil
    }

    var hasAnthropicKey: Bool {
        AIConfiguration.anthropicKey != nil
    }

    func saveOpenAIKey(_ key: String) {
        AIConfiguration.openAIKey = key.isEmpty ? nil : key
    }

    func saveAnthropicKey(_ key: String) {
        AIConfiguration.anthropicKey = key.isEmpty ? nil : key
    }
}
