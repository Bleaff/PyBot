#!/bin/bash

# Install Telegram Bot Service Script

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

# Define the service file path
SERVICE_FILE_PATH="/etc/systemd/system/telegram.service"

# Copy the telegram.service file to the systemd directory
echo "Copying telegram.service to $SERVICE_FILE_PATH"
cp telegram.service $SERVICE_FILE_PATH

# Set proper permissions for the service file
echo "Setting permissions for $SERVICE_FILE_PATH"
chmod 644 $SERVICE_FILE_PATH

# Reload systemd manager configuration
echo "Reloading systemd manager configuration"
systemctl daemon-reload

# Enable the telegram service
echo "Enabling telegram service"
systemctl enable telegram.service

# Start the telegram service
echo "Starting telegram service"
systemctl start telegram.service

# Check the status of the telegram service
echo "Checking status of telegram service"
systemctl status telegram.service

echo "Telegram Bot Service installation completed."

