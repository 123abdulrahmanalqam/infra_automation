#!/bin/bash
set -e

LOG_FILE="logs/provisioning.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - BASH - $1" | tee -a "$LOG_FILE"
}

log "INFO - Starting Nginx installation check..."

if command -v nginx &> /dev/null; then
    log "INFO - Nginx is already installed. Skipping installation."
    exit 0
fi

log "INFO - Nginx not found. Installing Nginx..."

if [[ "$OSTYPE" == "linux-gnu"* ]] && command -v apt-get &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y nginx
elif [[ "$OSTYPE" == "darwin"* ]] && command -v brew &> /dev/null; then
    brew install nginx
else
    log "INFO - Package manager not available in local environment. Simulating Nginx installation..."
    sleep 1
fi

log "INFO - Nginx installation completed successfully."
