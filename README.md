# 📚 KU Database Term Project

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](https://html.spec.whatwg.org/)

고려대학교 데이터베이스 수업의 텀 프로젝트로 개발한 **온라인 강의 등록 및 결제 시스템**입니다. Flask와 PostgreSQL을 활용하여 구현한 풀스택 웹 애플리케이션입니다.

---

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [데이터베이스 설계](#-데이터베이스-설계)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [시작하기](#-시작하기)
- [사용자 역할](#-사용자-역할)
- [핵심 기능 설명](#-핵심-기능-설명)
- [데이터베이스 스키마](#-데이터베이스-스키마)
- [개발 히스토리](#-개발-히스토리)

---

## 🎯 프로젝트 개요

이 프로젝트는 **온라인 강의 플랫폼**을 구현한 데이터베이스 시스템입니다. 강의를 등록하고 판매하는 튜터(tutor)와 강의를 구매하는 튜티(tutee) 간의 거래를 관리하며, 사용자 등급 시스템과 할인 혜택을 포함한 완전한 결제 프로세스를 구현합니다.

### 프로젝트의 특징

- 💳 **크레딧 기반 결제 시스템**: 가상 크레딧을 사용한 강의 구매
- 🏆 **등급 시스템**: 사용 금액에 따른 사용자 등급 부여 (Gold, Silver, Bronze, Welcome)
- 🎁 **할인 혜택**: 등급별 차등 할인율 적용
- 👥 **역할 분리**: Tutor와 Tutee로 구분된 사용자 인터페이스
- 🔐 **인증 시스템**: 로그인 및 회원가입 기능
- 📊 **관리자 대시보드**: 전체 시스템 관리 및 모니터링

---

## ✨ 주요 기능

### 1. 사용자 관리

- **회원가입**: ID, 비밀번호, 역할(Tutor/Tutee) 선택
- **로그인**: 사용자 인증 및 역할별 페이지 제공
- **등급 시스템**: 
  - Gold: 500,000 크레딧 이상 (2.5% 할인)
  - Silver: 100,000 크레딧 이상 (1% 할인)
  - Bronze: 50,000 크레딧 이상 (0.5% 할인)
  - Welcome: 신규 회원 (0% 할인)

### 2. 강의 관리 (Tutor)

- **강의 등록**: 과목 코드, 강의명, 가격 설정
- **수강생 확인**: 자신의 강의를 수강하는 학생 목록 조회
- **수익 관리**: 강의 판매로 인한 크레딧 증가

### 3. 강의 수강 (Tutee)

- **강의 검색**: 전체 강의 목록 조회
- **강의 등록**: 원하는 강의 선택 및 결제
- **할인 적용**: 등급에 따른 자동 할인 적용
- **수강 내역**: 등록한 강의 목록 확인

### 4. 결제 시스템

- **크레딧 기반 결제**: 가상 화폐 시스템
- **자동 할인 계산**: 등급별 할인율 자동 적용
- **거래 안전성**: 
  - 크레딧 부족 시 결제 차단
  - 자신의 강의 구매 차단
  - 중복 구매 차단

### 5. 관리자 기능

- **사용자 관리**: 전체 사용자 목록 조회
- **강의 관리**: 전체 강의 목록 조회
- **과목 관리**: 새로운 과목 추가
- **통계 확인**: 인기 강의 조회

---

## 🗃️ 데이터베이스 설계

### ERD (Entity-Relationship Diagram)

```
┌──────────────┐       ┌──────────────┐
│    users     │       │   subject    │
├──────────────┤       ├──────────────┤
│ id (PK)      │       │ code (PK)    │
│ password     │       │ subject_name │
└──────┬───────┘       └──────┬───────┘
       │                      │
       │                      │
       ├──────────────────────┼──────────────┐
       │                      │              │
       │                      │              │
┌──────▼───────┐       ┌─────▼──────┐  ┌────▼──────────┐
│   account    │       │  lecture   │  │  enrollment   │
├──────────────┤       ├────────────┤  ├───────────────┤
│ id (PK,FK)   │       │ code (FK)  │  │ tutee (FK)    │
│ credit       │       │ name       │  │ tutor (FK)    │
│ rating (FK)  │       │ price      │  │ code (FK)     │
│ role         │       │ tutor (FK) │  │ lecture_name  │
└──────┬───────┘       └────────────┘  │ lecture_price │
       │                                └───────────────┘
       │
┌──────▼───────┐
│ rating_info  │
├──────────────┤
│ rating (PK)  │
│ condition    │
│ discount     │
└──────────────┘
```

### 테이블 관계

1. **users** ↔ **account**: 1:1 관계
2. **users** ↔ **lecture**: 1:N 관계 (Tutor가 여러 강의 개설)
3. **subject** ↔ **lecture**: 1:N 관계 (하나의 과목에 여러 강의)
4. **users** ↔ **enrollment**: M:N 관계 (다대다 관계)
5. **rating_info** ↔ **account**: 1:N 관계

---

## 🛠 기술 스택

### Backend

| 기술 | 용도 |
|------|------|
| **Python 3.x** | 프로그래밍 언어 |
| **Flask** | 웹 프레임워크 |
| **psycopg2** | PostgreSQL 데이터베이스 어댑터 |

### Frontend

| 기술 | 용도 |
|------|------|
| **HTML5** | 마크업 언어 |
| **Jinja2** | Flask 템플릿 엔진 |

### Database

| 기술 | 용도 |
|------|------|
| **PostgreSQL** | 관계형 데이터베이스 |

---

## 📁 프로젝트 구조

```
KU_database_term/
├── app.py                      # Flask 애플리케이션 메인 파일
├── term.sql                    # 데이터베이스 스키마 및 초기 데이터
├── psycopg2_test1.py          # PostgreSQL 연결 테스트 1
├── psycopg2_test2.py          # PostgreSQL 연결 테스트 2
└── templates/                  # HTML 템플릿 파일
    ├── welcome.html            # 로그인/회원가입 페이지
    ├── signup.html             # 회원가입 폼
    ├── main_basic_admin.html   # 관리자 메인 페이지
    ├── main_basic_tutor.html   # 튜터 메인 페이지
    ├── main_basic_tutee.html   # 튜티 메인 페이지
    ├── main_tutor.html         # 튜터 상세 정보 페이지
    ├── main_tutee.html         # 튜티 상세 정보 페이지
    ├── lecture_add.html        # 강의 추가 페이지
    ├── lecture_payment.html    # 강의 결제 페이지
    ├── subject_add.html        # 과목 추가 페이지
    ├── print_user_table.html   # 사용자 테이블 출력
    ├── print_lecture_table.html # 강의 테이블 출력
    └── print_enrollment_table.html # 수강 테이블 출력
```

---

## 🚀 시작하기

### 필요 조건

- Python 3.x
- PostgreSQL 13+
- pip (Python 패키지 관리자)

### 설치 및 실행

1. **저장소 클론**

```bash
git clone https://github.com/eojin16/KU_database_term.git
cd KU_database_term
```

2. **필요한 패키지 설치**

```bash
pip install flask psycopg2
```

3. **PostgreSQL 데이터베이스 설정**

```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE term;

# term 데이터베이스에 연결
\c term

# 스키마 및 초기 데이터 로드
\i term.sql
```

4. **애플리케이션 실행**

```bash
python app.py
```

5. **브라우저에서 확인**

[http://localhost:5000](http://localhost:5000)을 열어 애플리케이션을 확인하세요.

---

## 👥 사용자 역할

### 1. Admin (관리자)

**기본 계정:**
- ID: `admin`
- Password: `0000`
- Credit: 10,000,000
- Rating: Gold

**권한:**
- 전체 사용자 조회
- 전체 강의 조회
- 과목 추가
- 등급 정보 조회
- 인기 강의 통계 확인

### 2. Tutor (강사)

**기능:**
- 강의 등록
- 자신의 강의 수강생 조회
- 강의 판매 수익 확인
- 다른 강의 수강 (Tutee로서)

### 3. Tutee (수강생)

**기능:**
- 강의 검색 및 조회
- 강의 등록 (결제)
- 수강 내역 확인
- 등급별 할인 혜택

---

## 🔧 핵심 기능 설명

### 1. 회원가입 프로세스

```python
@app.route('/create', methods=['post'])
def create():
    # 1. 사용자 입력 데이터 수집
    # 2. ID 중복 확인
    # 3. users 테이블에 사용자 정보 삽입
    # 4. account 테이블에 계정 정보 삽입
    #    - 초기 크레딧: 10,000
    #    - 초기 등급: welcome
```

### 2. 로그인 프로세스

```python
@app.route('/register', methods=['post'])
def register():
    # 1. ID, Password 확인
    # 2. 사용자 정보 조회
    # 3. 역할(role)에 따라 페이지 분기
    #    - admin → 관리자 페이지
    #    - tutor → 튜터 페이지
    #    - tutee → 튜티 페이지
```

### 3. 강의 결제 시스템

```python
@app.route('/payment', methods=['post'])
def payment():
    # 1. 결제 유효성 검증
    #    - 크레딧 충분 여부 확인
    #    - 자신의 강의인지 확인
    #    - 중복 수강 여부 확인
    # 2. 크레딧 차감 (할인 적용)
    # 3. 튜터에게 크레딧 지급
    # 4. enrollment 테이블에 기록
    # 5. 사용자 등급 업데이트
```

### 4. 할인 계산 로직

```python
# 사용자 등급에 따른 할인율 적용
@app.route('/register_lecture', methods=['post'])
def register_lecture():
    # 1. 강의 정보 조회
    # 2. 사용자 등급 확인
    # 3. 등급별 할인율 조회
    # 4. 최종 가격 계산
    #    total_price = 원가
    #    discount_price = 원가 * 할인율 / 100
    #    final_price = 원가 - 할인금액
```

---

## 📊 데이터베이스 스키마

### users 테이블
```sql
CREATE TABLE users (
    id VARCHAR(15) NOT NULL,
    password VARCHAR(20) NOT NULL,
    PRIMARY KEY (id)
);
```

### subject 테이블
```sql
CREATE TABLE subject (
    code VARCHAR(2) NOT NULL,
    subject_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (code)
);
```

### lecture 테이블
```sql
CREATE TABLE lecture (
    code VARCHAR(2) NOT NULL,
    name VARCHAR(20) NOT NULL,
    price INT NOT NULL CHECK (price >= 0),
    tutor VARCHAR(15) NOT NULL,
    PRIMARY KEY (code, name, price, tutor),
    FOREIGN KEY (code) REFERENCES subject (code),
    FOREIGN KEY (tutor) REFERENCES users (id)
);
```

### enrollment 테이블
```sql
CREATE TABLE enrollment (
    tutee VARCHAR(15) NOT NULL,
    tutor VARCHAR(15) NOT NULL,
    code VARCHAR(2) NOT NULL,
    lecture_name VARCHAR(20) NOT NULL,
    lecture_price INT NULL CHECK (lecture_price >= 0),
    FOREIGN KEY (tutee) REFERENCES users (id),
    FOREIGN KEY (tutor) REFERENCES users (id),
    FOREIGN KEY (code) REFERENCES subject (code)
);
```

### rating_info 테이블
```sql
CREATE TABLE rating_info (
    rating VARCHAR(10) NOT NULL,
    condition INT NOT NULL CHECK (condition >= 0),
    discount NUMERIC(4,2) NOT NULL CHECK (100 > discount AND discount >= 0),
    PRIMARY KEY (rating)
);
```

### account 테이블
```sql
CREATE TABLE account (
    id VARCHAR(15) NOT NULL,
    credit INT NOT NULL CHECK (credit >= 0),
    rating VARCHAR(10) NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('tutor', 'tutee')),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES users (id),
    FOREIGN KEY (rating) REFERENCES rating_info (rating)
);
```

---

## 📈 개발 히스토리

### v1.0 (2023년 5월 31일)
- ✅ **최종 완성**: 모든 기능 구현 완료
- ✅ HTML 파일 최적화
- ✅ SQL 스키마 최종 확정

### v0.9 (2023년 5월 30일)
- ✅ 강의 결제 시스템 구현
- ✅ 등급 시스템 및 할인 로직 완성

### v0.8 (2023년 5월 22일)
- ✅ 관리자 기능 구현
- ✅ 인기 강의 조회 기능
- ✅ 강의 조회 페이지 완성

### v0.7 (2023년 5월 21일)
- ✅ 사용자 정보 페이지 구현
- ✅ 로그인 시스템 완성

---

## 💡 주요 학습 내용

이 프로젝트를 통해 다음 개념을 학습하고 적용했습니다:

1. **관계형 데이터베이스 설계**
   - ERD 설계
   - 정규화 (1NF, 2NF, 3NF)
   - 외래키 제약조건

2. **SQL 쿼리 작성**
   - CRUD 연산
   - JOIN 연산 (INNER JOIN)
   - GROUP BY 및 집계 함수
   - 서브쿼리

3. **웹 애플리케이션 개발**
   - Flask 프레임워크
   - Jinja2 템플릿 엔진
   - RESTful 라우팅

4. **비즈니스 로직 구현**
   - 트랜잭션 처리
   - 데이터 검증
   - 에러 핸들링

---

## 🔍 주요 쿼리 예시

### 인기 강의 조회
```sql
SELECT e.lecture_name, s.subject_name, e.tutor, COUNT(*) AS number_of_enrollments 
FROM enrollment e 
INNER JOIN subject s ON e.code = s.code 
GROUP BY e.lecture_name, s.subject_name, e.tutor 
ORDER BY COUNT(*) DESC 
LIMIT 1;
```

### 사용자 등급 업데이트
```sql
SELECT rating FROM rating_info 
WHERE condition < %s 
ORDER BY condition DESC 
LIMIT 1;
```

### 수강 내역 조회 (JOIN 사용)
```sql
SELECT DISTINCT subject.subject_name, enrollment.lecture_name, enrollment.tutor, enrollment.lecture_price 
FROM enrollment 
JOIN subject ON subject.code = enrollment.code 
WHERE enrollment.tutee = %s;
```

---

## 🚧 향후 개선 사항

- [ ] 강의 평가 및 리뷰 시스템
- [ ] 강의 카테고리 필터링
- [ ] 크레딧 충전 기능
- [ ] 환불 시스템
- [ ] 실시간 알림 기능
- [ ] 비밀번호 암호화 (bcrypt)
- [ ] 세션 관리 개선
- [ ] RESTful API 구현
- [ ] 프론트엔드 프레임워크 도입 (React/Vue)

---

## 📝 라이선스

이 프로젝트는 고려대학교 데이터베이스 수업의 텀 프로젝트로 제작되었습니다.

---

## 🙏 감사의 글

- 고려대학교 데이터베이스 수업
- Flask 및 PostgreSQL 커뮤니티

---

<p align="center">
  Made with ❤️ for KU Database Course
</p>

<p align="center">
  <sub>Last Updated: May 2023</sub>
</p>
