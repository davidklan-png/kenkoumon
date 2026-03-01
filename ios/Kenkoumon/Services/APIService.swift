//
//  APIService.swift
//  Kenkoumon
//
//  HTTP client for backend API communication.
//

import Foundation

enum HTTPMethod: String {
    case GET
    case POST
    case PATCH
    case DELETE
}

class APIService {
    static let shared = APIService()

    private let baseURL: String
    private let session: URLSession
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder

    init() {
        self.baseURL = APIConfig.baseURL

        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = APIConfig.timeout
        self.session = URLSession(configuration: configuration)

        self.decoder = JSONDecoder()
        self.decoder.dateDecodingStrategy = .iso8601

        self.encoder = JSONEncoder()
        self.encoder.dateEncodingStrategy = .iso8601
    }

    // MARK: - Request

    func request<T: Decodable>(
        endpoint: String,
        method: HTTPMethod = .GET,
        body: Encodable? = nil,
        requiresAuth: Bool = true
    ) async throws -> T {
        let url = URL(string: baseURL + "/api/\(APIConfig.apiVersion)" + endpoint)!
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        // Add auth token
        if requiresAuth,
           let token = KeychainService.shared.authToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        // Add body
        if let body = body {
            request.httpBody = try encoder.encode(body)
        }

        // Perform request
        let (data, response) = try await session.data(for: request)

        // Handle response
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        switch httpResponse.statusCode {
        case 200...299:
            return try decoder.decode(T.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            throw APIError.serverError(httpResponse.statusCode)
        }
    }

    // MARK: - Multipart Upload

    func uploadAudio(
        sessionId: String,
        audioFileURL: URL,
        transcriptionSource: String? = nil
    ) async throws -> Session {
        let url = URL(string: baseURL + "/api/\(APIConfig.apiVersion)/sessions/\(sessionId)/audio")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        if let token = KeychainService.shared.authToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()

        // Add transcription source if provided
        if let source = transcriptionSource {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"transcription_source\"\r\n\r\n".data(using: .utf8)!)
            body.append("\(source)\r\n".data(using: .utf8)!)
        }

        // Add audio file
        let audioData = try Data(contentsOf: audioFileURL)
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"audio.m4a\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: audio/m4a\r\n\r\n".data(using: .utf8)!)
        body.append(audioData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.uploadFailed
        }

        return try decoder.decode(Session.self, from: data)
    }
}

// MARK: - Errors

enum APIError: LocalizedError {
    case invalidResponse
    case unauthorized
    case notFound
    case serverError(Int)
    case uploadFailed
    case networkError(Error)

    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "無効なレスポンスです"
        case .unauthorized:
            return "認証に失敗しました"
        case .notFound:
            return "見つかりませんでした"
        case .serverError(let code):
            return "サーバーエラー: \(code)"
        case .uploadFailed:
            return "アップロードに失敗しました"
        case .networkError(let error):
            return error.localizedDescription
        }
    }
}
