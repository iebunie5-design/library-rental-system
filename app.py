import streamlit as st
import random
from datetime import date, timedelta
from library_system import Book, Member, Library, create_mock_data

# --- 페이지 설정 ---
st.set_page_config(page_title="도서관 대여 시스템", page_icon="📚", layout="wide")

# --- 세션 상태 초기화 (새로고침해도 데이터가 날아가지 않게!) ---
if 'library' not in st.session_state:
    # 1. 도서관 객체 생성
    lib = Library()
    # 2. 임의의 데이터 채워넣기
    create_mock_data(lib)
    # 3. 세션에 저장
    st.session_state.library = lib

# 편하게 쓰기 위해 변수에 할당
library = st.session_state.library

# --- UI 제목 ---
st.title("📚 우리동네 도서관 대여 시스템")
st.markdown("---")

# --- 탭 메뉴 만들기 ---
tab1, tab2, tab3, tab4 = st.tabs(["📖 도서 목록", "👥 회원 목록", "🔄 대여/반납", "🛠️ 도서 관리"])

# [탭 1] 도서 목록 보여주기
with tab1:
    st.header("현재 소장 중인 도서")
    
    # [NEW] 카테고리 필터
    all_categories = ["전체"] + sorted(list(set([b.category for b in library.books])))
    selected_category = st.selectbox("카테고리별 보기", all_categories)
    
    # 책 데이터를 테이블 형태로 보여주기 위해 리스트 생성
    book_data = []
    for book in library.books:
        # 필터링 로직
        if selected_category != "전체" and book.category != selected_category:
            continue
            
        status = "✅ 대출 가능" if book.is_available else "❌ 대출중"
        book_data.append({
            "카테고리": book.category,
            "제목": book.title, 
            "저자": book.author, 
            "상태": status
        })
    
    st.table(book_data)

# [탭 2] 회원 목록 보여주기
with tab2:
    st.header("등록된 회원")
    
    # 회원 데이터를 텍스트로 깔끔하게 보여주기
    if not library.members:
        st.info("등록된 회원이 없습니다.")
    else:
        for member in library.members:
            with st.expander(f"👤 {member.name} 님"):
                if not member.borrowed_books:
                    st.write("대출 중인 책이 없습니다.")
                else:
                    st.write("📚 대출 목록:")
                    for book in member.borrowed_books:
                        st.write(f"- {book.title} ({book.author})")

# [탭 3] 대여 및 반납 기능
with tab3:
    st.header("대여 및 반납 데스크")
    
    col1, col2 = st.columns(2)
    
    # 1. 대여하기 섹션
    with col1:
        st.subheader("대여하기")
        # 회원 선택
        member_names = [m.name for m in library.members]
        selected_member_rent = st.selectbox("회원 선택", member_names, key="rent_member")
        
        # 대출 가능한 책만 필터링
        available_books = [b.title for b in library.books if b.is_available]
        selected_book_rent = st.selectbox("책 선택", available_books, key="rent_book")
        
        # [NEW] 대출 일정 선택 기능 (기본값: 오늘부터 3일 뒤)
        today = date.today()
        default_due_date = today + timedelta(days=3)
        rent_date = st.date_input("대여 일정 선택", value=default_due_date, key="rent_date")

        if st.button("대여 실행", key="btn_rent"):
            if not selected_book_rent:
                st.error("대출 가능한 책이 없습니다.")
            else:
                # 실제 객체 찾기
                member_obj = next(m for m in library.members if m.name == selected_member_rent)
                
                # 대출 실행 (날짜도 같이 전달)
                library.rent_book(member_obj, selected_book_rent, rent_date)
                
                # [NEW] 성공 메시지
                st.success(f"🎉 '{member_obj.name}' 회원님, '{selected_book_rent}' 대여가 완료되었습니다! (반납예정일: {rent_date})")
                
                # [NEW] 3일 뒤 시뮬레이션 메시지 (미리 보기)
                if rent_date <= today:
                     st.warning(f"⚠️ [알림 시뮬레이션] '{member_obj.name}'님, 반납일이 지났습니다! 책을 반납해주세요.")
                
                st.rerun() # 화면 새로고침

    with col2:
        st.subheader("반납하기")
        selected_member_return = st.selectbox("회원 선택 (반납)", member_names, key="return_member")
        
        # 해당 회원이 빌린 책 목록 가져오기
        member_obj = next(m for m in library.members if m.name == selected_member_return)
        borrowed_titles = [b.title for b in member_obj.borrowed_books]
        
        selected_book_return = st.selectbox("반납할 책 선택", borrowed_titles, key="return_book")
        
        if st.button("반납 실행", key="btn_return"):
            if not selected_book_return:
                st.error("반납할 책이 없습니다.")
            else:
                library.return_book(member_obj, selected_book_return)
                st.success(f"'{selected_book_return}' 반납 완료!")
                st.rerun() # 화면 새로고침

# [탭 4] 도서 관리 (신간 등록 및 폐기)
with tab4:
    st.header("도서 관리 시스템")
    
    col_new, col_del = st.columns(2)
    
    # 1. 신간 도서 등록
    with col_new:
        st.subheader("✨ 신간 도서 등록")
        category_options = ["문학", "판타지", "인문", "과학", "경제/경영", "자기계발", "역사", "기술/IT", "만화", "기타"]
        new_category = st.selectbox("카테고리", category_options, key="new_category")
        new_title = st.text_input("책 제목", key="new_title")
        new_author = st.text_input("저자", key="new_author")
        
        if st.button("도서 등록", key="btn_add"):
            if new_title and new_author:
                new_book = Book(new_title, new_author, new_category)
                library.add_book(new_book)
                st.success(f"'{new_category}' 분야의 '{new_title}' 입고 완료! 🎉")
                st.rerun()
            else:
                st.warning("제목과 저자를 모두 입력해주세요.")

    # 2. 도서 폐기
    with col_del:
        st.subheader("🗑️ 도서 폐기")
        # 폐기할 책 선택 (대출 중이 아닌 책만 폐기 가능하도록 하면 좋겠지만, 일단 전체 목록 보여줌)
        all_books = [b.title for b in library.books]
        book_to_delete = st.selectbox("폐기할 책 선택", all_books, key="del_book")
        
        if st.button("폐기 실행", key="btn_del"):
            if book_to_delete:
                 library.remove_book(book_to_delete)
                 st.error(f"'{book_to_delete}' 폐기 처리되었습니다.")
                 st.rerun()
            else:
                st.warning("폐기할 책이 없습니다.")

