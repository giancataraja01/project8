import firebase_admin
from firebase_admin import credentials, db

SERVICE_ACCOUNT_PATH = 'replace_this.json'
DATABASE_URL = 'https://project8-b295f-default-rtdb.asia-southeast1.firebasedatabase.app'
LOG_FILE_PATH = 'detection_logs.txt'

# Initialize Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': DATABASE_URL
        })
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    exit(1)

# Determine detectstat from log file
try:
    with open(LOG_FILE_PATH, 'r') as f:
        log_content = f.read()
    new_value = "DETECTED" in log_content.upper()
except Exception as e:
    print(f"Error reading log file: {e}")
    new_value = False  # Default to False on error

# Update Firebase with detectstat
try:
    ref = db.reference('detectstat')
    ref.set(new_value)
    print(f"'detectstat' updated to: {new_value}")
except Exception as e:
    print(f"Database update error: {e}")
