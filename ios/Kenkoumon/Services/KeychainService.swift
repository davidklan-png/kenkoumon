//
//  KeychainService.swift
//  Kenkoumon
//
//  Secure storage for API keys and sensitive data.
//

import Security
import Foundation

class KeychainService {
    static let shared = KeychainService()

    private let service = "com.kenkoumon.keys"

    private init() {}

    // MARK: - Save

    /// Save a string value to keychain
    func save(key: String, value: String) -> Bool {
        guard let data = value.data(using: .utf8) else { return false }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]

        // Delete existing item first
        SecItemDelete(query as CFDictionary)

        // Add new item
        let status = SecItemAdd(query as CFDictionary, nil)
        return status == errSecSuccess
    }

    /// Save data to keychain
    func save(key: String, data: Data) -> Bool {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]

        SecItemDelete(query as CFDictionary)

        let status = SecItemAdd(query as CFDictionary, nil)
        return status == errSecSuccess
    }

    // MARK: - Retrieve

    /// Get a string value from keychain
    func get(key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        if status == errSecSuccess,
           let data = result as? Data {
            return String(data: data, encoding: .utf8)
        }
        return nil
    }

    /// Get data from keychain
    func getData(key: String) -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        if status == errSecSuccess {
            return result as? Data
        }
        return nil
    }

    // MARK: - Delete

    /// Delete a value from keychain
    func delete(key: String) -> Bool {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key
        ]

        let status = SecItemDelete(query as CFDictionary)
        return status == errSecSuccess
    }

    /// Delete all keychain items for this app
    func deleteAll() -> Bool {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service
        ]

        let status = SecItemDelete(query as CFDictionary)
        return status == errSecSuccess
    }

    // MARK: - Update

    /// Update an existing value in keychain
    func update(key: String, value: String) -> Bool {
        guard let data = value.data(using: .utf8) else { return false }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key
        ]

        let attributes: [String: Any] = [
            kSecValueData as String: data
        ]

        let status = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)
        return status == errSecSuccess
    }

    // MARK: - Convenience Methods for API Keys

    /// OpenAI API Key
    var openAIKey: String? {
        get { get(key: "openai_key") }
        set { _ = save(key: "openai_key", value: newValue ?? "") }
    }

    /// Anthropic API Key
    var anthropicKey: String? {
        get { get(key: "anthropic_key") }
        set { _ = save(key: "anthropic_key", value: newValue ?? "") }
    }

    /// User-hosted Ollama URL
    var ollamaURL: String? {
        get { get(key: "ollama_url") }
        set { _ = save(key: "ollama_url", value: newValue ?? "") }
    }

    /// Backend API URL
    var apiURL: String? {
        get { get(key: "api_url") }
        set { _ = save(key: "api_url", value: newValue ?? "") }
    }

    /// Auth token
    var authToken: String? {
        get { get(key: "auth_token") }
        set { _ = save(key: "auth_token", value: newValue ?? "") }
    }
}
