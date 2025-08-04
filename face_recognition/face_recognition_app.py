import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from keras_facenet import FaceNet
from PIL import Image
import time

# Initialize FaceNet and MediaPipe
embedder = FaceNet()
mp_face = mp.solutions.face_detection

st.set_page_config(page_title="Face Verification", layout="centered")
st.title("Face Verification via Webcam")
st.markdown(
    "Upload a reference image of your face, and the webcam will match your live face in real-time."
)

# Upload reference image
uploaded_file = st.file_uploader(
    " Upload a clear face image (JPG/PNG)", type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    # Load and display image
    ref_image = Image.open(uploaded_file).convert("RGB")
    ref_image_np = np.array(ref_image)
    st.image(ref_image_np, caption="Reference Image", width=300)

    # Detect face from image
    def detect_face(image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        with mp_face.FaceDetection(
            model_selection=1, min_detection_confidence=0.6
        ) as detector:
            results = detector.process(rgb_image)
            if results.detections:
                bbox = results.detections[0].location_data.relative_bounding_box
                h, w, _ = image.shape
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                x2 = x1 + int(bbox.width * w)
                y2 = y1 + int(bbox.height * h)
                face = rgb_image[y1:y2, x1:x2]
                return face
        return None

    # Get embedding for reference image
    ref_face = detect_face(ref_image_np)
    if ref_face is None:
        st.error(
            "No face detected in uploaded image. Please delete the image and upload an image with a face."
        )
        st.stop()

    ref_embedding = embedder.embeddings([ref_face])[0]
    st.success("Reference face successfully embedded.")

    # Create button with session-state reset
    if "webcam_active" not in st.session_state:
        st.session_state.webcam_active = False

    if st.button("📷 Start Webcam and Match"):
        st.session_state.webcam_active = True

    if st.session_state.webcam_active:
        stframe = st.empty()
        cap = cv2.VideoCapture(0)

        match_found = False
        match_time = None  # Start timer after match
        MAX_POST_MATCH_DURATION = 15  # seconds

        with mp_face.FaceDetection(
            model_selection=1, min_detection_confidence=0.6
        ) as detector:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.warning("Failed to read from webcam.")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = detector.process(frame_rgb)

                match_status = "No face"
                color = (100, 100, 100)

                if results.detections:
                    bbox = results.detections[0].location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x1 = int(bbox.xmin * w)
                    y1 = int(bbox.ymin * h)
                    x2 = x1 + int(bbox.width * w)
                    y2 = y1 + int(bbox.height * h)
                    face_crop = frame_rgb[y1:y2, x1:x2]

                    if face_crop.size != 0:
                        try:
                            emb = embedder.embeddings([face_crop])[0]
                            distance = np.linalg.norm(ref_embedding - emb)

                            if distance < 0.8:
                                match_status = f"MATCH ({distance:.2f})"
                                color = (0, 255, 0)
                                if not match_found:
                                    match_found = True
                                    match_time = time.time()
                            else:
                                match_status = f"NO MATCH ({distance:.2f})"
                                color = (0, 0, 255)
                        except Exception as e:
                            match_status = "Error"
                            print("Face embedding failed:", e)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        frame,
                        match_status,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2,
                    )

                stframe.image(frame, channels="BGR")

                # If match detected, and 15s passed, stop webcam
                if match_found and match_time:
                    elapsed = time.time() - match_time
                    if elapsed > MAX_POST_MATCH_DURATION:
                        st.success("Match confirmed.")
                        break

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            stframe.empty()
            st.session_state.webcam_active = False  # Reset so button can be reused
