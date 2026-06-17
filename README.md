# PensionFit

미래에셋 연금투자 가이드북의 생애주기별 포트폴리오 표를 기반으로 만든 교육용 연금 포트폴리오 추천 서비스입니다.

- GitHub Repository: https://github.com/junwon1694-create/oss_final_assignment
- Demo Video: https://youtu.be/9FpYHZtbyEc

## 프로젝트 개요

- Frontend: Streamlit
- Backend: FastAPI
- Deployment: Docker Compose, AWS EC2
- 추천 방식: 사용자 입력을 FastAPI로 전달하고, 백엔드가 가이드북 표에 매핑한 JSON 결과를 Streamlit 화면에 표시합니다.

## 입력값

| 입력 항목 | 선택지 |
| --- | --- |
| 생애주기 | 20~30대, 40~50대, 60대 이상 |
| 투자 유형 | 성장형, 밸런스형, 안정형 |
| 연금 계좌 종류 | 개인연금, 퇴직연금 DC, IRP |

## 추천 로직

| 생애주기 | 투자 유형 | 공격수 | 미드필더 | 수비수+골키퍼 |
| --- | --- | ---: | ---: | ---: |
| 20~30대 | 성장형 | 40% | 25% | 35% |
| 20~30대 | 밸런스형 | 30% | 30% | 40% |
| 40~50대 | 밸런스형 | 30% | 30% | 40% |
| 40~50대 | 안정형 | 20% | 30% | 50% |
| 60대 이상 | 밸런스형 | 25% | 35% | 40% |
| 60대 이상 | 안정형 | 20% | 30% | 50% |

DC/IRP 계좌는 위험자산 70% 한도를 확인하도록 안내합니다.

## 실행 방법

```bash
docker compose up --build -d
```

```text
Streamlit: http://localhost:8501
FastAPI Docs: http://localhost:8000/docs
```

## 프로젝트 구조

```text
Final_Project/
  back/
    main.py
    requirements.txt
    Dockerfile
  front/
    app.py
    requirements.txt
    Dockerfile
  docker-compose.yml
  README.md
```

## 주의

본 서비스는 오픈소스소프트웨어실습 과제용 교육 서비스이며, 실제 투자 권유나 투자자문이 아닙니다.
