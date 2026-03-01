//
//  AudioPermissionManager.swift
//  Kenkoumon
//
//  Handles microphone permission requests.
//

import AVFoundation
import Foundation

class AudioPermissionManager {
    static func requestPermission() {
        AVAudioSession.sharedInstance().requestRecordPermission { granted in
            if granted {
                print("Microphone permission granted")
            } else {
                print("Microphone permission denied")
            }
        }
    }

    static var isAuthorized: Bool {
        AVAudioSession.sharedInstance().recordPermission == .granted
    }
}
