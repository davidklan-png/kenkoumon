//
//  Configuration.swift
//  Kenkoumon
//
//  App configuration for different environments.
//

import Foundation

enum Environment: String, CaseIterable {
    case development
    case staging
    case production

    var baseURL: String {
        switch self {
        case .development:
            return "http://localhost:8000"
        case .staging:
            return "https://staging-api.kenkoumon.example.com"
        case .production:
            return "https://api.kenkoumon.example.com"
        }
    }

    var displayString: String {
        rawValue.capitalized
    }
}

struct APIConfig {
    static let environment: Environment = .development
    static let baseURL = environment.baseURL
    static let timeout: TimeInterval = 30.0
    static let apiVersion = "v1"
}
