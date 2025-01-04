import cv2
import numpy as np

# Load the reference image (the face you want to recognize)
reference_img_path = "IMG_20190111_195807.jpg"
reference_img = cv2.imread(reference_img_path)

if reference_img is None:
    print(f"Error: Could not load reference image from {reference_img_path}")
    exit(1)

# Convert the reference image to grayscale
reference_gray = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

if face_cascade.empty():
    print("Error: Could not load Haar Cascade.")
    exit(1)

# Detect the face in the reference image
reference_faces = face_cascade.detectMultiScale(reference_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

if len(reference_faces) == 0:
    print("No face detected in the reference image.")
    exit(1)

# Extract the first detected face region
(x, y, w, h) = reference_faces[0]
reference_face = reference_gray[y:y+h, x:x+w]

# Initialize the video capture
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use CAP_DSHOW for Windows

if not video_capture.isOpened():
    print("Error: Could not open camera.")
    exit(1)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    # Convert the frame to grayscale for face detection
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # Extract face region from the frame
            detected_face = frame_gray[y:y+h, x:x+w]

            # Resize both faces to the same size for comparison
            detected_face_resized = cv2.resize(detected_face, (reference_face.shape[1], reference_face.shape[0]))

            # Compute similarity using Template Matching (TM_CCOEFF_NORMED)
            result = cv2.matchTemplate(detected_face_resized, reference_face, cv2.TM_CCOEFF_NORMED)
            max_similarity = np.max(result)

            # Display match or no match
            if max_similarity > 0.6:  # Adjust threshold as needed
                cv2.putText(frame, "Match", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No Match", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    else:
        # If no faces are detected in the frame
        cv2.putText(frame, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()

