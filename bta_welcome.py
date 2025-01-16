import requests
import time
import config

# GroupMe API Details
ACCESS_TOKEN = config.access_token
GROUP_ID = config.group_id
API_URL = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
HEADERS = {"X-Access-Token": ACCESS_TOKEN}

# Track the latest message ID
last_message_id = None

def get_messages():
    global last_message_id
    params = {"limit": 1}  # Get the latest message
    response = requests.get(API_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        messages = response.json().get("response", {}).get("messages", [])
        if messages:
            message = messages[0]
            if message["id"] != last_message_id:
                last_message_id = message["id"]
                return message
    return None

def main():
    while True:
        message = get_messages()
        if message:
            text = message.get("text", "")
            user = message.get("name", "")
            if "added" in text:  # Look for "added" in message text
                text = text.split(" added ")[1]
                added_user = text.split(" to the group.")[0]
                print(f"Welcome, {added_user}")
                # Display the name on a connected display here
            elif "joined" in text:
                joined_user = text.split(" has joined the group")[0]
                print(f"Welcome, {joined_user}")
        time.sleep(2)  # Avoid spamming the API

if __name__ == "__main__":
    main()
