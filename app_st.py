import streamlit as st
import re
import os
import cv2
import numpy as np

from FaceRecog import get_face_encodings

@st.cache_resource
def load_models():
    # Init models face detection & recognition
    weights = os.path.join( "models",
                            "face_detection_yunet_2023mar_int8.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    face_detector.setScoreThreshold(0.87)

    weights = os.path.join( "models", "face_recognition_sface_2021dec_int8.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")

    return face_detector,face_recognizer



def is_valid_mac(mac):
    # pattern = r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$'
    pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
    if re.match(pattern,mac):
        return True
    else:
        return False


with st.form("Attendance Form"):
    st.title("Attendance system")
    year = st.selectbox("Year",["First Year","Second Year","Third Year","Fourth Year"])
    year = year.replace(" ","_")
    ID = st.text_input("Enter you ID")
    MAC = st.text_input("Enter your MAC Address in the form of a1:b2:c3:d4:f5:g6")
    MAC = MAC.upper()
    img = st.file_uploader("Upload an image of you face",['.jpg','png','heic'])
    submitted = st.form_submit_button("Submit")

    if submitted:
        if ID and MAC and img:
            if not is_valid_mac(MAC):
                st.error("Invalid MAC, please try again")
            else:
                detector,recognizer = load_models()
                image = cv2.imdecode(np.frombuffer(img.read(), np.uint8), 1)
                result = get_face_encodings(image,detector,recognizer,ID,MAC,year)
                if result:
                    st.success(f"Success! Welcome: {ID}")
                else:
                    st.error("The uploaded image doesn't contain any face")
        else:
            st.error("Empty fields, please make sure to fill or fields")
