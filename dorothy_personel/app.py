import base64
import warnings
import numpy as np
import joblib
from PIL import Image
from io import BytesIO
import json
import dlib

def lambda_handler(event, context):
    warnings.filterwarnings('ignore')
    if not "body" in event or len(event["body"]) == 0:
        return {"statusCode": 400, "body": json.dumps({"result": 'No Body'})}
    image_data = event['body']

    '''이미지 처리 및 디코딩 '''
    try:
        # Base64 디코딩을 통해 이미지를 복원
        image = base64.b64decode(image_data)

        # Pillow를 사용하여 이미지로 디코딩
        image = Image.open(BytesIO(image))

        # 이미지를 numpy 배열로 변환
        image = np.array(image)
    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({"result": "Can't decode image or make numpy"})}

    '''얼굴 인식 및 처리 '''
    try:
        # 얼굴 검출기 초기화
        face_detector = dlib.get_frontal_face_detector()

        # 얼굴 영역 검출
        faces = face_detector(image)

        # 얼굴 랜드마크 검출기 초기화
        landmark_predictor = dlib.shape_predictor(
            '/var/task/static/shape_predictor_68_face_landmarks.dat')
        
    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({"result": "Can't find face"})}
    
    '''이미지 ML 처리 '''
    try:
        for face in faces:
            # 얼굴 랜드마크 검출
            landmarks = landmark_predictor(image, face)

            # 미간 자리 좌표 추출 (27부터 30까지의 인덱스 사용)
            forehead_points = np.array(
                [(landmarks.part(i).x, landmarks.part(i).y) for i in range(27, 31)])

            # 해당 영역의 색상 추출
            forehead_color_rgb = np.mean(
                image[forehead_points[:, 1], forehead_points[:, 0]], axis=0)

            r = forehead_color_rgb[0]
            g = forehead_color_rgb[1]
            b = forehead_color_rgb[2]
            clf = joblib.load("/var/task/static/voting_clf.h5")
            pre = clf.predict([[r, g, b]])

    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({"result": "Can't predict Personel Color"})}
        
    return {"statusCode": 200, "body": json.dumps({"result": pre[0]})}

