//
//  AuthManager.swift
//  Kenkoumon
//
//  Authentication state management.
//

import Foundation
import Combine

class AuthManager: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: Patient?
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let apiService = APIService()
    private var cancellables = Set<AnyCancellable>()

    init() {
        checkExistingAuth()
    }

    // MARK: - Authentication

    func register(email: String, password: String, fullName: String?) async throws {
        isLoading = true
        defer { isLoading = false }

        let request = RegisterRequest(
            email: email,
            password: password,
            fullName: fullName
        )

        let response: TokenResponse = try await apiService.request(
            endpoint: "/auth/register",
            method: .POST,
            body: request
        )

        KeychainService.shared.authToken = response.accessToken
        await fetchCurrentUser()
    }

    func login(email: String, password: String) async throws {
        isLoading = true
        defer { isLoading = false }

        let request = LoginRequest(email: email, password: password)
        let response: TokenResponse = try await apiService.request(
            endpoint: "/auth/login",
            method: .POST,
            body: request
        )

        KeychainService.shared.authToken = response.accessToken
        await fetchCurrentUser()
    }

    func logout() {
        KeychainService.shared.authToken = nil
        isAuthenticated = false
        currentUser = nil
    }

    // MARK: - Private

    private func checkExistingAuth() {
        if KeychainService.shared.authToken != nil {
            Task {
                await fetchCurrentUser()
            }
        }
    }

    private func fetchCurrentUser() async {
        do {
            let user: Patient = try await apiService.request(endpoint: "/auth/me")
            await MainActor.run {
                self.currentUser = user
                self.isAuthenticated = true
            }
        } catch {
            await MainActor.run {
                self.isAuthenticated = false
                self.errorMessage = error.localizedDescription
            }
        }
    }
}

// MARK: - Request/Response Models

struct Patient: Identifiable, Codable {
    let id: String
    let email: String
    let fullName: String?
    let createdAt: Date
}

struct RegisterRequest: Codable {
    let email: String
    let password: String
    let fullName: String?
}

struct LoginRequest: Codable {
    let email: String
    let password: String
}

struct TokenResponse: Codable {
    let accessToken: String
    let tokenType: String
}
