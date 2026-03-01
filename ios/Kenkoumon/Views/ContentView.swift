//
//  ContentView.swift
//  Kenkoumon
//
//  Main view that routes to authentication or main app.
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var authManager: AuthManager

    var body: some View {
        Group {
            if authManager.isAuthenticated {
                MainTabView()
            } else {
                AuthView()
            }
        }
    }
}

struct MainTabView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            SessionListView()
                .tabItem {
                    Image(systemName: "list.bullet")
                    Text("セッション")
                }
                .tag(0)

            RecordingView()
                .tabItem {
                    Image(systemName: "mic.circle.fill")
                    Text("録音")
                }
                .tag(1)

            SettingsView()
                .tabItem {
                    Image(systemName: "gearshape")
                    Text("設定")
                }
                .tag(2)
        }
        .accentColor(.blue)
    }
}
