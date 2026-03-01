//
//  URL+Extensions.swift
//  Kenkoumon
//
//  URL extensions for MIME type detection.
//

import Foundation
import UniformTypeIdentifiers

extension URL {
    var mimeType: String? {
        let ext = pathExtension.lowercased()
        switch ext {
        case "pdf":
            return "application/pdf"
        case "jpg", "jpeg":
            return "image/jpeg"
        case "png":
            return "image/png"
        case "txt", "text":
            return "text/plain"
        case "json":
            return "application/json"
        default:
            return nil
        }
    }
}
