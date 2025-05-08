import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
def initialize_firebase():
    # Path to your service account key JSON file
    service_account_path = "serviceAccountKey.json"
    try:
        # Load the service account credentials
        cred = credentials.Certificate(service_account_path)
        
        # Initialize the Firebase app
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://project8-b295f.firebaseio.com/'  # Replace <YOUR_PROJECT_ID> with your Firebase project ID
        })
        print("Firebase initialized successfully!")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

# Read the detection status value from the file
def read_detection_status(file_path):
    try:
        with open(file_path, 'r') as file:
            value = file.read().strip()  # Read and strip whitespace
            # Convert string to boolean
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            else:
                raise ValueError("Invalid value in detection_logs.txt. Must be 'True' or 'False'.")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        raise
    except Exception as e:
        print(f"Error reading detection status: {e}")
        raise

# Update the "detectstat" field in the Realtime Database
def update_detectstat(detectstat_value: bool):
    try:
        ref = db.reference('detectstat')  # Reference to the "detectstat" field
        ref.set(detectstat_value)        # Set the value of "detectstat"
        print(f"'detectstat' field updated to: {detectstat_value}")
    except Exception as e:
        print(f"Error updating 'detectstat': {e}")

if __name__ == "__main__":
    # Initialize Firebase
    initialize_firebase()
    
    # Path to the file containing the detection value
    log_file_path = "detection_logs.txt"
    
    try:
        # Read the value from the log file
        detectstat_value = read_detection_status(log_file_path)
        
        # Update the value in the Firebase Realtime Database
        update_detectstat(detectstat_value)
    except Exception as e:
        print(f"Program encountered an error: {e}")
