//
//  HealthDocument.swift
//  Kenkoumon
//
//  Imported health document from MyNumber Portal.
//

import Foundation
import SwiftUI

struct HealthDocument: Identifiable, Codable, Equatable {
    let id: String
    let patientId: String
    let fileName: String
    let fileType: DocumentType
    let uploadDate: Date
    var documentDate: Date?
    var category: DocumentCategory?
    var extractedData: ExtractedHealthData?
    var summary: String?
    var tags: [String]

    var fileURL: URL? {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first?
            .appendingPathComponent("health_documents")
            .appendingPathComponent(id)
            .appendingPathExtension("pdf")
    }

    enum DocumentType: String, Codable {
        case pdf = "application/pdf"
        case image = "image/jpeg"
        case text = "text/plain"

        var displayString: String {
            switch self {
            case .pdf: return "PDF"
            case .image: return "画像"
            case .text: return "テキスト"
            }
        }
    }

    enum DocumentCategory: String, Codable, CaseIterable {
        case healthCheckup = "健康診断"
        case medication = "お薬手帳"
        case vaccination = "予防接種"
        case labResults = "検査結果"
        case medicalCertificate = "診断書"
        case other = "その他"

        var displayString: String {
            rawValue
        }

        var icon: String {
            switch self {
            case .healthCheckup: return "stethoscope"
            case .medication: return "pills"
            case .vaccination: return "syringe"
            case .labResults: return "testtube.2"
            case .medicalCertificate: return "doc.text"
            case .other: return "doc"
            }
        }
    }
}

struct ExtractedHealthData: Codable {
    // Health checkup data
    var checkupDate: Date?
    var height: Double?
    var weight: Double?
    var bmi: Double?
    var bloodPressureSystolic: Int?
    var bloodPressureDiastolic: Int?
    var bloodSugar: Double?
    var hba1c: Double?
    var ldlCholesterol: Double?
    var hdlCholesterol: Double?
    var triglycerides: Double?
    var ast: Double?
    var alt: Double?
    var gammaGtp: Double?

    // Medication data
    var medications: [MedicationRecord]?

    // Vaccination data
    var vaccinations: [VaccinationRecord]?

    struct MedicationRecord: Codable {
        let name: String
        let dosage: String?
        let startDate: Date?
        let endDate: Date?
    }

    struct VaccinationRecord: Codable {
        let name: String
        let date: Date?
    }
}

struct HealthDocumentCreateRequest: Codable {
    let fileName: String
    let fileType: String
    let category: String?
    let documentDate: Date?
}

struct HealthDocumentUpdateRequest: Codable {
    var category: String?
    var summary: String?
    var tags: [String]?
}
