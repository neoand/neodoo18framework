#!/bin/bash
# Neodoo18Framework Environment Activation Helper

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "🐍 Neodoo18Framework Python environment activated!"
    echo "📦 Framework location: $(pwd)"
    echo "🔧 Python version: $(python --version)"
    echo "📚 To create project: ./quick-start.sh my_project"
    echo "✅ To validate: python3 framework/validator.py my_project/"
else
    echo "❌ Virtual environment not found!"
    echo "Run: ./setup-env.sh to create it"
fi
