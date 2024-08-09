 #    Copyright [2024] [Issei-177013]

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0
#!/bin/bash

# Ask user for service names
read -p "Enter the name for the auto clicker service to uninstall: " AUTO_CLICKER_SERVICE_NAME
read -p "Enter the name for the auto buy service to uninstall: " AUTO_BUY_SERVICE_NAME

AUTO_CLICKER_SERVICE_FILE="/etc/systemd/system/${AUTO_CLICKER_SERVICE_NAME}_hamster_auto_clicker.service"
AUTO_BUY_SERVICE_FILE="/etc/systemd/system/${AUTO_BUY_SERVICE_NAME}_hamster_auto_buy.service"

# Stop and disable services
echo "Stopping and disabling services..."
sudo systemctl stop ${AUTO_CLICKER_SERVICE_NAME}_hamster_auto_clicker
sudo systemctl disable ${AUTO_CLICKER_SERVICE_NAME}_hamster_auto_clicker

sudo systemctl stop ${AUTO_BUY_SERVICE_NAME}_hamster_auto_buy
sudo systemctl disable ${AUTO_BUY_SERVICE_NAME}_hamster_auto_buy

# Remove service files
echo "Removing service files..."
sudo rm $AUTO_CLICKER_SERVICE_FILE
sudo rm $AUTO_BUY_SERVICE_FILE

# Reload systemd to apply changes
sudo systemctl daemon-reload

echo "Services uninstalled."
