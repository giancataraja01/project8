import firebase_admin
from firebase_admin import credentials, db

# Path to your Firebase Admin SDK service account key
SERVICE_ACCOUNT_PATH = 'project8-b295f-19709ee58270.json'

# Your Firebase Realtime Database URL
DATABASE_URL = 'https://project8-b295f-default-rtdb.asia-southeast1.firebasedatabase.app'

# Initialize Firebase app
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL
})

# Reference to the field you want to update
ref = db.reference('detectstat')  # Adjust if detectstat is nested

# Set the boolean value (True or False)
new_value = True  # or False, depending on your update
ref.set(new_value)

print(f"'detectstat' updated to: {new_value}")
