import cv2
import sys
import os

# List of video files
video_files = ['video1.mp4', 'video2.mp4', 'video3.mp4']

for video in video_files:
    if not os.path.exists(video):
        print(f"Error: {video} not found!")
        sys.exit(1)

for video_file in video_files:
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Error loading {video_file}")
        continue

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Sequence', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            sys.exit(0)
    cap.release()

cv2.destroyAllWindows()

print("Sequence finished!")
