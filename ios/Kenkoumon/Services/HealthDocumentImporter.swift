//
//  HealthDocumentImporter.swift
//  Kenkoumon
//
//  File picker for importing health documents.
//

import SwiftUI
import UniformTypeIdentifiers

struct HealthDocumentImporter: UIViewControllerRepresentable {
    @Binding var isPresented: Bool
    let onDocumentsSelected: ([URL]) -> Void

    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let picker = UIDocumentPickerViewController(
            forOpeningContentTypes: [.pdf, .text],
            asCopy: true
        )
        picker.delegate = context.coordinator
        picker.allowsMultipleSelection = true
        return picker
    }

    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIDocumentPickerDelegate {
        let parent: HealthDocumentImporter

        init(_ parent: HealthDocumentImporter) {
            self.parent = parent
        }

        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            parent.onDocumentsSelected(urls)
            parent.isPresented = false
        }

        func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
            parent.isPresented = false
        }
    }
}
