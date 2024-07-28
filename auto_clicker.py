import os
import sys
import time
import random
import requests
from datetime import datetime
import json

# Colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
PURPLE = '\033[0;35m'
CYAN = '\033[0;36m'
BLUE = '\033[0;34m'
RESET = '\033[0m'

# Function to check for necessary packages and install them
def install_packages():
    try:
        import requests
    except ImportError:
        os.system('pip install requests')

# Function to read configuration from config.json
def read_config():
    config_file = 'config.json'
    default_config = {
        "authorization": None,
        "capacity": None
    }
    
    # Check if config file exists and is not empty
    if os.path.exists(config_file) and os.path.getsize(config_file) > 0:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            # Handle case where config file is empty or invalid JSON
            print(f"{RED}Error: Config file '{config_file}' is empty or invalid JSON.{RESET}")
            sys.exit(1)
        
        # Check and update missing fields with defaults
        for key, value in default_config.items():
            if key not in config or config[key] is None:
                if key == 'authorization':
                    authorization = input(f"{GREEN}Enter Authorization [{CYAN}Example: {YELLOW}Bearer 171852....{GREEN}]: {RESET}")
                    config['authorization'] = authorization
                elif key == 'capacity':
                    capacity = input(f"{GREEN}Enter Coin Capacity [{YELLOW}default:5000{GREEN}]: {RESET}")
                    capacity = int(capacity) if capacity else 5000
                    config['capacity'] = capacity
                
                # Save updated config to file
                with open(config_file, 'w') as f:
                    json.dump(config, f)
        
        authorization = config['authorization']
        capacity = config['capacity']
        
    else:
        authorization = input(f"{GREEN}Enter Authorization [{CYAN}Example: {YELLOW}Bearer 171852....{GREEN}]: {RESET}")
        capacity = input(f"{GREEN}Enter Coin Capacity [{YELLOW}default:5000{GREEN}]: {RESET}")
        capacity = int(capacity) if capacity else 5000
        
        # Save inputs to config.json for future runs
        with open(config_file, 'w') as f:
            json.dump({'authorization': authorization, 'capacity': capacity}, f)
    
    return authorization, capacity

# Function to get taps count
def get_taps(auth_token, server_url):
    response = requests.post(
        f'{server_url}/clicker/sync',
        headers={
            'Content-Type': 'application/json',
            'Authorization': auth_token
        },
        json={}
    )
    return response.json().get('clickerUser', {}).get('availableTaps', 0)

# Main function for auto clicker and auto purchase
def run_hamster_service(authorization, capacity=5000, server_url="https://api.hamsterkombat.io"):
    while True:
        taps = get_taps(authorization, server_url)
        
        if taps < 30:
            print("Taps are less than 30. Waiting to reach", capacity, "again...")
            while taps < capacity:
                taps = get_taps(authorization, server_url)
                time.sleep(5)
            continue

        random_sleep = random.uniform(0.02, 0.06)
        time.sleep(random_sleep)

        response = requests.post(
            f'{server_url}/clicker/tap',
            headers={
                'Content-Type': 'application/json',
                'Authorization': authorization
            },
            json={
                'availableTaps': taps,
                'count': 3,
                'timestamp': int(datetime.now().timestamp())
            }
        )
        if response.status_code == 200:
            print(f"Taps left: {taps}")
        else:
            print(f"Failed to perform tap action: {response.status_code} - {response.text}")

# Run the service
if __name__ == "__main__":
    # Clear the screen
    os.system('clear')
    print(f"{PURPLE}======={YELLOW} Hamster Combat Auto Clicker{PURPLE}======={RESET}")
    
    # Read configuration from config.json or ask user for inputs
    authorization, capacity = read_config()
    
    # Start the main service function
    run_hamster_service(authorization, capacity)
