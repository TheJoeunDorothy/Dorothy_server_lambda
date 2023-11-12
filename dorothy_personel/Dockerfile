FROM public.ecr.aws/lambda/python:3.11

# 필요한 시스템 패키지 설치
RUN yum install -y gcc gcc-c++ make cmake pkgconfig poppler-cpp-devel \
    openblas-devel \
    lapack-devel \
    libX11-devel \
    gtk3-devel \
    atlas-devel

# 애플리케이션을 위한 디렉토리 생성
WORKDIR /var/task

# Python 라이브러리 설치
COPY requirements.txt ./
RUN python3.11 -m pip install -r requirements.txt -t .

# 애플리케이션 코드 복사
COPY app.py ./

# 필요한 모델 파일 복사
COPY static/* ./static/
# Static은 잘 있나 확인하기
RUN ls /var/task/static
# 모든 권한 부여
RUN chmod -R 777 /var/task/static

CMD ["app.lambda_handler"]


# COPY static/shape_predictor_68_face_landmarks.dat ./static/shape_predictor_68_face_landmarks.dat
# COPY static/voting_clf.h5 ./static/voting_clf.h5
