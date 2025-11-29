#!/bin/bash
set -e

echo "⚡ Bot ishga tushmoqda (auto-reload)..."

watchfiles "python bot/main.py"
