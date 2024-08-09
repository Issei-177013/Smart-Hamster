 #    Copyright [2024] [Issei-177013]

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0
#!/bin/bash

CONFIG_FILE="config.json"
CLICKER_SERVICE="hamster_auto_clicker"
BUY_SERVICE="hamster_auto_buy"

# Function to display menu
display_menu() {
    echo "==================================="
    echo "        Hamster Combat Menu        "
    echo "==================================="
    echo "1. Install services"
    echo "2. Uninstall services"
    echo "3. Check service status"
    echo "4. Change config variables"
    echo "5. Restart services"
    echo "6. Exit"
    echo "-----------------------------------"
}

# Function to install services
install_services() {
    echo "Installing services..."
    sudo bash install.sh
    echo "Services installed and started successfully."
}

# Function to uninstall services
uninstall_services() {
    echo "Uninstalling services..."
    sudo bash uninstall.sh
    echo "Services uninstalled."
}

# Function to check service status
check_service_status() {
    echo "Checking service status..."
    read -p "Enter the name for the auto clicker service to check: " AUTO_CLICKER_SERVICE_NAME
    read -p "Enter the name for the auto buy service to check: " AUTO_BUY_SERVICE_NAME

    sudo systemctl status ${AUTO_CLICKER_SERVICE_NAME}_hamster_auto_clicker
    sudo systemctl status ${AUTO_BUY_SERVICE_NAME}_hamster_auto_buy
}

# Function to change config variables
change_config_variables() {
    echo "Changing config variables..."
    echo "Enter new authorization (Bearer ...): "
    read authorization
    echo "Enter new min balance threshold: "
    read min_balance_threshold
    echo "Enter new capacity: "
    read capacity
    echo "Enter new threshold: "
    read threshold

    # Update config.json
    echo "{
    \"authorization\": \"$authorization\",
    \"min_balance_threshold\": $min_balance_threshold,
    \"capacity\": $capacity,
    \"threshold\": $threshold
    }" > $CONFIG_FILE

    echo "Config variables updated."
}

# Function to restart services
restart_services() {
    echo "Restarting services..."
    read -p "Enter the name for the auto clicker service to restart: " AUTO_CLICKER_SERVICE_NAME
    read -p "Enter the name for the auto buy service to restart: " AUTO_BUY_SERVICE_NAME

    sudo systemctl restart ${AUTO_CLICKER_SERVICE_NAME}_hamster_auto_clicker
    sudo systemctl restart ${AUTO_BUY_SERVICE_NAME}_hamster_auto_buy
    echo "Services restarted."
}

# Main loop
while true; do
    display_menu

    echo "Enter your choice (1-6): "
    read choice

    case $choice in
        1) install_services ;;
        2) uninstall_services ;;
        3) check_service_status ;;
        4) change_config_variables ;;
        5) restart_services ;;
        6) echo "Exiting..."; break ;;
        *) echo "Invalid choice. Please enter a number between 1 and 6." ;;
    esac

    echo "Press Enter to continue..."
    read
done
