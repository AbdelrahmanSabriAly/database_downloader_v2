import os
import time
import cv2
import pickle


COSINE_THRESHOLD = 0.5

def match(recognizer, feature1, dictionary):
    max_score = 0.0
    sim_user_id = ""
    for user_id, feature2 in zip(dictionary.keys(), dictionary.values()):
        score = recognizer.match(
            feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
        if score >= max_score:
            max_score = score
            sim_user_id = user_id
    if max_score < COSINE_THRESHOLD:
        return False, ("", 0.0)
    return True, (sim_user_id, max_score)

def recognize_face(image, face_detector, face_recognizer, file_name=None):
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    if image.shape[0] > 1000:
        image = cv2.resize(image, (0, 0),
                           fx=500 / image.shape[0], fy=500 / image.shape[0])

    height, width, _ = image.shape
    face_detector.setInputSize((width, height))
    try:
        dts = time.time()
        _, faces = face_detector.detect(image)
        if file_name is not None:
            assert len(faces) > 0, f'the file {file_name} has no face'

        faces = faces if faces is not None else []
        features = []
        print(f'time detection  = {time.time() - dts}')
        for face in faces:
            rts = time.time()

            aligned_face = face_recognizer.alignCrop(image, face)
            feat = face_recognizer.feature(aligned_face)
            print(f'time recognition  = {time.time() - rts}')

            features.append(feat)
        return features, faces
    except Exception as e:
        print(e)
        print(file_name)
        return None, None


def get_face_encodings(image,face_detector,face_recognizer,id,mac,year):
    feats, faces = recognize_face(
        image, face_detector, face_recognizer)

    if len(faces) == 0:
        return False
    if os.path.exists(f'{year}_database.pkl'):
        # Open the pickle file to load the existing dictionary
        with open(f'{year}_database.pkl', 'rb') as file:
            existing_dict = pickle.load(file)

        # Append a new item to the existing dictionary
        existing_dict[0][id] = feats[0]
        existing_dict[1][id] = mac

        # Save the updated dictionary back to the pickle file
        with open(f'{year}_database.pkl', 'wb') as file:
            pickle.dump(existing_dict, file)

    else:
        face_dictionary = {}
        mac_dictionary = {}
        face_dictionary[id] = feats[0]
        mac_dictionary[id] = mac
        with open(f'{year}_database.pkl', 'wb') as f:
            pickle.dump([face_dictionary,mac_dictionary], f)
    return True
