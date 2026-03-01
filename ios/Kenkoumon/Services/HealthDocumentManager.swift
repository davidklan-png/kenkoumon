//
//  HealthDocumentManager.swift
//  Kenkoumon
//
//  Manage health documents and history.
//

import Foundation
import Combine

@MainActor
class HealthDocumentManager: ObservableObject {
    @Published var documents: [HealthDocument] = []
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let apiService = APIService()

    // Load all documents
    func loadDocuments() async throws {
        isLoading = true
        defer { isLoading = false }

        let response: [HealthDocument] = try await apiService.request(
            endpoint: "/health-documents",
            method: .GET
        )

        self.documents = response.sorted { $0.uploadDate > $1.uploadDate }
    }

    // Import documents from file picker
    func importDocuments(from urls: [URL]) async throws {
        isLoading = true
        defer { isLoading = false }

        for url in urls {
            try await importDocument(from: url)
        }
    }

    private func importDocument(from url: URL) async throws {
        // Read file data
        let data = try Data(contentsOf: url)

        // Extract health data from PDF
        var extractedData: ExtractedHealthData?
        if url.pathExtension.lowercased() == "pdf" {
            extractedData = try? await PDFHealthDataExtractor.shared.extract(from: url)
        }

        // Create request
        let fileName = url.lastPathComponent
        let fileType = url.mimeType ?? "application/pdf"
        let request = HealthDocumentCreateRequest(
            fileName: fileName,
            fileType: fileType,
            category: nil,
            documentDate: extractedData?.checkupDate
        )

        // Upload to backend
        let uploaded: HealthDocument = try await apiService.uploadHealthDocument(
            fileData: data,
            fileName: fileName,
            request: request
        )

        documents.insert(uploaded, at: 0)
    }

    // Update document metadata
    func updateDocument(_ document: HealthDocument, summary: String? = nil, category: HealthDocument.DocumentCategory? = nil) async throws {
        let request = HealthDocumentUpdateRequest(
            category: category?.rawValue,
            summary: summary,
            tags: document.tags
        )

        let updated: HealthDocument = try await apiService.request(
            endpoint: "/health-documents/\(document.id)",
            method: .PATCH,
            body: request
        )

        if let index = documents.firstIndex(where: { $0.id == document.id }) {
            documents[index] = updated
        }
    }

    // Delete document
    func deleteDocument(_ document: HealthDocument) async throws {
        let _: EmptyResponse = try await apiService.request(
            endpoint: "/health-documents/\(document.id)",
            method: .DELETE
        )

        documents.removeAll { $0.id == document.id }
    }

    // Get health summary across all documents
    func getHealthSummary() -> HealthSummary {
        var summary = HealthSummary()

        for document in documents {
            guard let data = document.extractedData else { continue }

            // Latest values
            if let height = data.height {
                summary.latestHeight = height
            }
            if let weight = data.weight {
                summary.latestWeight = weight
            }
            if let bmi = data.bmi {
                summary.latestBMI = bmi
            }
            if let systolic = data.bloodPressureSystolic,
               let diastolic = data.bloodPressureDiastolic {
                summary.latestBloodPressure = "\(systolic)/\(diastolic)"
            }
        }

        return summary
    }
}

struct HealthSummary {
    var latestHeight: Double?
    var latestWeight: Double?
    var latestBMI: Double?
    var latestBloodPressure: String?
    var lastCheckupDate: Date?
}
