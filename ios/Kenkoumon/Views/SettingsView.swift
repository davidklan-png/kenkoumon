//
//  SettingsView.swift
//  Kenkoumon
//
//  App settings and configuration.
//

import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var authManager: AuthManager
    @EnvironmentObject var settingsManager: SettingsManager
    @State private var showingAPIKeySheet = false
    @State private var apiKeyType = APIKeyType.openai

    var body: some View {
        NavigationStack {
            List {
                // AI Configuration
                Section("AI設定") {
                    Picker("文字起こし", selection: $settingsManager.transcriptionSource) {
                        ForEach(AISource.allCases, id: \.self) { source in
                            Text(source.displayString).tag(source)
                        }
                    }

                    Picker("レポート生成", selection: $settingsManager.llmSource) {
                        ForEach(AISource.allCases, id: \.self) { source in
                            Text(source.displayString).tag(source)
                        }
                    }

                    if settingsManager.llmSource == .cloud {
                        Picker("AIプロバイダー", selection: $settingsManager.cloudLLMProvider) {
                            ForEach(CloudLLMProvider.allCases, id: \.self) { provider in
                                Text(provider.rawValue).tag(provider)
                            }
                        }
                    }

                    if settingsManager.llmSource == .userHosted ||
                       settingsManager.transcriptionSource == .userHosted {
                        HStack {
                            Text("Ollama URL")
                            TextField("http://localhost:11434", text: $settingsManager.ollamaURL)
                                .textInputAutocapitalization(.never)
                                .autocapitalization(.none)
                        }
                    }
                }

                // API Keys
                Section("APIキー") {
                    apiKeyRow(type: .openai, isSet: settingsManager.hasOpenAIKey)
                    apiKeyRow(type: .anthropic, isSet: settingsManager.hasAnthropicKey)
                }

                // Storage
                Section("ストレージ") {
                    Picker("音声の自動削除", selection: $settingsManager.autoDeleteAudio) {
                        ForEach(SettingsManager.AutoDeleteOption.allCases, id: \.self) { option in
                            Text(option.displayString).tag(option)
                        }
                    }
                }

                // Account
                Section("アカウント") {
                    if let user = authManager.currentUser {
                        HStack {
                            Text("メール")
                            Spacer()
                            Text(user.email)
                                .foregroundStyle(.secondary)
                        }

                        if let name = user.fullName {
                            HStack {
                                Text("お名前")
                                Spacer()
                                Text(name)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }

                    Button(role: .destructive) {
                        authManager.logout()
                    } label: {
                        Text("ログアウト")
                    }
                }

                // About
                Section("Kenkoumonについて") {
                    HStack {
                        Text("バージョン")
                        Spacer()
                        Text("0.1.0")
                            .foregroundStyle(.secondary)
                    }

                    Link("利用規約", destination: URL(string: "https://github.com/davidklan-png/kenkoumon")!)
                    Link("プライバシーポリシー", destination: URL(string: "https://github.com/davidklan-png/kenkoumon")!)
                }
            }
            .navigationTitle("設定")
            .sheet(isPresented: $showingAPIKeySheet) {
                APIKeySheet(type: apiKeyType)
            }
        }
    }

    private func apiKeyRow(type: APIKeyType, isSet: Bool) -> some View {
        Button {
            apiKeyType = type
            showingAPIKeySheet = true
        } label: {
            HStack {
                Text(type.displayName)
                Spacer()
                if isSet {
                    Text("設定済み")
                        .foregroundStyle(.green)
                    } else {
                        Text("未設定")
                            .foregroundStyle(.secondary)
                }
                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
    }
}

enum APIKeyType {
    case openai
    case anthropic

    var displayName: String {
        switch self {
        case .openai: return "OpenAI API Key"
        case .anthropic: return "Anthropic API Key"
        }
    }
}

// MARK: - API Key Sheet

struct APIKeySheet: View {
    @Environment(\.dismiss) var dismiss
    let type: APIKeyType
    @EnvironmentObject var settingsManager: SettingsManager
    @State private var apiKey = ""

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    Text(type.displayName + "を入力してください")
                        .foregroundStyle(.secondary)

                    SecureField("API Key", text: $apiKey)
                } header: {
                    Text("APIキー")
                } footer: {
                    Text("キーはデバイスのキーチェーンに安全に保存されます")
                }
            }
            .navigationTitle("APIキー設定")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("キャンセル") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("保存") {
                        saveKey()
                        dismiss()
                    }
                }
            }
            .onAppear {
                loadKey()
            }
        }
    }

    private func loadKey() {
        switch type {
        case .openai:
            apiKey = AIConfiguration.openAIKey ?? ""
        case .anthropic:
            apiKey = AIConfiguration.anthropicKey ?? ""
        }
    }

    private func saveKey() {
        switch type {
        case .openai:
            settingsManager.saveOpenAIKey(apiKey)
        case .anthropic:
            settingsManager.saveAnthropicKey(apiKey)
        }
    }
}
