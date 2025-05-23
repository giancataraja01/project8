import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import firebase_admin
from firebase_admin import credentials, storage
import time

# Configuration
DURATION = 5  # seconds
FS = 96000    # Sampling rate (high enough for ultrasonic >20kHz)
FILENAME = "ultrasonic_recording.wav"

# Initialize Firebase Admin
cred = credentials.Certificate('path/to/serviceAccountKey.json')  # <-- Update path here
firebase_admin.initialize_app(cred, {
    'storageBucket': '<your-project-id>.appspot.com'  # <-- Update bucket name here
})

def record_audio(filename, duration, fs):
    print(f"Recording {duration} seconds at {fs} Hz...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wavfile.write(filename, fs, recording)
    print(f"Saved recording to {filename}")

def upload_to_firebase(filename):
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    print(f"Uploaded {filename} to Firebase Storage")

if __name__ == "__main__":
    record_audio(FILENAME, DURATION, FS)
    upload_to_firebase(FILENAME)
