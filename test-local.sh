#!/bin/bash

# Local Testing Script for Morning Intelligence Brief
# Make sure you have .env file with your credentials

echo "================================"
echo "Morning Intelligence Brief - Local Test"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Create .env file first:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your credentials"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check required variables
if [ -z "$RECIPIENT_EMAIL" ] || [ -z "$SMTP_EMAIL" ] || [ -z "$SMTP_PASSWORD" ]; then
    echo "❌ Error: Missing required environment variables!"
    echo ""
    echo "Make sure .env contains:"
    echo "  RECIPIENT_EMAIL=..."
    echo "  SMTP_EMAIL=..."
    echo "  SMTP_PASSWORD=..."
    exit 1
fi

echo "✅ Environment variables loaded"
echo "   Recipient: $RECIPIENT_EMAIL"
echo "   Sender: $SMTP_EMAIL"
echo ""

# Install dependencies if needed
if ! python3 -c "import requests" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Run the script
echo "🚀 Running Morning Intelligence Brief..."
echo ""
python3 main.py

echo ""
echo "================================"
echo "Done! Check your email inbox 📧"
echo "================================"
