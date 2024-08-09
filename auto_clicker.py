 #    Copyright [2024] [Issei-177013]

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0
import os
import json
import time
import random
import requests
from collections import deque

CONFIG_FILE = 'config.json'

# Function to load configuration from JSON file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

# Function to save configuration to JSON file
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# Function to purchase upgrade (equivalent to Bash function)
def purchase_upgrade(upgrade_id, authorization):
    timestamp = int(time.time() * 1000)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': authorization,
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/'
    }
    payload = {
        'upgradeId': upgrade_id,
        'timestamp': timestamp
    }
    response = requests.post('https://api.hamsterkombat.io/clicker/buy-upgrade', json=payload, headers=headers)
    return response.json()

# Function to get the best upgrade item (equivalent to Bash function)
def get_best_item(authorization):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Android 12; Mobile; rv:102.0) Gecko/102.0 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://hamsterkombat.io/',
        'Authorization': authorization,
        'Origin': 'https://hamsterkombat.io',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4'
    }
    response = requests.post('https://api.hamsterkombatgame.io/clicker/upgrades-for-buy', headers=headers)
    items = response.json().get('upgradesForBuy', [])
    
    # Filter valid items
    valid_items = [item for item in items if not item.get('isExpired') and item.get('isAvailable') and item.get('profitPerHourDelta') != 0 and item.get('price') != 0]
    
    # Find best item
    sorted_upgrades = sorted(valid_items, key=lambda x: -(x['profitPerHourDelta'] / x['price']))
    return sorted_upgrades[0] if sorted_upgrades else None

def get_second_best_item(authorization):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Android 12; Mobile; rv:102.0) Gecko/102.0 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://hamsterkombat.io/',
        'Authorization': authorization,
        'Origin': 'https://hamsterkombat.io',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4'
    }
    response = requests.post('https://api.hamsterkombatgame.io/clicker/upgrades-for-buy', headers=headers)
    items = response.json().get('upgradesForBuy', [])
    
    # Filter valid items
    valid_items = [item for item in items if not item.get('isExpired') and item.get('isAvailable') and item.get('profitPerHourDelta') != 0 and item.get('price') != 0]
    
    # Find best item
    sorted_upgrades = sorted(valid_items, key=lambda x: -(x['profitPerHourDelta'] / x['price']))
    return sorted_upgrades[1] if len(sorted_upgrades) > 1 else None

# Function to wait for cooldown period (equivalent to Bash function)
def wait_for_cooldown(cooldown_seconds):
    print(f"Upgrade is on cooldown. Waiting for cooldown period of {cooldown_seconds} seconds...")
    for remaining_time in range(cooldown_seconds, 0, -1):
        print(f"{remaining_time} seconds remaining...", end='\r')
        time.sleep(1)
    print("Cooldown period is over. Resuming operations.")

def choose(best_item, second_item, threshold):
    left_side = (threshold) * (best_item['price'] / best_item['profitPerHourDelta'])
    right_side = second_item['price'] / second_item['profitPerHourDelta']

    if not best_item.get('cooldownSeconds') or best_item['cooldownSeconds'] == 0:
        return best_item
    elif second_item.get('cooldownSeconds') and second_item['cooldownSeconds'] != 0:
        return best_item
    elif left_side > right_side:
        return second_item
    else:
        return best_item

# Function to log messages to a file
def log_message(message):
    with open("hamster_auto_buy.log", "a") as log_file:
        log_file.write(message + "\n")

# Main function (equivalent to Bash main logic)
def main():
    print("\033[0;35m=======\033[0;33mHamster Combat Auto Buy best cards\033[0;35m=======")
    print()

    config = load_config()

    authorization = config.get('authorization')
    min_balance_threshold = config.get('min_balance_threshold')
    threshold = config.get('threshold', 1.0)  # Default threshold value if not present in config

    if not authorization:
        authorization = input("\033[0;32mEnter Authorization [Example: Bearer 171852....]: \033[0m")
        config['authorization'] = authorization
        save_config(config)

    print("\033[0;35m============================\033[0m")

    if not min_balance_threshold:
        min_balance_threshold = float(input("\033[0;32mEnter minimum balance threshold (the script will stop purchasing if the balance is below this amount): \033[0m"))
        config['min_balance_threshold'] = min_balance_threshold
        save_config(config)

    total_spent = 0
    total_profit = 0

    profit_spent_ratios = deque(maxlen=10)  # Maintain a deque with max length 10 to store profit/spent ratios

    while True:
        best_item = get_best_item(authorization)
        second_best_item = get_second_best_item(authorization)  # Get the second best item
        
        if not best_item:
            log_message("No valid item found to buy.")
            break
        
        chosen_item = choose(best_item, second_best_item, threshold) if second_best_item else best_item

        best_item_id = chosen_item['id']
        section = chosen_item.get('section', 'Unknown Section')
        price = chosen_item.get('price', 0)
        profit = chosen_item.get('profitPerHourDelta', 0)
        cooldown = chosen_item.get('cooldownSeconds', 0)

        log_message("============================")
        log_message(f"Best item to buy: {best_item_id} in section: {section}")
        log_message(f"Price: {price}")
        log_message(f"Profit per Hour: {profit}")
        log_message(f"Cooldown Seconds: {cooldown}")
        log_message("")

        headers = {
            'Authorization': authorization,
            'Origin': 'https://hamsterkombat.io',
            'Referer': 'https://hamsterkombat.io/'
        }
        current_balance_response = requests.post('https://api.hamsterkombat.io/clicker/sync', headers=headers)
        current_balance = current_balance_response.json()['clickerUser']['balanceCoins']

        if current_balance - price > min_balance_threshold:
            log_message(f"Attempting to purchase upgrade '{best_item_id}'...")
            log_message("")

            purchase_status = purchase_upgrade(best_item_id, authorization)

            if 'error_code' in purchase_status:
                wait_for_cooldown(cooldown)
            else:
                purchase_time = time.strftime('%Y-%m-%d %H:%M:%S')
                total_spent += price
                total_profit += profit
                current_balance -= price

                log_message(f"Upgrade '{best_item_id}' purchased successfully at {purchase_time}.")
                log_message(f"Total spent so far: {total_spent} coins.")
                log_message(f"Total profit added: {total_profit} coins per hour.")
                log_message(f"Current balance: {current_balance} coins.")
                
                # Add the current profit/spent ratio to the deque
                profit_spent_ratios.append(profit / price)
                
                # Adjust the threshold based on the average profit/spent ratio
                if profit_spent_ratios:
                    threshold = max(1.0, sum(profit_spent_ratios) / len(profit_spent_ratios))
                config['threshold'] = threshold
                save_config(config)
                
                sleep_duration = random.randint(5, 12)
                log_message(f"Waiting for {sleep_duration} seconds before next purchase...")
                time.sleep(sleep_duration)
        else:
            log_message(f"Current balance ({current_balance}) minus price of item ({price}) is below the threshold ({min_balance_threshold}). Stopping purchases.")
            break

if __name__ == "__main__":
    main()
