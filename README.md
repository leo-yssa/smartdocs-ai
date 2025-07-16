# SmartDocs-AI

**SmartDocs-AI**는 최신 LangChain, LLM, RAG(Retrieval-Augmented Generation), 벡터 검색 및 에이전트를 활용한  
지능형 문서 검색 및 질의응답 시스템입니다. 사내 문서, 매뉴얼, 지식 베이스 등 방대한 텍스트 데이터를  
자연어로 쉽고 빠르게 탐색할 수 있도록 설계되었습니다.

---

## 주요 기능

- 🔍 **RAG 기반 문서 검색**  
  벡터 임베딩과 전통적 키워드 검색을 결합하여 정확하고 빠른 문서 검색 제공
- 🤖 **LLM & 에이전트 통합**  
  최신 대형 언어 모델(LLM)과 LangChain 에이전트를 활용해 문서 내용 기반 질의응답 및 복잡한 작업 자동화 지원
- 🗂️ **다양한 문서 포맷 지원**  
  PDF, DOCX, 텍스트 파일 등 다양한 포맷에서 정보를 추출하고 색인화
- ⚙️ **확장 가능한 백엔드 아키텍처**  
  마이크로서비스 구조 및 캐시, 큐 기반 비동기 처리로 대규모 데이터도 효율적 처리
- 📊 **실시간 모니터링 & 로깅**  
  Prometheus, Grafana 등과 연동해 서비스 상태 및 쿼리 성능 모니터링

---

## 구현된 전체 플로우

- **문서 업로드/색인**: REST API로 문서(title, content) 업로드 → 임베딩 생성 및 벡터 인덱스 저장
- **검색**: 쿼리 임베딩 → 벡터 인덱스에서 유사 문서 ID/제목 반환
- **질의응답(RAG)**: 검색된 문서 본문을 LLM에 컨텍스트로 넣어 답변 생성
- **마이크로서비스 구조**: Spring Boot(Kotlin) ↔ Python(gRPC)로 분리, proto 기반 서비스/메시지 정의
- **테스트/확장성**: REST API로 전체 플로우 손쉽게 테스트, HuggingFace/로컬 LLM, PDF 등 다양한 확장도 용이

---

## 기술 스택

- **LangChain** — 체인화된 LLM 작업 흐름 구현  
- **OpenAI GPT-4 / GPT-3.5, HuggingFace/로컬 LLM** — 자연어 이해 및 생성  
- **FAISS** — 벡터 데이터베이스  
- **Spring Boot (Kotlin)** — 메인 API 서버 (gRPC 클라이언트)  
- **Python (gRPC 서버)** — AI/임베딩/검색/LLM 서비스  
- **gRPC, Protobuf** — 마이크로서비스 간 고성능 통신  
- **Docker, Kubernetes** — 컨테이너화 및 오케스트레이션  
- **Prometheus, Grafana** — 모니터링 및 알림

---

## 프로젝트 구조

```
smartdocs-ai/
├── backend-spring/         # 메인 API 서버 (Kotlin + Spring Boot, gRPC 클라이언트)
│   ├── build.gradle.kts
│   ├── settings.gradle.kts
│   ├── src/
│   │   ├── main/kotlin/com/smartdocs/...
│   │   └── main/resources/application.yml
│   └── ...
├── ai-backend/             # AI 서버 (Python, gRPC 서버)
│   ├── requirements.txt    # 의존성 명세
│   ├── .env                # 환경변수(OPENAI_API_KEY 등)
│   └── app/
│       ├── grpc_server.py  # gRPC 서버 진입점
│       ├── services/       # 임베딩, 벡터검색, LLM 등 서비스 로직
│       └── ...
├── proto/                  # gRPC 서비스/메시지 정의 proto 파일
│   └── smartdocs.proto
├── README.md
└── ...
```

---

## 설치 및 실행

### 1. Spring Boot(Kotlin) 백엔드 실행

```bash
cd backend-spring
./gradlew build
./gradlew bootRun
```
- 기본 포트: 8080
- 헬스체크: http://localhost:8080/health

### 2. AI 서버(Python, gRPC) 실행

```bash
cd ai-backend
python -m venv venv
source venv/bin/activate
pip install --upgrade --force-reinstall -r requirements.txt
# .env 파일에 OPENAI_API_KEY=sk-xxxx... 입력
python -m app.grpc_server
```
- gRPC 포트: 50051

### 3. proto 코드 생성 (Spring Boot)

Spring Boot 빌드시 proto/smartdocs.proto로부터 gRPC/Protobuf 코드 자동 생성

---

## 샘플 API 테스트

- **문서 업로드**
  ```bash
  curl -X POST "http://localhost:8080/grpc/upload" -d "title=TestDoc" -d "content=This is a test document about RAG."
  # 결과: {"documentId": "...", "message": "Document uploaded and indexed."}
  ```
- **문서 검색**
  ```bash
  curl "http://localhost:8080/grpc/search?query=RAG"
  # 결과: {"documentIds": ["..."], "titles": ["TestDoc"]}
  ```
- **질의응답(RAG)**
  ```bash
  curl "http://localhost:8080/grpc/ask?question=What%20is%20RAG%3F"
  # 결과: {"answer": "...", "contextDocuments": ["This is a test document about RAG."]}
  ```

---

## LLM 연동 옵션

- **OpenAI API**: .env에 OPENAI_API_KEY 필요, 요금제/크레딧 필요
- **HuggingFace/로컬 모델**: transformers, torch 등 설치 후 llm_service.py에서 모델 교체 가능

---

## 남은 확장/고도화 포인트

- 파일 업로드(PDF, DOCX 등) 및 본문 추출
- 사용자 인증/권한, 문서별 접근 제어
- DB 연동(문서/임베딩 영속화)
- 운영/배포(Docker, CI/CD, 모니터링 등)
- 프론트엔드 UI 연동
- 기타 엔터프라이즈 기능(알림, 감사로그 등)

---

## 기타

- FastAPI/REST 구조(main.py, api/)는 현재 미사용 (gRPC 기반)
