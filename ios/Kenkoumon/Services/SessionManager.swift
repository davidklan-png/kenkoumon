//
//  SessionManager.swift
//  Kenkoumon
//
//  Recording session management.
//

import Foundation
import Combine

@MainActor
class SessionManager: ObservableObject {
    @Published var sessions: [Session] = []
    @Published var currentSession: Session?
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let apiService = APIService()

    // MARK: - CRUD

    func loadSessions() async throws {
        isLoading = true
        defer { isLoading = false }

        let response: [Session] = try await apiService.request(
            endpoint: "/sessions",
            method: .GET
        )

        self.sessions = response
    }

    func createSession(date: Date = Date()) async throws {
        isLoading = true
        defer { isLoading = false }

        let request = SessionCreateRequest(date: date)
        let session: Session = try await apiService.request(
            endpoint: "/sessions",
            method: .POST,
            body: request
        )

        self.currentSession = session
        self.sessions.insert(session, at: 0)
    }

    func updateSessionNotes(_ notes: String) async throws {
        guard let session = currentSession else { return }

        let request = SessionUpdateRequest(patientNotes: notes)
        let updated: Session = try await apiService.request(
            endpoint: "/sessions/\(session.id)",
            method: .PATCH,
            body: request
        )

        self.currentSession = updated
        if let index = sessions.firstIndex(where: { $0.id == session.id }) {
            sessions[index] = updated
        }
    }

    func deleteSession(_ session: Session) async throws {
        isLoading = true
        defer { isLoading = false }

        let _: EmptyResponse = try await apiService.request(
            endpoint: "/sessions/\(session.id)",
            method: .DELETE
        )

        sessions.removeAll { $0.id == session.id }
        if currentSession?.id == session.id {
            currentSession = nil
        }
    }

    // MARK: - Processing

    func uploadAudio(fileURL: URL, source: String? = nil) async throws {
        guard let session = currentSession else {
            throw APIError.notFound
        }

        isLoading = true
        defer { isLoading = false }

        let updated: Session = try await apiService.uploadAudio(
            sessionId: session.id,
            audioFileURL: fileURL,
            transcriptionSource: source
        )

        self.currentSession = updated
        updateSessionInList(updated)
    }

    func transcribe(source: String = "cloud") async throws {
        guard let session = currentSession else { throw APIError.notFound }

        isLoading = true
        defer { isLoading = false }

        let updated: Session = try await apiService.request(
            endpoint: "/sessions/\(session.id)/transcribe?source=\(source)",
            method: .POST
        )

        self.currentSession = updated
        updateSessionInList(updated)
    }

    func generateReport(source: String = "cloud", provider: String = "claude") async throws {
        guard let session = currentSession else { throw APIError.notFound }

        isLoading = true
        defer { isLoading = false }

        let updated: Session = try await apiService.request(
            endpoint: "/sessions/\(session.id)/generate?source=\(source)&cloud_provider=\(provider)",
            method: .POST
        )

        self.currentSession = updated
        updateSessionInList(updated)
    }

    func pollForUpdates() async throws {
        guard let session = currentSession,
              session.status.isProcessing else { return }

        let updated: Session = try await apiService.request(
            endpoint: "/sessions/\(session.id)"
        )

        self.currentSession = updated
        updateSessionInList(updated)

        if updated.status.isProcessing {
            try? await Task.sleep(nanoseconds: 5_000_000_000) // 5 seconds
            try await pollForUpdates()
        }
    }

    // MARK: - Private

    private func updateSessionInList(_ session: Session) {
        if let index = sessions.firstIndex(where: { $0.id == session.id }) {
            sessions[index] = session
        } else {
            sessions.insert(session, at: 0)
        }
    }
}

struct EmptyResponse: Codable {}
