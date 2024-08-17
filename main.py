import face_recognition
import cv2
import datetime
import sqlite3
import numpy as np
from PIL import Image
import imagehash
import time
import yaml
import hashlib
import tensorflow as tf

# Import necessary libraries for feature extraction
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize


# Load the pre-trained MobileNetV2 model for feature extraction
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
feature_extractor = Model(inputs=base_model.input, outputs=layers.GlobalAveragePooling2D()(base_model.output))
base_model.trainable = False


def extract_clothing_features(image):
    # Resize the image to 128x128
    img = cv2.resize(image, (128, 128))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    features = feature_extractor.predict(img)
    return features

def compare_clothing_features(features1, features2, threshold=0.8):
    features1 = features1.reshape(1, -1)  # Reshape to 2D array
    features2 = features2.reshape(1, -1)  # Reshape to 2D array
    
    features1 = normalize(features1)
    features2 = normalize(features2)
    
    similarity = cosine_similarity(features1, features2)
    return similarity[0][0] > threshold


# Load configuration from a file
def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def create_connection(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS occupancy (
        id INTEGER PRIMARY KEY,
        signature TEXT,
        entry_time TEXT,
        exit_time TEXT
    )
    ''')
    conn.commit()
    return conn, cursor

def reset_occupancy(cursor, conn):
    cursor.execute('DELETE FROM occupancy')
    conn.commit()
    print("Occupancy reset to 0.")

def log_entry(cursor, conn, signature):
    entry_time = datetime.datetime.now().isoformat()
    cursor.execute('INSERT INTO occupancy (signature, entry_time) VALUES (?, ?)', (signature, entry_time))
    conn.commit()
    print(f"Entry logged at {entry_time} with signature {signature}")

def log_exit(cursor, conn, signature):
    exit_time = datetime.datetime.now().isoformat()
    cursor.execute('''
    UPDATE occupancy
    SET exit_time = ?
    WHERE signature = ? AND exit_time IS NULL
    ''', (exit_time, signature))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"Exit logged at {exit_time} with signature {signature}")
    else:
        print(f"No entry found for signature {signature} to log exit.")

def get_current_occupancy(cursor):
    cursor.execute('SELECT COUNT(*) FROM occupancy WHERE exit_time IS NULL')
    occupancy = cursor.fetchone()[0]
    print(f"Current Occupancy: {occupancy}")
    return occupancy

def is_similar_hash(hash1, hash2, max_diff=10):
    return abs(hash1 - hash2) <= max_diff


def is_close_position(pos1, pos2, max_distance=40):
    return np.linalg.norm(np.array(pos1) - np.array(pos2)) <= max_distance

def detect_people(frame, person_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return person_cascade.detectMultiScale(gray, 1.1, 4)


import hashlib
def process_person(person_center, frame_center, person_roi, known_signatures, current_time, config, cursor, conn):
    face_locations = face_recognition.face_locations(person_roi)
    face_encodings = face_recognition.face_encodings(person_roi, face_locations)

    if len(face_encodings) > 0:
        signature = tuple(face_encodings[0])  # Directly use the face encoding as the signature
        mode = "face"
    else:
        # Extract features from clothing
        clothing_features = extract_clothing_features(person_roi)
        signature = tuple(clothing_features.flatten())  # Use clothing features as the signature
        mode = "clothing"

    matched_signature = None
    for known_signature, (known_features, last_seen_pos, last_seen_time) in known_signatures.items():
        # Extract features if it's in clothing mode
        if mode == "clothing":
            known_features = np.array(known_signature).reshape(1, -1)  # Convert tuple to array and reshape
            
            if compare_clothing_features(known_features, np.array(signature).reshape(1, -1)) and \
               is_close_position(person_center, last_seen_pos, config['max_distance']):
                matched_signature = known_signature
                break
        else:
            if np.array_equal(known_signature, signature) and \
               is_close_position(person_center, last_seen_pos, config['max_distance']):
                matched_signature = known_signature
                break

    if matched_signature is None:
        if signature not in known_signatures:
            known_signatures[signature] = (signature, person_center, current_time)
            log_entry(cursor, conn, hashlib.sha256(str(signature).encode()).hexdigest())  # Log the entry with the signature as a string
    else:
        if current_time - known_signatures[matched_signature][2] > config['debounce_time']:
            known_signatures[matched_signature] = (signature, person_center, current_time)


            
def process_video_stream(camera_index, video_path, config):
    conn, cursor = create_connection(config['db_path'])
    reset_occupancy(cursor, conn)
    
    cap = cv2.VideoCapture(video_path)
    known_signatures = {}

    if not cap.isOpened():
        print(f"Error: Could not open video for camera {camera_index}.")
        return

    person_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + config['cascade_path'])
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_center = (frame_width // 2, frame_height // 2)

    frame_skip = config.get('frame_skip', 5)
    frame_count = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print(f"End of video stream for camera {camera_index}.")
                break

            frame_count += 1
            if frame_count % frame_skip != 0:
                continue

            people = detect_people(frame, person_cascade)

            for (x, y, w, h) in people:
                person_center = (x + w // 2, y + h // 2)
                distance_to_center = np.linalg.norm(np.array(person_center) - np.array(frame_center))

                if distance_to_center < config['center_threshold']:
                    print(f"Person detected at the center of the frame (Camera {camera_index}).")

                    person_roi = frame[y:y+h, x:x+w]
                    current_time = time.time()
                    process_person(person_center, frame_center, person_roi, known_signatures, current_time, config, cursor, conn)

            current_occupancy = get_current_occupancy(cursor)
            print(f"Current Occupancy (Camera {camera_index}): {current_occupancy}")

    finally:
        cap.release()
        conn.close()

# Configuration file path
config = load_config('config.yaml')
# Video file path
video_path = '/workspaces/my-atttendance-tracker-with-definite-privacy/data/10827607-hd_1080_1920_30fps.mp4'

# Running for one camera to simplify debugging
process_video_stream(0, video_path, config)
