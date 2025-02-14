import requests
import time
from rpi_lcd import LCD

import config

#LCD config
lcd = LCD()

# GroupMe API Details
ACCESS_TOKEN = config.access_token
GROUP_ID = config.group_id
GROUP_URL = f"https://api.groupme.com/v3/groups/{GROUP_ID}"
MESSAGE_URL = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
HEADERS = {"X-Access-Token": ACCESS_TOKEN}

# Track the latest message ID and member count
last_message_id = None
current_member_count = 0

# Get member count
def get_mem_count():
    global current_member_count
    response = requests.get(GROUP_URL, headers=HEADERS)
    
    if response.status_code == 200:
        member_count = response.json().get("response", {}).get("members_count")

        return member_count
    else:
        print(f"Failed to fetch member count: {response.status_code}")
    return current_member_count

# Get message
def get_messages():
    global last_message_id
    params = {"limit": 1}  # Get the latest message
    response = requests.get(MESSAGE_URL, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        messages = response.json().get("response", {}).get("messages", [])
        
        if messages:
            message = messages[0]
            
            if message["id"] != last_message_id:
                last_message_id = message["id"]
                return message
    else:
        print(f"Failed to fetch message: {response.status_code}")
    return None

# Display to LCD
def display(line1, line2 = ""):
    try:
        lcd.clear()
        lcd.text(f"{line1}", 1)
        if line2:
            lcd.text(f"{line2}", 2)
    except Exception as e:
        print(f"Error displaying text on LCD: {e}")

def main():
    global current_member_count
    
    current_member_count = get_mem_count()
    display(f"BTA Members:", current_member_count)
    
    while True:
        message = get_messages()
        
        if message:
            text = message.get("text", "")
            user = message.get("name", "")
           
            if "added" in text:
                text = text.split(" added ")[1]
                added_user = text.split(" to the group.")[0]
                
                current_member_count = get_mem_count()

                print(f"Welcome, {added_user}")
                display(f"Welcome,", added_user)
                
                time.sleep(5)  
            elif "joined" in text:
                joined_user = text.split(" has joined the group")[0]

                current_member_count = get_mem_count()
                
                print(f"Welcome, {joined_user}")
                display(f"Welcome,", joined_user) 
                
                time.sleep(5)
        
        display(f"BTA Members:", current_member_count)
        time.sleep(2)  # Avoid spamming the API

if __name__ == "__main__":
    try:
        lcd.clear()
        main()
    except KeyboardInterrupt:
        time.sleep(0.5)
        lcd.clear()
        print("Program stopped")
