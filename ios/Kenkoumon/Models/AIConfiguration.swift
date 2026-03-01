//
//  AIConfiguration.swift
//  Kenkoumon
//
//  AI service configuration.
//

import Foundation

enum AISource: String, CaseIterable {
    case onDevice = "On-device"
    case userHosted = "User-hosted"
    case cloud = "Cloud"

    var displayString: String {
        rawValue
    }
}

enum CloudLLMProvider: String, CaseIterable {
    case claude = "Claude"
    case gpt = "GPT-4"
}

struct AIConfiguration {
    // Transcription
    static var transcriptionSource: AISource = .cloud
    static let openAIAudioFormat = "m4a"
    static let transcriptionLanguage = "ja"

    // Report Generation
    static var llmSource: AISource = .cloud
    static var cloudLLMProvider: CloudLLMProvider = .claude

    // API Keys (stored in Keychain)
    static var openAIKey: String? {
        get { KeychainService.shared.get(key: "openai_key") }
        set { KeychainService.shared.save(key: "openai_key", value: newValue ?? "") }
    }

    static var anthropicKey: String? {
        get { KeychainService.shared.get(key: "anthropic_key") }
        set { KeychainService.shared.save(key: "anthropic_key", value: newValue ?? "") }
    }

    // User-Hosted
    static var ollamaURL: String? {
        get { KeychainService.shared.get(key: "ollama_url") }
        set { KeychainService.shared.save(key: "ollama_url", value: newValue ?? "") }
    }

    static var ollamaModel = "llama3.1"

    // On-Device Models
    static let whisperModelName = "whisper-large-v3"
    static let llamaModelName = "llama-3.1-8b-instruct-q4_0"
}
