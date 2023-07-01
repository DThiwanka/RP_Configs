# camera.py

import cv2

def capture_images():
    # Open the device's camera
    camera = cv2.VideoCapture(0)

    # Capture multiple images
    captured_images = []
    num_images = 5  # Number of images to capture
    for _ in range(num_images):
        ret, frame = camera.read()
        if ret:
            captured_images.append(frame)

    # Release the camera
    camera.release()

    return captured_images
