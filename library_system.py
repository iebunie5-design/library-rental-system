# library_system.py

# 1. Book (책) 클래스: 붕어빵 틀 1
# 책이라면 가지고 있어야 할 정보들을 정의합니다.
class Book:
    def __init__(self, title, author, category="기타"):
        self.title = title          # 책 제목
        self.author = author        # 저자
        self.category = category    # 카테고리 (New!)
        self.is_available = True    # 대출 가능 여부
        self.due_date = None        # 반납 예정일

    def __str__(self):
        return f"BOOK [{self.title}] by {self.author}"


# 2. Member (회원) 클래스: 붕어빵 틀 2
# 회원이라면 가지고 있어야 할 정보들을 정의합니다.
class Member:
    def __init__(self, name):
        self.name = name            # 회원 이름
        self.borrowed_books = []    # 빌린 책 목록 (처음엔 비어있음)

    def __str__(self):
        return f"MEMBER [{self.name}]"


# 3. Library (도서관) 클래스: 붕어빵 틀 3
# 책과 회원을 관리하는 관리자 역할을 합니다.
class Library:
    def __init__(self):
        self.books = []     # 도서관이 소장한 책 리스트 (책장)
        self.members = []   # 등록된 회원 리스트 (회원명부)

    # 책을 도서관에 등록하는 기능
    def add_book(self, book):
        self.books.append(book)
        print(f"📖 입고 완료: '{book.title}' 책이 도서관에 들어왔습니다.")

    # [NEW] 책을 폐기하는 기능
    def remove_book(self, book_title):
        book_to_remove = None
        for book in self.books:
            if book.title == book_title:
                book_to_remove = book
                break
        
        if book_to_remove:
            self.books.remove(book_to_remove)
            print(f"🗑️ 폐기 완료: '{book_title}' 책을 도서관에서 치웠습니다.")
        else:
            print(f"⚠️ 오류: '{book_title}' 책을 찾을 수 없습니다.")


    # 회원을 등록하는 기능
    def register_member(self, member):
        self.members.append(member)
        print(f"👤 회원 가입: '{member.name}' 님이 등록되었습니다.")

    # 책을 빌려주는 기능 (due_date 추가)
    def rent_book(self, member, book_title, due_date=None):
        # 1. 먼저 책을 찾습니다.
        book_to_rent = None
        for book in self.books:
            if book.title == book_title:
                book_to_rent = book
                break
        
        # 2. 책이 있고, 대출 가능한 상태인지 확인합니다.
        if book_to_rent and book_to_rent.is_available:
            book_to_rent.is_available = False       # 대출중으로 변경
            book_to_rent.due_date = due_date        # 반납 예정일 설정
            member.borrowed_books.append(book_to_rent) # 회원 대출 목록에 추가
            print(f"✅ 대출 성공: '{member.name}' 님이 '{book_title}'을(를) 빌렸습니다. (반납일: {due_date})")
        else:
            print(f"❌ 대출 실패: '{book_title}' 책을 찾을 수 없거나 이미 대출 중입니다.")

    # 책을 반납받는 기능
    def return_book(self, member, book_title):
        book_to_return = None
        # 회원이 빌린 책 목록에서 찾기
        for book in member.borrowed_books:
            if book.title == book_title:
                book_to_return = book
                break
        
        if book_to_return:
            book_to_return.is_available = True      # 다시 대출 가능으로 변경
            book_to_return.due_date = None          # 반납 예정일 초기화
            member.borrowed_books.remove(book_to_return) # 회원 대출 목록에서 제거
            print(f"↩️ 반납 완료: '{book_title}'이(가) 반납되었습니다.")
        else:
            print(f"⚠️ 오류: '{member.name}' 님이 '{book_title}'을 빌린 적이 없습니다.")

# --- 임의의 데이터를 생성하는 함수 (도우미) ---
def create_mock_data(library):
    import random
    
    # 1. 책 데이터 만들기
    titles = [
        "해리포터", "반지의 제왕", "어린왕자", "데미안", 
        "코스모스", "사피엔스", "채식주의자", "소년이 온다",
        "부자 아빠 가난한 아빠", "트렌드 코리아 2024", "돈의 심리학",
        "미움받을 용기", "아주 작은 습관의 힘",
        "침묵의 봄", "이기적 유전자",
        "파이썬 코딩 도장", "점프 투 파이썬",
        "슬램덩크", "원피스"
    ]
    authors = [
        "J.K.롤링", "톨킨", "생텍쥐페리", "헤르만 헤세", 
        "칼 세이건", "유발 하라리", "한강", "한강",
        "로버트 기요사키", "김난도", "모건 하우절",
        "기시미 이치로", "제임스 클리어",
        "레이첼 카슨", "리처드 도킨스",
        "남재윤", "박응용",
        "이노우에 다케히코", "오다 에이치로"
    ]
    categories = [
        "판타지", "판타지", "문학", "문학",
        "과학", "인문", "문학", "문학",
        "경제/경영", "경제/경영", "경제/경영",
        "자기계발", "자기계발",
        "과학", "과학",
        "기술/IT", "기술/IT",
        "만화", "만화"
    ]
    
    print("\n📚 [자동 생성] 책을 서가에 꽂고 있습니다...")
    for _ in range(10): # 10권으로 늘려서 다양한 책이 나오도록!
        idx = random.randint(0, len(titles)-1)
        book = Book(titles[idx], authors[idx], categories[idx])
        library.add_book(book)

    # 2. 회원 데이터 만들기
    names = ["철수", "영희", "민수", "지은", "혜진", "준호"]
    print("\n👥 [자동 생성] 회원들을 모집하고 있습니다...")
    for _ in range(5): # 5명만 무작위로
        name = random.choice(names)
        member = Member(name)
        library.register_member(member)

# --- 여기부터는 실제로 잘 작동하는지 테스트하는 코드입니다 ---
if __name__ == "__main__":
    print("=== 🏫 도서관 시스템 시뮬레이션 시작 ===")

    # 1. 도서관 생성
    my_library = Library()

    # 2. 임의의 데이터 자동 생성 (여기가 추가되었습니다!)
    create_mock_data(my_library)

    # 3. 새로운 회원과 책 추가 (테스트를 위해 명확히 추가)
    print("\n--- 테스트를 위한 추가 데이터 ---")
    student = Member("김코딩")
    my_library.register_member(student)
    my_library.add_book(Book("해리포터", "J.K.롤링", "판타지")) # 이미 있을 수 있지만, 테스트를 위해 확실히 추가

    # 6. 대출 시도
    print("\n--- 대출 시나리오 ---")
    my_library.rent_book(student, "해리포터", due_date="2024-12-25")
    
    # Check if due date is set
    for book in student.borrowed_books:
        if book.title == "해리포터":
            print(f"--> 확인: '{book.title}'의 반납 예정일은 {book.due_date} 입니다.")

    # 7. 이미 빌린 책을 또 빌리려고 할 때
    my_library.rent_book(student, "해리포터", due_date="2024-12-30")

    # 8. 반납 시도
    print("\n--- 반납 시나리오 ---")
    my_library.return_book(student, "해리포터")
    
    print("\n=== 시뮬레이션 종료 ===")

