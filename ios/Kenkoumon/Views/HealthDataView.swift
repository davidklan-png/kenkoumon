//
//  HealthDataView.swift
//  Kenkoumon
//
//  View for health documents and history.
//

import SwiftUI

struct HealthDataView: View {
    @EnvironmentObject var documentManager: HealthDocumentManager
    @State private var showingImporter = false
    @State private var selectedDocument: HealthDocument?
    @State private var showingSummary = false

    var body: some View {
        NavigationStack {
            List {
                // Summary Card
                summaryCard

                // Documents Section
                Section {
                    if documentManager.documents.isEmpty {
                        emptyState
                    } else {
                        ForEach(documentManager.documents) { document in
                            DocumentRow(document: document)
                                .contentShape(Rectangle())
                                .onTapGesture {
                                    selectedDocument = document
                                }
                        }
                        .onDelete(perform: deleteDocuments)
                    }
                } header: {
                    Text("ドキュメント")
                }
            }
            .navigationTitle("健康データ")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button {
                        showingImporter = true
                    } label: {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingImporter) {
                HealthDocumentImporter(isPresented: $showingImporter) { urls in
                    Task {
                        try? await documentManager.importDocuments(from: urls)
                    }
                }
            }
            .sheet(item: $selectedDocument) { document in
                DocumentDetailView(document: document)
            }
            .sheet(isPresented: $showingSummary) {
                HealthSummaryView()
            }
            .onAppear {
                if documentManager.documents.isEmpty {
                    Task {
                        try? await documentManager.loadDocuments()
                    }
                }
            }
        }
    }

    private var summaryCard: some View {
        Section {
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Text("健康サマリー")
                        .font(.headline)
                    Spacer()
                    Button("詳細") {
                        showingSummary = true
                    }
                    .font(.caption)
                }

                let summary = documentManager.getHealthSummary()

                Grid(alignment: .leading, horizontalSpacing: 16, verticalSpacing: 8) {
                    GridRow {
                        Text("身長")
                            .foregroundStyle(.secondary)
                        if let height = summary.latestHeight {
                            Text("\(String(format: "%.1f", height)) cm")
                        }
                    }

                    GridRow {
                        Text("体重")
                            .foregroundStyle(.secondary)
                        if let weight = summary.latestWeight {
                            Text("\(String(format: "%.1f", weight)) kg")
                        }
                    }

                    GridRow {
                        Text("BMI")
                            .foregroundStyle(.secondary)
                        if let bmi = summary.latestBMI {
                            let bmiValue = String(format: "%.1f", bmi)
                            Text(bmiValue)
                            .foregroundStyle(bmiColor(for: bmi))
                        }
                    }

                    GridRow {
                        Text("血圧")
                            .foregroundStyle(.secondary)
                        if let bp = summary.latestBloodPressure {
                            Text(bp)
                        }
                    }
                }
            }
            .padding()
            .background(Color(.systemGray6))
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .listRowInsets(EdgeInsets())
        }
    }

    private func bmiColor(for bmi: Double) -> Color {
        switch bmi {
        case 0..<18.5: return .blue
        case 18.5..<25: return .green
        case 25..<30: return .orange
        default: return .red
        }
    }

    private var emptyState: some View {
        VStack(spacing: 16) {
            Image(systemName: "doc.text")
                .font(.system(size: 60))
                .foregroundStyle(.secondary)

            Text("健康データがありません")
                .font(.headline)

            Text("MyNumber Portalからダウンロードした\nPDFをインポートできます")
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
        .listRowSeparator(.hidden)
    }

    private func deleteDocuments(at offsets: IndexSet) {
        Task {
            for index in offsets {
                try? await documentManager.deleteDocument(documentManager.documents[index])
            }
        }
    }
}

struct DocumentRow: View {
    let document: HealthDocument

    var body: some View {
        HStack(spacing: 12) {
            // Icon
            Image(systemName: document.category?.icon ?? "doc")
                .font(.title2)
                .foregroundStyle(.blue)
                .frame(width: 40, height: 40)
                .background(Color.blue.opacity(0.1))
                .clipShape(Circle())

            // Info
            VStack(alignment: .leading, spacing: 4) {
                Text(document.fileName)
                    .font(.headline)

                Text(document.uploadDate, format: .dateTime.year().month().day())
                    .foregroundStyle(.secondary)
                    .font(.caption)
            }

            Spacer()

            // Category badge
            if let category = document.category {
                Text(category.displayString)
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color(.systemGray6))
                    .clipShape(Capsule())
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - Document Detail View

struct DocumentDetailView: View {
    @Environment(\.dismiss) var dismiss
    let document: HealthDocument
    @EnvironmentObject var documentManager: HealthDocumentManager
    @State private var summary: String = ""
    @State private var selectedCategory: HealthDocument.DocumentCategory?

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    // Header
                    VStack(alignment: .leading, spacing: 8) {
                        Text(document.fileName)
                            .font(.title2)
                            .fontWeight(.bold)

                        HStack {
                            Text(document.uploadDate, format: .dateTime.year().month().day())
                                .foregroundStyle(.secondary)
                            if let date = document.documentDate {
                                Text("•")
                                Text(date, format: .dateTime.year().month().day())
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }

                    // Category Picker
                    VStack(alignment: .leading, spacing: 8) {
                        Text("カテゴリー")
                            .font(.headline)

                        Picker("カテゴリー", selection: $selectedCategory) {
                            Text("選択しない").tag(nil as HealthDocument.DocumentCategory?)
                            ForEach(HealthDocument.DocumentCategory.allCases, id: \.self) { category in
                                Text(category.displayString).tag(category as HealthDocument.DocumentCategory?)
                            }
                        }
                        .pickerStyle(.menu)
                    }

                    // Extracted Data
                    if let data = document.extractedData {
                        extractedDataView(data)
                    }

                    // Notes
                    VStack(alignment: .leading, spacing: 8) {
                        Text("メモ")
                            .font(.headline)

                        TextEditor(text: $summary)
                            .frame(minHeight: 100)
                            .padding(8)
                            .background(Color(.systemGray6))
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                    }

                    // Save Button
                    Button {
                        Task {
                            try? await documentManager.updateDocument(
                                document,
                                summary: summary.isEmpty ? nil : summary,
                                category: selectedCategory
                            )
                            dismiss()
                        }
                    } label: {
                        Text("保存")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
            }
            .navigationTitle("ドキュメント詳細")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("閉じる") { dismiss() }
                }
            }
        }
        .onAppear {
            summary = document.summary ?? ""
            selectedCategory = document.category
        }
    }

    private func extractedDataView(_ data: ExtractedHealthData) -> some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("抽出されたデータ")
                .font(.headline)

            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: 12) {
                if let height = data.height {
                    DataPoint(label: "身長", value: "\(String(format: "%.1f", height)) cm")
                }
                if let weight = data.weight {
                    DataPoint(label: "体重", value: "\(String(format: "%.1f", weight)) kg")
                }
                if let bmi = data.bmi {
                    DataPoint(label: "BMI", value: String(format: "%.1f", bmi))
                }
                if let systolic = data.bloodPressureSystolic, let diastolic = data.bloodPressureDiastolic {
                    DataPoint(label: "血圧", value: "\(systolic)/\(diastolic)")
                }
                if let sugar = data.bloodSugar {
                    DataPoint(label: "血糖値", value: "\(String(format: "%.0f", sugar)) mg/dL")
                }
                if let hba1c = data.hba1c {
                    DataPoint(label: "HbA1c", value: "\(String(format: "%.1f", hba1c)) %")
                }
                if let ldl = data.ldlCholesterol {
                    DataPoint(label: "LDLコレステロール", value: "\(String(format: "%.0f", ldl)) mg/dL")
                }
                if let hdl = data.hdlCholesterol {
                    DataPoint(label: "HDLコレステロール", value: "\(String(format: "%.0f", hdl)) mg/dL")
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

struct DataPoint: View {
    let label: String
    let value: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(label)
                .font(.caption)
                .foregroundStyle(.secondary)
            Text(value)
                .font(.headline)
        }
        .padding(8)
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}

// MARK: - Health Summary View

struct HealthSummaryView: View {
    @EnvironmentObject var documentManager: HealthDocumentManager
    @Environment(\.dismiss) var dismiss

    var body: some View {
        NavigationStack {
            ScrollView {
                let summary = documentManager.getHealthSummary()

                VStack(alignment: .leading, spacing: 24) {
                    Text("健康データサマリー")
                        .font(.title2)
                        .fontWeight(.bold)

                    // Vitals Section
                    VStack(alignment: .leading, spacing: 16) {
                        Text("バイタル")
                            .font(.headline)

                        VStack(spacing: 12) {
                            if let height = summary.latestHeight {
                                SummaryRow(label: "身長", value: "\(String(format: "%.1f", height)) cm")
                            }
                            if let weight = summary.latestWeight {
                                SummaryRow(label: "体重", value: "\(String(format: "%.1f", weight)) kg")
                            }
                            if let bmi = summary.latestBMI {
                                SummaryRow(label: "BMI", value: String(format: "%.1f", bmi))
                                    .color(bmiColor(for: bmi))
                            }
                            if let bp = summary.latestBloodPressure {
                                SummaryRow(label: "血圧", value: bp)
                            }
                        }
                    }

                    // History Chart (placeholder for future)
                    VStack(alignment: .leading, spacing: 16) {
                        Text("推移")
                            .font(.headline)

                        Text("データが蓄積されるとグラフが表示されます")
                            .foregroundStyle(.secondary)
                    }

                    Button("閉じる") {
                        dismiss()
                    }
                    .buttonStyle(.borderedProminent)
                    .frame(maxWidth: .infinity)
                }
                .padding()
            }
            .navigationTitle("サマリー")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    private func bmiColor(for bmi: Double) -> Color {
        switch bmi {
        case 0..<18.5: return .blue
        case 18.5..<25: return .green
        case 25..<30: return .orange
        default: return .red
        }
    }
}

struct SummaryRow: View {
    let label: String
    let value: String
    var color: Color = .primary

    var body: some View {
        HStack {
            Text(label)
                .foregroundStyle(.secondary)
            Spacer()
            Text(value)
                .foregroundStyle(color)
                .fontWeight(.medium)
        }
    }
}
