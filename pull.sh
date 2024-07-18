#!/bin/bash

# Navigate to the project directory
cd /home/orangepi/Projects/PyBot

# Pull the latest changes from the repository
git pull origin main

# Restart service
echo "Service has been restarted"
sudo systemctl restart telegram.service
