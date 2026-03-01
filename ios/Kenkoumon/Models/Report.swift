//
//  Report.swift
//  Kenkoumon
//
//  Medical report model.
//

import Foundation

struct Report: Identifiable, Codable {
    let id: String
    let date: Date
    let status: Session.SessionStatus
    let transcriptJa: String?
    let reportJa: String?
    var patientNotes: String?
    let entities: ReportEntities
}

struct ReportEntities: Codable {
    let medications: [Medication]
    let conditions: [Condition]
    let instructions: [Instruction]
    let providers: [Provider]
}

struct Medication: Identifiable, Codable {
    let id: String
    let nameJa: String
    let nameEn: String?
    let dosage: String?
    let status: String
    let confidence: String?
    let patientConfirmed: Bool
}

struct Condition: Identifiable, Codable {
    let id: String
    let nameJa: String
    let nameEn: String?
    let icdCode: String?
    let status: String
    let confidence: String?
    let patientConfirmed: Bool
}

struct Instruction: Identifiable, Codable {
    let id: String
    let contentJa: String
    let category: String
    let dueDate: Date?
    let confidence: String?
    let patientConfirmed: Bool
}

struct Provider: Identifiable, Codable {
    let id: String
    let nameJa: String
    let nameEn: String?
    let specialty: String?
    let clinicName: String?
    let firstSeen: Date?
    let lastSeen: Date?
}

struct ShareLink: Identifiable, Codable {
    let id: String
    let token: String
    let expiresAt: Date
    let url: String
}

struct ShareLinkCreateRequest: Codable {
    let expiresInDays: Int
}
