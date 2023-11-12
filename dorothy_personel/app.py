import base64
import warnings
import numpy as np
import joblib
from PIL import Image
from io import BytesIO
import json
import dlib
import os

def lambda_handler(event, context):
    if not "body" in event or len(event["body"]) == 0:
        return {"statusCode": 400, "body": json.dumps({"result": 'No Body'})}
    image_data = event['body']
    print("Image data received")  # 로그 추가

    
    print(os.listdir('/var/task/static'))
    print(os.stat('/var/task/static/shape_predictor_68_face_landmarks.dat'))


    # Base64 디코딩을 통해 이미지를 복원
    image = base64.b64decode(image_data)
    print("Image decoded from base64")  # 로그 추가

    # Pillow를 사용하여 이미지로 디코딩
    image = Image.open(BytesIO(image))
    print("Image decoded with Pillow")  # 로그 추가

    # 이미지를 numpy 배열로 변환
    image = np.array(image)
    print("Image converted to numpy array")  # 로그 추가

    try:
        warnings.filterwarnings('ignore')

        # 얼굴 검출기 초기화
        face_detector = dlib.get_frontal_face_detector()
        print("Face detector initialized")  # 로그 추가

        # 얼굴 영역 검출
        faces = face_detector(image)
        print("Faces detected")  # 로그 추가

        # 얼굴 랜드마크 검출기 초기화
        landmark_predictor = dlib.shape_predictor(
            '/var/task/static/shape_predictor_68_face_landmarks.dat')
        print("Landmark predictor initialized")  # 로그 추가

        for face in faces:
            # 얼굴 랜드마크 검출
            landmarks = landmark_predictor(image, face)
            print("Landmarks detected")  # 로그 추가

            # 미간 자리 좌표 추출 (27부터 30까지의 인덱스 사용)
            forehead_points = np.array(
                [(landmarks.part(i).x, landmarks.part(i).y) for i in range(27, 31)])
            print("Forehead points extracted")  # 로그 추가

            # 해당 영역의 색상 추출
            forehead_color_rgb = np.mean(
                image[forehead_points[:, 1], forehead_points[:, 0]], axis=0)
            print("Forehead color extracted")  # 로그 추가

            r = forehead_color_rgb[0]
            g = forehead_color_rgb[1]
            b = forehead_color_rgb[2]
            clf = joblib.load("/var/task/static/voting_clf.h5")
            pre = clf.predict([[r, g, b]])

    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"result": str(e)})}
        
    return {"statusCode": 200, "body": json.dumps({"result": pre[0]})}

