import base64
import json
from io import BytesIO
import cv2
import dlib
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
from PIL import Image

def lambda_handler(event, context):
    ## Properties
    target_size = (128, 128)
    padding_size = (184, 184)
    brightness_adjustment = 83.15755552578428
    
    if not "body" in event or len(event["body"]) == 0:
        return {"statusCode": 400, "body": json.dumps({"result": 'No Body'})}
    image_data = event['body']

    '''이미지 처리 및 디코딩'''
    try:
        # Base64 디코딩을 통해 이미지를 복원
        image = base64.b64decode(image_data)
        # Pillow를 사용하여 이미지로 디코딩
        image = Image.open(BytesIO(image))
        # 이미지 불러오기 (Image -> Numpy Array)
        img = np.array(image)
        
    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({"result": "Can't decode image or make numpy"})}
    
    '''얼굴 인식 및 처리 '''
    try:
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # BGR GRAY 색상 변환 (PIL은 RGB 순서이므로 RGB->BGR 변환 후 GRAY 색상 변환)
        detector = dlib.get_frontal_face_detector()
        faces = detector(img, 1)

        if len(faces) > 0:
            face = faces[0]
            x = face.left()
            y = face.top()
            w = face.right() - x
            h = face.bottom() - y

            imgCrop = img_bgr[y:y+h, x:x+w]
            # 잘린 이미지 사이즈 조절 (128,128)
            face_resized = cv2.resize(imgCrop, target_size)

            # 패딩 사이즈 설정
            padded_face = np.zeros((*padding_size, 3), dtype=np.uint8)

            x_offset = (padding_size[0]-target_size[0])//2
            y_offset = (padding_size[1]-target_size[1])//2

    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({"result": "Can't find face"})}

    '''이미지 밝기 조절 '''
    try:
        padded_face[y_offset:y_offset+target_size[1],
                    x_offset:x_offset+target_size[0]] = face_resized

        # 학습된 이미지 평균 밝기로 밝기 조절
        adjusted_image = padded_face.astype(
            float) - np.mean(padded_face) + brightness_adjustment

        # 음수 값은 0으로 설정, 초과하는 값은 최댓값인 255로 설정
        adjusted_image = np.clip(adjusted_image, 0, 255)

    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({"result": "Can't bright images"})}

    '''이미지 사이즈 조절'''
    try:
        img2 = Image.fromarray(adjusted_image.astype('uint8'))
        img2 = img2.convert('L')

        train = np.zeros(1*184*184, dtype=np.int32).reshape(1, 184, 184)

        img = np.array(img2, dtype=np.int32)
        train[0, :, :] = img

        train = train.reshape(-1, 184 * 184)

        df = pd.DataFrame(train)

    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({"result": "Can't resize images"})}

    '''DL 모델 예측'''
    try:
        width, height, channel = 184, 184, 1  # 이미지 사이즈 184*184 pixel

        x_train = df.values

        x_train = x_train.reshape(
            (x_train.shape[0], width, height, channel))

        X = (x_train-127.5)/127.5
        pred = load_model('/var/task/static/32_64_64_10_model.h5').predict(X)

    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({"result": "Can't predict Age"})}

    classes = ['10대', '20대', '30대', '40대', '50대', '60대', '70대']
    faceAge, percent = classes[np.argmax(pred)], pred

    ## list comprehension
    '''
    flat_data = []
    for sublist in percent:
        for item in sublist:
            flat_data.append(item)
    ''' 
    flat_data = [item for sublist in percent for item in sublist]

    return {"statusCode": 200, 
            "body": json.dumps({
                'age': faceAge, 
                'percent' : eval(str(flat_data))
                })
            }
