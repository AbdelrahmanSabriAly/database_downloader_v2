import streamlit as st
import re
import os
import cv2
import numpy as np
import pickle

from FaceRecog import get_face_encodings

@st.cache_resource
def load_models():
    # Init models face detection & recognition
    weights_face_detect = os.path.join("models", "face_detection_yunet_2023mar_int8.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights_face_detect, "", (0, 0))
    face_detector.setScoreThreshold(0.87)

    weights_face_recog = os.path.join("models", "face_recognition_sface_2021dec_int8.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights_face_recog, "")

    return face_detector, face_recognizer

def is_valid_mac(mac):
    pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
    return bool(re.match(pattern, mac))

def main():
    
    ID = st.text_input("Enter your ID")

    if not ID:
        return

    if 'T' not in ID:
        handle_attendance_form(ID)
    else:
        handle_database_downloader()

def handle_attendance_form(ID):
    with st.form("Attendance Form"):
        st.header("Face | MAC form")
        year = st.selectbox("Year", ["First Year", "Second Year", "Third Year", "Fourth Year"])
        year = year.replace(" ", "_")

        MAC = st.text_input("Enter your MAC Address in the form of a1:b2:c3:d4:f5:g6").upper()
        img = st.file_uploader("Upload an image of your face", ['.jpg', 'png', 'heic'])
        submitted = st.form_submit_button("Submit")

        if submitted and is_valid_mac(MAC) and ID and img:
            detector, recognizer = load_models()
            image = cv2.imdecode(np.frombuffer(img.read(), np.uint8), 1)
            result = get_face_encodings(image, detector, recognizer, ID, MAC, year)

            if result:
                st.success(f"Success! Welcome: {ID}")
            else:
                st.error("The uploaded image doesn't contain any face")
        elif submitted:
            st.error("Invalid MAC or empty fields, please try again")

def handle_database_downloader():
    st.title("Database Downloader ⬇️")

    year = st.selectbox("Choose year", ["First Year", "Second Year", "Third Year", "Fourth Year"])
    year = year.replace(" ", "_")
    file_name = f"{year}_database.pkl"
    proceed_button = st.button("Proceed")

    if proceed_button:
        with open(file_name, 'rb') as file:
            existing_dict = pickle.load(file)

        st.success(f"There are {len(existing_dict[1])} students")
        st.table(existing_dict[1].items())
        st.download_button(
            label="Click here to download the database",
            data=open(file_name, "rb").read(),
            file_name=file_name,
            mime="application/octet-stream",
        )

if __name__ == "__main__":
    main()
