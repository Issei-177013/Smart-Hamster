#!/bin/bash

# Install jq (if not already installed)
if ! command -v jq &> /dev/null; then
    echo "Installing jq..."
    sudo apt update
    sudo apt install -y jq
fi

# Define the path to config.json
CONFIG_FILE="config.json"

# Check if config.json exists and is not empty
if [[ -s $CONFIG_FILE ]]; then
    echo "Config file $CONFIG_FILE found."
    # Read values from config.json using jq
    AUTHORIZATION=$(jq -r '.authorization' $CONFIG_FILE)
    MIN_BALANCE_THRESHOLD=$(jq -r '.min_balance_threshold' $CONFIG_FILE)
    CAPACITY=$(jq -r '.capacity' $CONFIG_FILE)
    THRESHOLD=$(jq -r '.threshold' $CONFIG_FILE)
else
    echo "Config file $CONFIG_FILE not found or empty. Creating new config..."
    # Ask user for input if config.json does not exist
    read -p "Enter Authorization [Example: Bearer 17194877Oo2Gp...]: " AUTHORIZATION
    read -p "Enter Minimum Balance Threshold [Example: 10000000.0]: " MIN_BALANCE_THRESHOLD
    read -p "Enter Capacity [Example: 10000]: " CAPACITY
    read -p "Enter Threshold [Example: 1.0]: " THRESHOLD
    
    # Create config.json with input values
    cat << EOF > $CONFIG_FILE
{
  "authorization": "$AUTHORIZATION",
  "min_balance_threshold": $MIN_BALANCE_THRESHOLD,
  "capacity": $CAPACITY,
  "threshold": $THRESHOLD
}
EOF
fi

# Ask user for service names
read -p "Enter the name for the auto clicker service: " AUTO_CLICKER_SERVICE_NAME
read -p "Enter the name for the auto buy service: " AUTO_BUY_SERVICE_NAME

AUTO_CLICKER_SERVICE_FILE="/etc/systemd/system/${AUTO_CLICKER_SERVICE_NAME}_hamster_auto_clicker.service"
AUTO_BUY_SERVICE_FILE="/etc/systemd/system/${AUTO_BUY_SERVICE_NAME}_hamster_auto_buy.service"

# Export variables for Python scripts to use
export AUTHORIZATION
export MIN_BALANCE_THRESHOLD
export CAPACITY
export THRESHOLD

# Get absolute path of this script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Create service files for both Python scripts
echo "Creating systemd services..."

# Service file for the first Python script (auto_clicker.py)
cat << EOF | sudo tee $AUTO_CLICKER_SERVICE_FILE > /dev/null
[Unit]
Description=Hamster Combat Auto Clicker Service
After=network.target

[Service]
User=$USER
Environment="AUTHORIZATION=$AUTHORIZATION"
Environment="CAPACITY=$CAPACITY"
Environment="THRESHOLD=$THRESHOLD"
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_DIR/auto_clicker.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Service file for the second Python script (auto_buy_best_cards.py)
cat << EOF | sudo tee $AUTO_BUY_SERVICE_FILE > /dev/null
[Unit]
Description=Hamster Combat Auto Buy Best Cards Service
After=network.target

[Service]
User=$USER
Environment="AUTHORIZATION=$AUTHORIZATION"
Environment="MIN_BALANCE_THRESHOLD=$MIN_BALANCE_THRESHOLD"
Environment="THRESHOLD=$THRESHOLD"
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_DIR/auto_buy_best_cards.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to load new service files
sudo systemctl daemon-reload

# Start and enable services
echo "Starting and enabling services..."
sudo systemctl start ${AUTO_CLICKER_SERVICE_NAME}_hamster_auto_clicker
sudo systemctl enable ${AUTO_CLICKER_SERVICE_NAME}_hamster_auto_clicker

sudo systemctl start ${AUTO_BUY_SERVICE_NAME}_hamster_auto_buy
sudo systemctl enable ${AUTO_BUY_SERVICE_NAME}_hamster_auto_buy

echo "Services started successfully."

# End of bash script
