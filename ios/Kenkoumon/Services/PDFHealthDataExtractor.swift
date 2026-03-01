//
//  PDFHealthDataExtractor.swift
//  Kenkoumon
//
//  Extract health data from MyNumber Portal PDFs.
//

import Foundation
import PDFKit
import NaturalLanguage

class PDFHealthDataExtractor {
    static let shared = PDFHealthDataExtractor()

    private init() {}

    func extract(from url: URL) async throws -> ExtractedHealthData {
        guard let document = PDFDocument(url: url) else {
            throw ExtractionError.invalidPDF
        }

        let text = extractText(from: document)
        let data = parseHealthData(from: text)

        return data
    }

    private func extractText(from document: PDFDocument) -> String {
        var text = ""

        for pageIndex in 0..<document.pageCount {
            if let page = document.page(at: pageIndex) {
                text += page.string ?? ""
            }
        }

        return text
    }

    private func parseHealthData(from text: String) -> ExtractedHealthData {
        var data = ExtractedHealthData()

        // Parse health checkup data
        data.height = extractValue(pattern: "身長[：:]\\s*(\\d+\\.?\\d*)", from: text, unit: "cm")
        data.weight = extractValue(pattern: "体重[：:]\\s*(\\d+\\.?\\d*)", from: text, unit: "kg")
        data.bmi = extractValue(pattern: "BMI[：:]\\s*(\\d+\\.?\\d*)", from: text)

        // Blood pressure (e.g., "血圧 120/80")
        if let bpRange = text.range(of: "血圧[：:]\\s*(\\d+)[/／](\\d+)", options: .regularExpression) {
            let bpText = String(text[bpRange])
            if let systolic = extractValue(pattern: "(\\d+)[/／]", from: bpText),
               let diastolic = extractValue(pattern: "[/／](\\d+)", from: bpText) {
                data.bloodPressureSystolic = Int(systolic)
                data.bloodPressureDiastolic = Int(diastolic)
            }
        }

        // Blood sugar
        data.bloodSugar = extractValue(pattern: "血糖値?|空腹時血糖[：:]\\s*(\\d+\\.?\\d*)", from: text)

        // HbA1c
        data.hba1c = extractValue(pattern: "HbA1c|ヘモグロビンA1c[：:]\\s*(\\d+\\.?\\d*)", from: text)

        // Cholesterol
        data.ldlCholesterol = extractValue(pattern: "LDLコレステロール|悪玉コレステロール[：:]\\s*(\\d+\\.?\\d*)", from: text)
        data.hdlCholesterol = extractValue(pattern: "HDLコレステロール|善玉コレステロール[：:]\\s*(\\d+\\.?\\d*)", from: text)
        data.triglycerides = extractValue(pattern: "中性脂肪|トリグリセリド[：:]\\s*(\\d+\\.?\\d*)", from: text)

        // Liver enzymes
        data.ast = extractValue(pattern: "AST|GOT[：:]\\s*(\\d+\\.?\\d*)", from: text)
        data.alt = extractValue(pattern: "ALT|GPT[：:]\\s*(\\d+\\.?\\d*)", from: text)
        data.gammaGtp = extractValue(pattern: "γ-GTP|ガンマGTP[：:]\\s*(\\d+\\.?\\d*)", from: text)

        return data
    }

    private func extractValue(pattern: String, from text: String, unit: String? = nil) -> Double? {
        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
            return nil
        }

        let range = NSRange(location: 0, length: text.utf16.count)
        guard let match = regex.firstMatch(in: text, options: [], range: range),
              let valueRange = Range(match.range(at: 1), in: text) else {
            return nil
        }

        let valueString = String(text[valueRange]).replacingOccurrences(of: ",", with: "")
        return Double(valueString)
    }

    enum ExtractionError: Error {
        case invalidPDF
        case noDataFound
    }
}
