//
//  KenkoumonApp.swift
//  Kenkoumon
//
//  Main app entry point.
//

import SwiftUI

@main
struct KenkoumonApp: App {
    @StateObject private var authManager = AuthManager()
    @StateObject private var settingsManager = SettingsManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authManager)
                .environmentObject(settingsManager)
                .onAppear {
                    configureApp()
                }
        }
    }

    private func configureApp() {
        // Request microphone permission on first launch
        AudioPermissionManager.requestPermission()
    }
}
