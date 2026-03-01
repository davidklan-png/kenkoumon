//
//  AuthView.swift
//  Kenkoumon
//
//  Authentication view for login and registration.
//

import SwiftUI

struct AuthView: View {
    @EnvironmentObject var authManager: AuthManager
    @State private var isLoginMode = true
    @State private var email = ""
    @State private var password = ""
    @State private var fullName = ""
    @State private var showingError = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                // Logo
                Image("Mascot")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 120, height: 120)

                Text("Kenkoumon")
                    .font(.largeTitle)
                    .fontWeight(.bold)

                Text("健康モニター")
                    .foregroundStyle(.secondary)

                Divider()

                // Form
                VStack(spacing: 16) {
                    if !isLoginMode {
                        TextField("お名前 (任意)", text: $fullName)
                            .textFieldStyle(.roundedBorder)
                            .textInputAutocapitalization(.words)
                    }

                    TextField("メールアドレス", text: $email)
                        .textFieldStyle(.roundedBorder)
                        .textInputAutocapitalization(.never)
                        .keyboardType(.emailAddress)

                    SecureField("パスワード", text: $password)
                        .textFieldStyle(.roundedBorder)
                }

                // Action Button
                Button {
                    Task {
                        await authenticate()
                    }
                } label: {
                    if authManager.isLoading {
                        ProgressView()
                            .progressViewStyle(.circular)
                    } else {
                        Text(isLoginMode ? "ログイン" : "新規登録")
                            .frame(maxWidth: .infinity)
                    }
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)
                .disabled(email.isEmpty || password.isEmpty || authManager.isLoading)

                // Toggle Mode
                Button {
                    withAnimation {
                        isLoginMode.toggle()
                    }
                } label: {
                    Text(isLoginMode ? "アカウントをお持ちでない方" : "すでにアカウントをお持ちの方")
                }

                Spacer()

                // Disclaimer
                Text("Kenkoumonはウェルネスツールです。医療的アドバイスを提供するものではありません。")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
                    .padding()
            }
            .padding()
            .alert("エラー", isPresented: $showingError) {
                Button("OK") { }
            } message: {
                if let error = authManager.errorMessage {
                    Text(error)
                }
            }
        }
    }

    private func authenticate() async {
        do {
            if isLoginMode {
                try await authManager.login(email: email, password: password)
            } else {
                try await authManager.register(email: email, password: password, fullName: fullName.isEmpty ? nil : fullName)
            }
        } catch {
            authManager.errorMessage = error.localizedDescription
            showingError = true
        }
    }
}
