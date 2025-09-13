#!/usr/bin/env bash
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers (Chromium)
playwright install --with-deps chromium
