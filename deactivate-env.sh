#!/bin/bash
# Neodoo18Framework Environment Deactivation Helper

if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
    echo "🐍 Neodoo18Framework environment deactivated"
else
    echo "ℹ️  No active virtual environment"
fi
