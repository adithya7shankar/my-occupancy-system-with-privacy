import face_recognition
import cv2
import datetime
import sqlite3
import numpy as np
from PIL import Image
import imagehash
import time

def create_connection():
    conn = sqlite3.connect('building_occupancy.db')
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

def process_video_stream(camera_index, video_path):
    conn, cursor = create_connection()
    
    # Reset the occupancy at the start of the program
    reset_occupancy(cursor, conn)
    
    cap = cv2.VideoCapture(video_path)

    known_signatures = {}  # Dictionary to store signatures with their last seen position and timestamp

    if not cap.isOpened():
        print(f"Error: Could not open video for camera {camera_index}.")
        return

    person_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_center = (frame_width // 2, frame_height // 2)

    center_threshold = 350  # Threshold to consider a person "centered" in the frame
    debounce_time = 2.0  # Minimum time between successive logs for the same person

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print(f"End of video stream for camera {camera_index}.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            people = person_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in people:
                person_center = (x + w // 2, y + h // 2)
                distance_to_center = ((person_center[0] - frame_center[0]) ** 2 + (person_center[1] - frame_center[1]) ** 2) ** 0.5

                if distance_to_center < center_threshold:
                    print(f"Person detected at the center of the frame (Camera {camera_index}).")

                    person_roi = frame[y:y+h, x:x+w]
                    face_locations = face_recognition.face_locations(person_roi)
                    face_encodings = face_recognition.face_encodings(person_roi, face_locations)

                    current_time = time.time()

                    if len(face_encodings) == 0:
                        # No face detected, use the clothes (person ROI) as the signature
                        print("No face detected, using clothes as the signature.")
                        roi_image = Image.fromarray(cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB))
                        new_signature_hash = imagehash.phash(roi_image)

                        matched_signature = None
                        for signature, data in known_signatures.items():
                            last_seen_pos, last_seen_time = data
                            if is_close_position(last_seen_pos, person_center) and (current_time - last_seen_time > debounce_time):
                                matched_signature = signature
                                break

                        if matched_signature is None:
                            known_signatures[new_signature_hash] = (person_center, current_time)
                            log_entry(cursor, conn, str(new_signature_hash))
                        else:
                            log_exit(cursor, conn, str(matched_signature))
                            known_signatures[matched_signature] = (person_center, current_time)
                    else:
                        for face_encoding in face_encodings:
                            matches = face_recognition.compare_faces(list(known_signatures.keys()), face_encoding, tolerance=0.6)
                            face_distance = face_recognition.face_distance(list(known_signatures.keys()), face_encoding)
                            best_match_index = np.argmin(face_distance) if len(face_distance) > 0 else -1

                            if best_match_index == -1 or not matches[best_match_index]:
                                known_signatures[face_encoding] = (person_center, current_time)
                                log_entry(cursor, conn, face_encoding)
                            else:
                                matched_signature = list(known_signatures.keys())[best_match_index]
                                log_exit(cursor, conn, matched_signature)
                                known_signatures[matched_signature] = (person_center, current_time)

            current_occupancy = get_current_occupancy(cursor)
            print(f"Current Occupancy (Camera {camera_index}): {current_occupancy}")

    finally:
        cap.release()
        conn.close()

# Running for one camera to simplify debugging
process_video_stream(0, '/workspaces/my-atttendance-tracker-with-definite-privacy/data/10827607-hd_1080_1920_30fps.mp4')
