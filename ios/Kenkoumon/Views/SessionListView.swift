//
//  SessionListView.swift
//  Kenkoumon
//
//  List of recording sessions.
//

import SwiftUI

struct SessionListView: View {
    @EnvironmentObject var sessionManager: SessionManager
    @State private var selectedSession: Session?
    @State private var showingDeleteAlert = false

    var body: some View {
        NavigationStack {
            Group {
                if sessionManager.isLoading && sessionManager.sessions.isEmpty {
                    ProgressView("読み込み中...")
                } else if sessionManager.sessions.isEmpty {
                    emptyState
                } else {
                    List {
                        ForEach(sessionManager.sessions) { session in
                            SessionRow(session: session)
                                .contentShape(Rectangle())
                                .onTapGesture {
                                    selectedSession = session
                                }
                        }
                        .onDelete(perform: deleteSessions)
                    }
                    .refreshable {
                        try? await sessionManager.loadSessions()
                    }
                }
            }
            .navigationTitle("セッション")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button {
                        Task {
                            try? await sessionManager.loadSessions()
                        }
                    } label: {
                        Image(systemName: "arrow.clockwise")
                    }
                }
            }
            .sheet(item: $selectedSession) { session in
                SessionDetailView(session: session)
            }
            .onAppear {
                if sessionManager.sessions.isEmpty {
                    Task {
                        try? await sessionManager.loadSessions()
                    }
                }
            }
        }
    }

    private var emptyState: some View {
        VStack(spacing: 16) {
            Image(systemName: "waveform")
                .font(.system(size: 60))
                .foregroundStyle(.secondary)

            Text("録音がありません")
                .font(.headline)

            Text("「録音」タブで録音を開始してください")
                .foregroundStyle(.secondary)

            NavigationLink {
                RecordingView()
            } label: {
                Text("録音を開始")
                    .buttonStyle(.borderedProminent)
            }
        }
    }

    private func deleteSessions(at offsets: IndexSet) {
        Task {
            for index in offsets {
                try? await sessionManager.deleteSession(sessionManager.sessions[index])
            }
        }
    }
}

struct SessionRow: View {
    let session: Session

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(session.date, format: .dateTime.year().month().day())
                    .font(.headline)
                Spacer()
                StatusBadge(status: session.status)
            }

            Text(session.date, format: .dateTime.hour().minute())
                .foregroundStyle(.secondary)
                .font(.caption)
        }
        .padding(.vertical, 4)
    }
}

struct StatusBadge: View {
    let status: Session.SessionStatus

    var body: some View {
        Text(status.displayString)
            .font(.caption)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(statusColor.opacity(0.2))
            .foregroundStyle(statusColor)
            .clipShape(Capsule())
    }

    var statusColor: Color {
        switch status {
        case .complete:
            return .green
        case .failed, .transcriptionFailed, .generationFailed:
            return .red
        case .uploading, .transcribing, .generating:
            return .blue
        default:
            return .gray
        }
    }
}
