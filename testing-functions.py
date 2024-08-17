import cv2

video_path = '/workspaces/my-atttendance-tracker-with-definite-privacy/data/10827607-hd_1080_1920_30fps.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
else:
    print("Video opened successfully.")

cap.release()
