import argparse
import os
import warnings
import serial

import ArcFace
import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing import image

warnings.filterwarnings("ignore")

# 아두이노와의 시리얼 통신 설정
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

model = ArcFace.load_model()
face_detector = MTCNN()

def detect_face(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detections = face_detector.detect_faces(img_rgb)
    detection = detections[0]
    x, y, w, h = detection["box"]
    detected_face = img[int(y):int(y+h), int(x):int(x+w)]
    return detected_face

def preprocess_face(img, target_size=(112, 112)):
    img = detect_face(img)
    img = cv2.resize(img, target_size)
    img_pixels = image.img_to_array(img)
    img_pixels = np.expand_dims(img_pixels, axis=0)
    img_pixels /= 255
    return img_pixels

def img_to_encoding(img, use_model=False):
    img = preprocess_face(img)
    if use_model:
        return model.predict(img)[0]
    else:
        return img

def calculate_cosine_similarity(array1, array2):
    return cosine_similarity(array1.reshape(1, -1), array2.reshape(1, -1))[0][0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get the encoding of two images")
    parser.add_argument('--image1_path', default='/home/twin0905/Desktop/Face_recognition/img1.jpg')
    parser.add_argument('--use_model', default=False, type=bool)

    args = parser.parse_args()

    # 이미지 1 경로
    path_to_image1 = args.image1_path

    # 이미지 2 캡쳐
    camera = cv2.VideoCapture(0)
    ret, img2 = camera.read()
    camera.release()

    if not ret:
        print("Failed to capture image from camera.")
        exit()

    # 이미지 1 인코딩
    encoding1 = img_to_encoding(cv2.imread(path_to_image1), args.use_model)

    # 이미지 2 인코딩
    encoding2 = img_to_encoding(img2, args.use_model)

    # 유사도 계산
    similarity = calculate_cosine_similarity(encoding1, encoding2)

    print(f"Cosine similarity between the two entities: {similarity:.4f}")

    # 유사도 임계값 설정 (예: 0.5 이상일 경우 잠금 해제)
    threshold = 0.5
    if similarity >= threshold:
        ser.write(b'Unlock\n')
    else:
        ser.write(b'Lock\n')
