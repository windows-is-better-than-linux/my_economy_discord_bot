import json
import os
import random
import datetime

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If file is empty or malformed, return an empty dictionary
                return {}
    else:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved: {data}")

def add_person(user_id):
    data = load_data()
    print(f"Current data: {data}")

    if str(user_id) not in data:
        data[str(user_id)] = {"gems": 0, "begs_today": 0, "last_claim": ""}
        print(f"Adding user {user_id} with initial gems: 0")
        save_data(data)
    else:
        print(f"User {user_id} already exists in the system.")

def beg(user_id):
    data = load_data()

    if str(user_id) not in data:
        return "You are not registered in the economy system. Use `!add_me` to register."

    user_data = data[str(user_id)]
    if user_data["begs_today"] >= 5:
        return "You have already begged 5 times today. Try again tomorrow."

    chance = random.randint(1, 5)
    if chance == 5:
        amount = 50
    elif chance == 4:
        amount = 25
    else:
        amount = 0

    if amount > 0:
        user_data["gems"] += amount
        user_data["begs_today"] += 1
        save_data(data)
        return f"You received {amount} gems! You now have {user_data['gems']} gems."
    else:
        user_data["begs_today"] += 1
        save_data(data)
        return "You begged but received nothing. Better luck next time!"

def claim_daily_reward(user_id):
    data = load_data()
    if str(user_id) not in data:
        return "You are not registered in the economy system. Use `!add_me` to register."

    user_data = data[str(user_id)]
    today = str(datetime.date.today())

    if user_data["last_claim"] == today:
        return "You have already claimed your daily reward today. Try again tomorrow."

    # Reward the user and update last claim date
    reward_amount = 10  # Set your reward amount
    user_data["gems"] += reward_amount
    user_data["last_claim"] = today
    save_data(data)

    return f"You received {reward_amount} gems! You now have {user_data['gems']} gems."

