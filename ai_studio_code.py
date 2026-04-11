import json
import os

# 데이터 파일 로드 함수
def load_data(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

# 데이터 저장 함수
def save_data(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class QuizProgram:
    def __init__(self):
        self.users = load_data('users.json')
        self.problems = load_data('problems.json')
        self.current_user = None

    # 회원가입
    def register(self):
        print("\n--- 회원가입 ---")
        user_id = input("아이디: ")
        if any(u['id'] == user_id for u in self.users):
            print("이미 존재하는 아이디입니다.")
            return

        pw = input("비밀번호: ")
        student_id = input("학번: ")
        name = input("이름: ")
        birth = input("생년월일(YYMMDD): ")

        new_user = {
            "id": user_id, "pw": pw, "student_id": student_id,
            "name": name, "birth": birth, "score": 0
        }
        self.users.append(new_user)
        save_data('users.json', self.users)
        print("회원가입 완료!")

    # 로그인
    def login(self):
        print("\n--- 로그인 ---")
        user_id = input("아이디: ")
        pw = input("비밀번호: ")

        for user in self.users:
            if user['id'] == user_id and user['pw'] == pw:
                self.current_user = user
                print(f"{user['name']}님 환영합니다!")
                return True
        print("아이디 또는 비밀번호가 틀렸습니다.")
        return False

    # 문제 풀기
    def solve_problems(self):
        if not self.current_user: return
        
        print("\n--- 문제 풀이 시작 ---")
        score = 0
        for p in self.problems:
            print(f"\n[문제 {p['id']}] {p['question']}")
            if p['view']: print(f"참고: {p['view']}")
            if p['image_file']: print(f"📎 이미지 참조: {p['image_file']}")
            
            for i, option in enumerate(p['options'], 1):
                print(f"{i}. {option}")
            
            try:
                choice = int(input("정답 번호 선택: "))
                if choice == p['answer']:
                    print("정답입니다!")
                    score += 10
                else:
                    print(f"틀렸습니다. 정답은 {p['answer']}번입니다.")
            except ValueError:
                print("숫자만 입력해주세요.")

        # 점수 업데이트
        for user in self.users:
            if user['id'] == self.current_user['id']:
                user['score'] = max(user['score'], score) # 최고점수 기록
        save_data('users.json', self.users)
        print(f"\n최종 점수: {score}점")

    # 랭킹 보기
    def show_rank(self):
        print("\n--- 명예의 전당 (랭킹) ---")
        sorted_users = sorted(self.users, key=lambda x: x['score'], reverse=True)
        for i, user in enumerate(sorted_users, 1):
            print(f"{i}위: {user['name']}({user['id']}) - {user['score']}점")

    def main_menu(self):
        while True:
            print("\n1. 로그인 / 2. 회원가입 / 3. 종료")
            choice = input("선택: ")
            if choice == '1':
                if self.login():
                    while True:
                        print("\n1. 문제 풀기 / 2. 랭킹 확인 / 3. 로그아웃")
                        sub_choice = input("선택: ")
                        if sub_choice == '1': self.solve_problems()
                        elif sub_choice == '2': self.show_rank()
                        elif sub_choice == '3': break
            elif choice == '2':
                self.register()
            elif choice == '3':
                break

if __name__ == "__main__":
    program = QuizProgram()
    program.main_menu()