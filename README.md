# 📚 도서관 대여 시스템 (Library Rental System)

파이썬(Python)과 스트림릿(Streamlit)으로 만든 간단하고 직관적인 도서관 관리 프로그램입니다.
비전공자도 쉽게 이해할 수 있는 객체 지향 프로그래밍(OOP) 구조로 설계되었습니다.

## ✨ 주요 기능
1.  **도서 대여/반납**: 회원이 원하는 책을 빌리고 반납할 수 있습니다.
2.  **대출 일정 관리**: 반납 예정일을 지정하고, 연체 시 알림을 받을 수 있습니다.
3.  **도서 관리**: 신간 도서를 등록하거나 폐기할 수 있습니다.
4.  **카테고리 분류**: 문학, 과학, 인문 등 분야별로 책을 관리합니다.
5.  **임의 데이터 생성**: 매번 실행 시 다양한 예시 데이터가 자동으로 생성됩니다.

## 🛠 사용 기술 (Tech Stack)
- **Language**: Python 3.x
- **Frontend**: Streamlit
- **Logic**: Pure Python Classes (Book, Member, Library)

## 🚀 실행 방법
이 프로젝트를 다운로드 받은 후 터미널에서 아래 명령어를 입력하세요.

```bash
pip install streamlit
streamlit run app.py
```

## 📂 프로젝트 구조
- `app.py`: 웹 화면을 담당하는 메인 파일
- `library_system.py`: 도서관의 핵심 로직(클래스)이 담긴 파일
- `system_architecture.md`: 시스템 설계도 및 다이어그램
