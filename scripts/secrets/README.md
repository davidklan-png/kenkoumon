# Secrets Management Guide

Secure management of API keys, passwords, and sensitive configuration.

## Table of Contents

- [Overview](#overview)
- [Development](#development)
- [Production](#production)
- [CI/CD](#cicd)
- [iOS Keychain](#ios-keychain)
- [Rotation](#rotation)

---

## Overview

**Never commit secrets to git!** All sensitive data must be stored securely.

### Types of Secrets

| Secret | Example | Location |
|--------|---------|----------|
| **API Keys** | OpenAI, Anthropic | `.env.local`, GitHub Secrets |
| **Database URLs** | PostgreSQL connection | `.env.local`, GitHub Secrets |
| **JWT Secrets** | Token signing | `.env.local`, generate per env |
| **Encryption Keys** | AES-256 keys | Derived from password |
| **Ollama URLs** | User-hosted AI | `.env.local` |

---

## Development

### Local Development (`.env.local`)

Create `.env.local` (gitignored):

```bash
# Copy template
cp backend/.env.example backend/.env.local

# Edit with your values
nano backend/.env.local
```

**Example `.env.local`:**
```bash
# Generate with: openssl rand -hex 32
SECRET_KEY=a1b2c3d4e5f6...

# Your API keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=sqlite:///kenkoumon.db

# AI sources
DEFAULT_TRANSCRIPTION_SOURCE=cloud
DEFAULT_LLM_SOURCE=cloud
```

### Loading Secrets

```bash
# Backend automatically loads from .env.local
cd backend
uvicorn main:app --reload
```

---

## Production

### Option 1: Environment Variables (Recommended for small deployments)

Set environment variables directly on the server:

```bash
# systemd service file
Environment="SECRET_KEY=your-secret"
Environment="OPENAI_API_KEY=your-key"
Environment="DATABASE_URL=postgresql://..."
```

### Option 2: AWS Secrets Manager

**Store secrets:**
```bash
aws secretsmanager create-secret \
  --name kenkoumon/production \
  --secret-string '{
    "SECRET_KEY": "...",
    "OPENAI_API_KEY": "...",
    "DATABASE_URL": "..."
  }'
```

**Load in application:**
```python
import boto3
import json

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='kenkoumon/production')
secrets = json.loads(response['SecretString'])
```

### Option 3: Docker Secrets

**docker-compose.yml:**
```yaml
services:
  api:
    secrets:
      - openai_key
      - jwt_secret
    environment:
      OPENAI_API_KEY_FILE: /run/secrets/openai_key
      SECRET_KEY_FILE: /run/secrets/jwt_secret

secrets:
  openai_key:
    file: ./secrets/openai_key.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

---

## CI/CD

### GitHub Secrets

Go to: **Repository → Settings → Secrets and variables → Actions → New repository secret**

**Required secrets:**

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SECRET_KEY` | JWT signing key | Generate with `openssl rand -hex 32` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-...` |
| `DATABASE_URL` | Production database | `postgresql://...` |

### Using Secrets in Workflows

```yaml
# .github/workflows/backend-ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests with secrets
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
        run: |
          echo "$OPENAI_API_KEY" > .env
          pytest
```

---

## iOS Keychain

### Storing API Keys in Keychain

**KeychainService.swift:**
```swift
import Security

class KeychainService {
    static let shared = KeychainService()

    private let service = "com.kenkoumon.keys"

    func save(key: String, value: String) -> Bool {
        let data = value.data(using: .utf8)!
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]
        SecItemDelete(query as CFDictionary) // Delete existing
        return SecItemAdd(query as CFDictionary, nil) == errSecSuccess
    }

    func get(key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        if status == errSecSuccess,
           let data = result as? Data {
            return String(data: data, encoding: .utf8)
        }
        return nil
    }

    func delete(key: String) -> Bool {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key
        ]
        return SecItemDelete(query as CFDictionary) == errSecSuccess
    }
}
```

**Usage:**
```swift
// Save API key
KeychainService.shared.save(key: "openai_key", value: "sk-...")

// Retrieve API key
let apiKey = KeychainService.shared.get(key: "openai_key")
```

### Entitlements

**ios/Kenkoumon/Kenkoumon.entitlements:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>keychain-access-groups</key>
    <array>
        <string>$(AppIdentifierPrefix)com.kenkoumon</string>
    </array>
</dict>
</plist>
```

---

## Rotation

### Regular Rotation Schedule

| Secret | Rotation Frequency | Method |
|--------|-------------------|--------|
| JWT Secret Key | Quarterly | Generate new, redeploy |
| API Keys | Annually | Regenerate in provider console |
| Database Password | Quarterly | Update database, update secrets |

### Rotating JWT Secret

```bash
# Generate new key
NEW_KEY=$(openssl rand -hex 32)

# Update AWS Secrets Manager
aws secretsmanager update-secret \
  --secret-id kenkoumon/production \
  --secret-string "{\"SECRET_KEY\":\"$NEW_KEY\"}"

# Redeploy application
kubectl rollout restart deployment/kenkoumon-api
```

---

## Best Practices

### DO ✅

- ✅ Use `.env.example` as template (commit this)
- ✅ Never commit `.env.local` or real secrets
- ✅ Use different secrets per environment
- ✅ Rotate secrets regularly
- ✅ Use Keychain on iOS
- ✅ Use GitHub Secrets for CI/CD
- ✅ Limit secret access to minimum necessary

### DON'T ❌

- ❌ Commit secrets to git
- ❌ Share secrets via email/chat
- ❌ Use same secret across environments
- ❌ Hardcode secrets in code
- ❌ Log secrets in error messages
- ❌ Store secrets in plain config files

---

## Verification

### Check for Committed Secrets

```bash
# Search for potential secrets in git history
git log --all --full-history --source -- "*key*" "*secret*" "*password*"

# Scan current files
grep -r "sk-" . --exclude-dir=.git
grep -r "sk-ant-" . --exclude-dir=.git
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Prevent committing secrets

if git diff --cached --name-only | grep -E "\.env$|\.key$|secrets\.yaml"; then
    echo "ERROR: Attempting to commit secrets file!"
    exit 1
fi

# Check for potential secrets in staged files
if git diff --cached | grep -E "sk-[a-zA-Z0-9]{20,}"; then
    echo "ERROR: Potential API key in staged changes!"
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Emergency: Exposed Secret

If a secret is accidentally committed:

1. **Rotate immediately** - Generate new secret
2. **Remove from git** - Use BFG Repo-Cleaner or git filter-repo
3. **Force push** - Overwrite git history
4. **Invalidate old** - Revoke old API key
5. **Audit** - Check for unauthorized access

```bash
# Remove file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```
