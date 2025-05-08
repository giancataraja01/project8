import firebase_admin
from firebase_admin import credentials, db

# Path to your Firebase Admin SDK service account key
SERVICE_ACCOUNT_PATH = 'path/to/your/serviceAccountKey.json'

# Your Firebase Realtime Database URL
DATABASE_URL = 'https://your-project-id.firebaseio.com/'

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
