#!/bin/bash
# Generate cryptographically secure secret keys for Kenkoumon

set -e

echo "Kenkoumon Secret Key Generator"
echo "=============================="
echo ""

# Function to generate secret
generate_secret() {
    local length=${1:-32}
    openssl rand -hex "$length"
}

# Generate JWT secret
echo "JWT Secret Key (SECRET_KEY):"
jwt_secret=$(generate_secret 32)
echo "$jwt_secret"
echo ""

# Generate encryption key (for future use)
echo "Encryption Key (ENCRYPTION_KEY):"
encryption_key=$(generate_secret 32)
echo "$encryption_key"
echo ""

# Generate API key salt (for key derivation)
echo "API Key Salt (API_KEY_SALT):"
api_salt=$(generate_secret 16)
echo "$api_salt"
echo ""

# Save to file (DO NOT COMMIT THIS)
echo "Saving to secrets.env..."
cat > secrets.env << EOF
# Kenkoumon Secrets - DO NOT COMMIT
# Generated: $(date)

# JWT Secret (required)
SECRET_KEY=$jwt_secret

# Encryption Key (for future AES-256 encryption)
ENCRYPTION_KEY=$encryption_key

# API Key Salt (for key derivation)
API_KEY_SALT=$api_salt

# Add your API keys below:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
EOF

chmod 600 secrets.env
echo "✓ Secrets saved to: $(pwd)/secrets.env"
echo ""
echo "⚠️  IMPORTANT:"
echo "   1. Add your API keys to secrets.env"
echo "   2. Source this file: source secrets.env"
echo "   3. DO NOT commit secrets.env to git"
echo ""
echo "To load secrets in your shell:"
echo "  source secrets.env"
