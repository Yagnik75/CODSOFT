# 🧑‍💻 Real-Time Face Verification App (Streamlit + FaceNet + Webcam)

This is a **Streamlit-based real-time face verification application** that allows users to:

- Upload a reference image of their face  
- Activate a webcam feed  
- Detect their face live using **MediaPipe**  
- Generate **face embeddings** using a **pre-trained FaceNet model**  
- Match the live face to the uploaded reference face  
- ✅ If a match is detected, the app shows success, keeps the webcam running for 15 seconds, and then stops automatically  
- 🔁 You can restart the webcam anytime to re-verify  

---

Changes made from the original prompt.

| Component               | Prompt-Specified                     | This Project Implementation                      |
|------------------------|--------------------------------------|--------------------------------------------------|
| Face Detection         | Haar cascades / deep learning        | ✅ **MediaPipe** (deep learning-based, fast, modern) |
| Face Recognition       | ArcFace / Siamese Network            | ✅ **FaceNet (Keras)** — uses triplet loss, like Siamese |
| Media Source           | Images / Videos                      | ✅ Supports **image upload + live webcam** stream |
| Interface              | CLI or app-based                     | ✅ **Streamlit Web App** (user-friendly frontend) |

###  Why These Changes?

- **MediaPipe vs Haar Cascades:**  
  Haar cascades are outdated and less robust. MediaPipe is faster, more accurate, and works in real-time with minimal setup.

- **FaceNet vs ArcFace/Siamese:**  
  FaceNet is a well-tested face embedding model trained using a **triplet loss**, very similar in nature to Siamese Networks. It's easier to implement with available Keras packages, and performs very well in practice.

- **Streamlit UI vs CLI:**  
  A Streamlit interface makes the app interactive and beginner-friendly without needing to write or run code manually.

---

NOTE; I HAVE USED PYTHON VERSION 3.10.9 FOR THIS SO ALL THE PACKAGES HAVE THE SAME COMPATIBLE VERSIONS. I HAVE ALSO EXECUTED THIS IN A VIRTUAL ENVIRONMENT.

## 🚀 Features

- 🔍 Face detection using **MediaPipe**
- 🧠 Face embedding generation with **Keras-FaceNet**
- 🎥 Real-time webcam support using **OpenCV**
- 🖼 Upload-based face matching system
- ⏱ Webcam stops 15 seconds after successful match
- 🔁 "Start Webcam" button lets you re-verify at will
- ✅ Smooth user experience via **Streamlit**

---

## 📦 Requirements

Install all dependencies:

```bash
pip install -r requirements.txt
