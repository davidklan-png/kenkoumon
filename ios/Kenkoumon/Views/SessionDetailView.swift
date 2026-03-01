//
//  SessionDetailView.swift
//  Kenkoumon
//
//  Detail view for a session with report.
//

import SwiftUI

struct SessionDetailView: View {
    let session: Session
    @Environment(\.dismiss) var dismiss
    @State private var report: Report?
    @State private var shareLink: ShareLink?
    @State private var isLoading = true
    @State private var notes = ""
    @State private var showingShare = false
    @State private var showingQR = false

    var body: some View {
        NavigationStack {
            ScrollView {
                if isLoading {
                    ProgressView()
                } else if let report = report {
                    reportContent(report)
                }
            }
            .navigationTitle("レポート")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("閉じる") { dismiss() }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button {
                        showingShare = true
                    } label: {
                        Image(systemName: "square.and.arrow.up")
                    }
                    .disabled(session.status != .complete)
                }
            }
            .sheet(isPresented: $showingShare) {
                ShareSheet(shareLink: shareLink)
            }
        }
        .task {
            await loadReport()
        }
    }

    private func reportContent(_ report: Report) -> some View {
        VStack(alignment: .leading, spacing: 24) {
            // Date
            Text(report.date, format: .dateTime.year().month().day().hour().minute())
                .foregroundStyle(.secondary)

            // Section 1: 診察内容の要約
            SectionView(
                title: "診察内容の要約",
                content: report.reportJa ?? "",
                isEditable: false
            )

            // Section 2: 主な医療情報
            SectionView(
                title: "主な医療情報",
                content: entitiesText(report.entities),
                isEditable: false
            )

            // Section 3: 次回診察に向けて
            SectionView(
                title: "次回診察に向けて",
                content: extractInstructions(report.reportJa ?? ""),
                isEditable: false
            )

            // Section 4: 患者からのメモ (Editable)
            SectionView(
                title: "患者からのメモ",
                content: notes,
                placeholder: "自分用のメモを追加...",
                isEditable: true
            ) { newNotes in
                notes = newNotes
                Task {
                    await saveNotes(newNotes)
                }
            }

            // Share Link Section
            if session.status == .complete {
                VStack(alignment: .leading, spacing: 12) {
                    Text("医師と共有")
                        .font(.headline)

                    if let link = shareLink {
                        VStack(spacing: 12) {
                            Button("リンクをコピー") {
                                UIPasteboard.general.string = link.url
                            }
                            .buttonStyle(.bordered)

                            Button("QRコードを表示") {
                                showingQR = true
                            }
                            .buttonStyle(.bordered)
                        }
                    } else {
                        Button("共有リンクを作成") {
                            Task { await createShareLink() }
                        }
                        .buttonStyle(.borderedProminent)
                    }
                }
                .padding()
                .background(Color(.systemGray6))
                .clipShape(RoundedRectangle(cornerRadius: 12))
            }
        }
        .padding()
        .sheet(isPresented: $showingQR) {
            if let link = shareLink {
                QRCodeView(url: link.url)
            }
        }
    }

    private func entitiesText(_ entities: ReportEntities) -> String {
        var text = ""

        if !entities.medications.isEmpty {
            text += "【薬剤】\n"
            for med in entities.medications {
                text += "• \(med.nameJa)"
                if let dosage = med.dosage {
                    text += " \(dosage)"
                }
                text += "\n"
            }
            text += "\n"
        }

        if !entities.conditions.isEmpty {
            text += "【病名・疾患】\n"
            for cond in entities.conditions {
                text += "• \(cond.nameJa)\n"
            }
            text += "\n"
        }

        if !entities.providers.isEmpty {
            text += "【医師】\n"
            for prov in entities.providers {
                text += "• \(prov.nameJa)"
                if let clinic = prov.clinicName {
                    text += " (\(clinic))"
                }
                text += "\n"
            }
        }

        return text
    }

    private func extractInstructions(_ report: String) -> String {
        // Simple extraction - in production, parse properly
        if let range = report.range(of: "次回診察に向けて") {
            let start = range.upperBound
            if let end = report[start...].range(of: "\n\n#") {
                return String(report[start..<end.lowerBound]).trimmingCharacters(in: .whitespaces)
            }
        }
        return ""
    }

    private func loadReport() async {
        do {
            // Load notes
            notes = session.patientNotes ?? ""

            // If report exists, show it
            if session.status == .complete, let reportText = session.reportJa {
                report = Report(
                    id: session.id,
                    date: session.date,
                    status: session.status,
                    transcriptJa: session.transcriptJa,
                    reportJa: reportText,
                    patientNotes: session.patientNotes,
                    entities: ReportEntities(
                        medications: [],
                        conditions: [],
                        instructions: [],
                        providers: []
                    )
                )
            }

            // Load share link if exists
            if session.status == .complete {
                // TODO: Load existing share links
            }

            isLoading = false
        } catch {
            isLoading = false
        }
    }

    private func saveNotes(_ newNotes: String) async {
        // TODO: Update via API
    }

    private func createShareLink() async {
        // TODO: Create share link via API
    }
}

struct SectionView: View {
    let title: String
    let content: String
    var placeholder: String = ""
    let isEditable: Bool
    var onUpdate: ((String) -> Void)?

    @State private var isEditing = false
    @State private var editText = ""

    init(title: String, content: String, placeholder: String = "", isEditable: Bool, onUpdate: ((String) -> Void)? = nil) {
        self.title = title
        self.content = content
        self.placeholder = placeholder
        self.isEditable = isEditable
        self.onUpdate = onUpdate
        self._editText = State(initialValue: content)
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(title)
                    .font(.headline)

                if isEditable {
                    Spacer()
                    Button(isEditing ? "完了" : "編集") {
                        if isEditing {
                            onUpdate?(editText)
                        }
                        isEditing.toggle()
                    }
                    .font(.caption)
                }
            }

            if isEditable && isEditing {
                TextEditor(text: $editText)
                    .frame(minHeight: 100)
                    .padding(8)
                    .background(Color(.systemGray6))
                    .clipShape(RoundedRectangle(cornerRadius: 8))
            } else {
                Text(content.isEmpty ? placeholder : content)
                    .foregroundStyle(content.isEmpty ? .secondary : .primary)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(Color(.systemGray6))
                    .clipShape(RoundedRectangle(cornerRadius: 8))
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

// MARK: - Share Sheet

struct ShareSheet: UIViewControllerRepresentable {
    let shareLink: ShareLink?

    func makeUIViewController(context: Context) -> UIActivityViewController {
        let items: [Any] = if let link = shareLink {
            [link.url]
        } else {
            []
        }

        return UIActivityViewController(
            activityItems: items,
            applicationActivities: nil
        )
    }

    func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {}
}

// MARK: - QR Code View

struct QRCodeView: View {
    let url: String
    @Environment(\.dismiss) var dismiss

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Text("医師と共有")
                    .font(.headline)

                if let qrImage = generateQRCode(from: url) {
                    Image(uiImage: qrImage)
                        .interpolation(.none)
                        .resizable()
                        .scaledToFit()
                        .frame(width: 250, height: 250)
                }

                Text(url)
                    .font(.caption)
                    .foregroundStyle(.secondary)

                Button("閉じる") { dismiss() }
                    .buttonStyle(.borderedProminent)
            }
            .padding()
            .navigationTitle("QRコード")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    private func generateQRCode(from string: String) -> UIImage? {
        let data = string.data(using: .utf8)
        let filter = CIFilter(name: "CIQRCodeGenerator")
        filter?.setValue(data, forKey: "inputMessage")

        if let output = filter?.outputImage {
            let transform = CGAffineTransform(scaleX: 10, y: 10)
            let scaled = output.transformed(by: transform)

            if let cgImage = CIContext().createCGImage(scaled, from: scaled.extent) {
                return UIImage(cgImage: cgImage)
            }
        }
        return nil
    }
}
