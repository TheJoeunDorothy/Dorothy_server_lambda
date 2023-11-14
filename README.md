# dorothy_personel_Server

이 서버는 Dorothy 앱 배포를 위한, SAM(Serverless Application Model)CLI를 통한 Application 작성 입니다.

- dorothy_age : 나이 예측을 위한 람다 함수와 Dockerfile 이미지
- dorothy_personel : Personel Color 예측을 위한 람다 함수와 Dockerfile 이미지
- template.yaml - SAM의 구성도를 작성

이 앱은 AWS Resources, 2개의 람다 함수, API GATEWAY API 설정이 포함 되어 있습니다.  
이 모든 기술은 `template.yaml`에 작성 되어있습니다.

## 서버 구성도
<img src = https://github.com/TheJoeunDorothy/Dorothy_server_lambda/blob/main/Readme/Dorothy_구성도.png>  

## 클래스 다이어그램
### 1.dorothy_age
<img src = https://github.com/TheJoeunDorothy/Dorothy_server_lambda/blob/main/Readme/dorothy_age.png>  

### 2.dorothy_personel  

<img src = https://github.com/TheJoeunDorothy/Dorothy_server_lambda/blob/main/Readme/dorothy_personel.png> 

## 어플리케이션 배포방법

Serverless Application Model Command Line Interface(SAM CLI)는 AWS CLI의 확장 기능으로, Lambda 애플리케이션을 구축하고 테스트하는 기능을 추가합니다.  
이는 Docker를 사용하여 함수를 Lambda와 일치하는 Amazon Linux 환경에서 실행합니다.  
또한, 애플리케이션의 빌드 환경과 API를 실행할 수도 있습니다.  
SAM CLI를 사용하려면 다음 도구들이 필요합니다.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

그리고 추가적인 언어 설치가 필요합니다.
* [Python 3 installed](https://www.python.org/downloads/)

빌드 하기 위해서는 터미널에서

```bash
sam build
sam deploy --guided
```

로 설정 할수 있습니다.

## SAM CLI를 통한 빌드와 간단한 local Test

`sam build` command를 통해 빌드를 마치면,

```bash
dorothy_personel$ sam build
```
SAM CLI는 Dockerfile로부터 Docker 이미지를 빌드하고, 해당 Docker 이미지 내부에  
`${각 람다함수 프로젝트 루트}/requirements.txt`에 정의된 의존성들을 설치합니다.  
처리된 템플릿 파일은 `.aws-sam/build` 폴더에 저장됩니다.  
SAM CLI는 또한 애플리케이션의 API를 에뮬레이트할 수 있습니다.  
`sam local start-api`를 사용하여 로컬의 3000번 포트에서 API를 실행합니다.

```bash
dorothy_personel$ sam local start-api
dorothy_personel$ curl http://localhost:3000/
```

## 삭제

만든 서버 애플리케이션을 삭제하려면 AWS CLI를 이용해 다음과 같은 명령어로 삭제 할 수 있습니다. 

```bash
sam delete --stack-name "dorothy_personel"
```

## 만든이

[Oh-Kang94](https://github.com/Oh-Kang94)
