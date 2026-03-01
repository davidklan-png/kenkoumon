//
//  Session.swift
//  Kenkoumon
//
//  Recording session model.
//

import Foundation

struct Session: Identifiable, Codable, Equatable {
    let id: String
    let patientId: String
    var date: Date
    var audioReference: String?
    var transcriptJa: String?
    var reportJa: String?
    var patientNotes: String?
    var status: SessionStatus
    let createdAt: Date
    var updatedAt: Date

    enum SessionStatus: String, Codable {
        case uploading = "uploading"
        case uploaded = "uploaded"
        case transcribing = "transcribing"
        case transcribed = "transcribed"
        case generating = "generating"
        case complete = "complete"
        case failed = "failed"
        case transcriptionFailed = "transcription_failed"
        case generationFailed = "generation_failed"

        var displayString: String {
            switch self {
            case .uploading: return "アップロード中"
            case .uploaded: return "アップロード完了"
            case .transcribing: return "文字起こし中"
            case .transcribed: return "文字起こし完了"
            case .generating: return "レポート生成中"
            case .complete: return "完了"
            case .failed: return "失敗"
            case .transcriptionFailed: return "文字起こし失敗"
            case .generationFailed: return "レポート生成失敗"
            }
        }

        var isProcessing: Bool {
            switch self {
            case .uploading, .transcribing, .generating:
                return true
            default:
                return false
            }
        }
    }
}

struct SessionCreateRequest: Codable {
    let date: Date
}

struct SessionUpdateRequest: Codable {
    let patientNotes: String?
}
