# Imports
import json
import os
import re
import bcrypt

USERS_FILE = "users.json"

# Hash password using bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Check if provided password matches hashed password
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Load users from JSON file
def load_users():
    if not os.path.exists(USERS_FILE): # If users file doesn't exist, return empty dictionary
        return {}
    try:
        with open(USERS_FILE, 'r') as f: # Open existing users file
            return json.load(f)
    except json.JSONDecodeError:
        return {}

# Save users to JSON file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# Register a new user
def register_user(username, password):
    users = load_users()
    if username in users: # Check if username already exists
        return False, "Username already exists."
    users[username] = hash_password(password)
    save_users(users)
    return True, "User registered successfully."

# Authenticate user with username and password
def authenticate_user(username, password):
    users = load_users()
    if username in users and check_password(password, users[username]): # Check if username exists and password matches
        return True
    return False

# Validate username and password according to specified rules
def validate_credentials(username, password):
    if not username or not password: # Check if username or password is empty
        return False, "Username and password cannot be empty."

    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username): # Check if username matches pattern (3–20 characters, letters, numbers and underscores only)
        return False, "Username must be 3–20 characters, (letters, numbers & underscores only)."

    if len(password) < 8: # Check if password is at least 8 characters long
        return False, "Password must be at least 8 characters long."

    if not re.search(r"\d", password): # Check if password contains at least one digit
        return False, "Password must include at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): # Check if password contains at least one special character
        return False, "Password must include at least one special character."

    return True, ""