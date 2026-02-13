#!/bin/bash
# Quick Start Script pou Senjivis Komès 2026

echo "🚀 Senjivis Komès 2026 - Dashboard Setup"
echo "==========================================="
echo ""

# Check Python version
echo "✓ Verifye Python version..."
python3 --version

# Create virtual environment
echo ""
echo "✓ Kreye virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "✓ Aktive virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "✓ Enstale dependans..."
pip install -r requirements.txt

# Display next steps
echo ""
echo "================================================"
echo "✅ Setup Konplè!"
echo "================================================"
echo ""
echo "📊 Pou demaré dashboard la, jis kouri:"
echo "   python app.py"
echo ""
echo "🌐 Apre sa, vizite sa URL nan browser:"
echo "   http://localhost:8050"
echo ""
echo "📁 Pwojè lokalize nan:"
echo "   ~/ecommerce-dashboard"
echo ""
echo "================================================"
