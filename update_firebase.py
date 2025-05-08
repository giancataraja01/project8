import firebase_admin
from firebase_admin import credentials, db

# Path to your Firebase Admin SDK service account key file
SERVICE_ACCOUNT_PATH = 'project8-b295f-19709ee58270.json'

# Your Firebase Realtime Database URL
DATABASE_URL = 'https://project8-b295f-default-rtdb.asia-southeast1.firebasedatabase.app'

# Initialize Firebase app (only once)
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': DATABASE_URL
        })
except Exception as e:
    print(f"Error initializing Firebase app: {e}")
    exit(1)

# Reference to the field you want to update
ref = db.reference('detectstat')

# Set the boolean value
new_value = True  # Set to False if needed
try:
    ref.set(new_value)
    print(f"'detectstat' updated to: {new_value}")
except Exception as e:
    print(f"Error updating database: {e}")
