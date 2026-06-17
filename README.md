# PensionFit

GitHub Repository: https://github.com/junwon1694-create/oss_final_assignment

미래에셋 연금투자 가이드북의 생애주기별 포트폴리오 표를 바탕으로 만든 교육용 연금 포트폴리오 추천 시스템입니다.

이 프로젝트는 오픈소스소프트웨어실습 기말 대체 과제를 위해 제작되었습니다. Streamlit 프론트엔드에서 사용자의 정보를 입력받고, FastAPI 백엔드가 추천 로직을 처리한 뒤 JSON 결과를 반환합니다.

## 주요 기능

- 생애주기, 투자 유형, 연금 계좌 종류를 입력받습니다.
- FastAPI가 입력값을 미래에셋 연금투자 가이드북의 연금 포트폴리오 표에 매핑합니다.
- Streamlit은 FastAPI 응답을 받아 추천 결과를 화면에 표시합니다.
- 퇴직연금 DC와 IRP는 공격수+미드필더 합산 비중이 위험자산 70% 한도 안에 있는지 확인합니다.
- 개인연금은 레버리지·인버스형 상품을 제외하도록 안내합니다.
- Docker Compose로 Streamlit과 FastAPI를 각각 다른 컨테이너에서 실행합니다.

## 입력값

| 입력 항목 | 선택지 |
| --- | --- |
| 생애주기 | 20~30대, 40~50대, 60대 이상 |
| 투자 유형 | 성장형, 밸런스형, 안정형 |
| 연금 계좌 종류 | 개인연금, 퇴직연금 DC, IRP |

## 추천 로직 요약

1. 생애주기와 투자 유형을 가이드북의 포트폴리오 표에 매핑합니다.
2. 20~30대는 연금 성장기 성장형 또는 밸런스형을 적용합니다.
3. 40~50대는 연금 성숙기 밸런스형 또는 안정형을 적용합니다.
4. 60대 이상은 연금 인출기 밸런스형 또는 안정형을 적용합니다.
5. 계좌가 퇴직연금 DC 또는 IRP이면 위험자산 비중이 70% 이내인지 확인합니다.

## 가이드북 포메이션 비중

| 생애주기 | 적용 포메이션 | 공격수 | 미드필더 | 수비수+골키퍼 |
| --- | --- | ---: | ---: | ---: |
| 20~30대 | 성장기 성장형 | 40% | 25% | 35% |
| 20~30대 | 성장기 밸런스형 | 30% | 30% | 40% |
| 40~50대 | 성숙기 밸런스형 | 30% | 30% | 40% |
| 40~50대 | 성숙기 안정형 | 20% | 30% | 50% |
| 60대 이상 | 인출기 밸런스형 | 25% | 35% | 40% |
| 60대 이상 | 인출기 안정형 | 20% | 30% | 50% |

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
  .dockerignore
  .gitignore
  README.md
```

## Docker 실행 방법

```bash
docker compose up --build
```

실행 후 브라우저에서 아래 주소로 접속합니다.

```text
http://localhost:8501
```

FastAPI 문서는 아래 주소에서 확인할 수 있습니다.

```text
http://localhost:8000/docs
```

## API 예시

### 요청

```json
{
  "life_stage": "40~50대",
  "portfolio_type": "밸런스형",
  "account_type": "IRP"
}
```

### 응답 주요 항목

```json
{
  "profile_title": "연금 성숙기 밸런스형 포트폴리오 (밸런스형)",
  "formation_name": "연금 성숙기 밸런스형",
  "risk_asset_ratio": 60,
  "safe_asset_ratio": 40,
  "allocation": [
    {
      "asset_class": "공격수",
      "ratio": 30,
      "role": "장기 성장과 초과수익을 기대하는 주식형·테마형 자산"
    },
    {
      "asset_class": "미드필더",
      "ratio": 30,
      "role": "대표지수·배당·분산형 상품으로 성장과 안정의 균형을 잡는 자산"
    },
    {
      "asset_class": "수비수+골키퍼",
      "ratio": 40,
      "role": "채권혼합형·단기국채·금현물·TDF/TIF 등 변동성 완충 자산"
    }
  ]
}
```

## EC2 배포 체크리스트

1. EC2 인스턴스에 Docker와 Docker Compose를 설치합니다.
2. GitHub 저장소를 EC2로 clone합니다.
3. 프로젝트 폴더에서 `docker compose up --build -d`를 실행합니다.
4. 보안 그룹에서 Streamlit 포트 `8501`을 열어줍니다.
5. `docker ps`로 `pensionfit-front`, `pensionfit-back` 컨테이너가 실행 중인지 확인합니다.
6. 브라우저에서 `http://EC2_PUBLIC_IP:8501`로 접속합니다.

## 데모 영상에 포함할 내용

- EC2 주소로 Streamlit 앱 접속
- 3개 입력값 선택
- 포트폴리오 추천 버튼 클릭
- 추천 비중, 추천 이유, 상품 유형, 계좌 제한 안내 확인
- EC2 터미널에서 `docker ps` 실행
- FastAPI 문서 또는 API 응답 탭으로 백엔드 연결 확인

## 주의 문구

본 서비스는 오픈소스소프트웨어실습 과제용 교육 서비스이며, 실제 투자 권유나 투자자문이 아닙니다.
