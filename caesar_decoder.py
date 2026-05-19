import os

def caesar_cipher_decode(target_text: str):
    """
    카이사르 암호를 1~25번째 자리수까지 복호화하여 출력하고,
    보너스 과제 조건에 맞춰 사전에 있는 단어가 발견되면 자동으로 탐색을 멈춥니다.
    """
    # 보너스 과제: 암호 해독을 자동으로 멈추기 위한 단어 사전
    dictionary = ["LOVE", "YOU", "SECRET", "MARS", "KEY"]
    decoded_results = {}

    print("\n==================================================")
    print("🤖 카이사르 암호 해독을 시작합니다.")
    print("==================================================")
    
    # 알파벳 개수만큼 반복 (1칸부터 25칸까지 밀어보기)
    for shift in range(1, 26):
        decoded_text = ""
        
        for char in target_text:
            if char.isupper():
                # 대문자 복호화 (A-Z 범위 유지)
                decoded_text += chr((ord(char) - 65 - shift) % 26 + 65)
            elif char.islower():
                # 소문자 복호화 (a-z 범위 유지)
                decoded_text += chr((ord(char) - 97 - shift) % 26 + 97)
            else:
                # 공백이나 특수문자는 그대로 유지
                decoded_text += char
        
        decoded_results[shift] = decoded_text
        print(f"[{shift:2d}번째 자리수 이동 결과] : {decoded_text}")

        # 보너스 과제: 사전에 있는 단어가 암호 속에서 발견될 경우 반복을 멈춤
        # 대소문자 구분을 없애기 위해 .upper()를 사용합니다.
     
        found_word = [word for word in dictionary if word in decoded_text.upper()]
        if found_word:
            print("==================================================")
            print(f"✨ [보너스 과제 성공] 사전에 등록된 단어 {found_word}를 발견했습니다!")
            print(f"💡 자동으로 반복을 중단합니다. 유력한 암호 힌트: [{shift}번]")
            print("==================================================")
            break  # 매칭되는 단어가 있으면 반복문(for)을 즉시 탈출합니다.

    return decoded_results


def main():
    # 1. 제약사항: 파일 읽기 예외처리
    try:
        if not os.path.exists("password.txt"):
            print("[오류] password.txt 파일이 존재하지 않습니다. 먼저 파일을 생성해 주세요.")
            return
            
        with open("password.txt", "r", encoding="utf-8") as f:
            encrypted_text = f.read().strip()
            
        if not encrypted_text:
            print("[경고] password.txt 파일이 비어 있습니다.")
            return
            
        print(f"🔒 읽어온 암호문: {encrypted_text}")
        
    except Exception as e:
        print(f"[파일 읽기 오류] 파일을 읽는 중 오류가 발생했습니다: {e}")
        return

    # 2. 복호화 함수 실행 (결과물은 딕셔너리 형태로 반환됨)
    decoded_table = caesar_cipher_decode(encrypted_text)

    # 3. 제약사항: 사용자 확인 및 결과 저장 예외처리
    try:
        user_choice = input("\n눈으로 식별된 올바른 해독 번호(자리수)를 입력하세요: ").strip()
        
        # 입력값 검증 (숫자인지, 해독한 결과 내에 있는 번호인지)
        if not user_choice.isdigit() or int(user_choice) not in decoded_table:
            print("[오류] 화면에 표시된 유효한 숫자를 입력해야 합니다. 프로그램을 종료합니다.")
            return
            
        selected_shift = int(user_choice)
        final_password = decoded_table[selected_shift]

        # result.txt로 최종 암호 저장
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(final_password)
            
        print("\n==================================================")
        print(f"💾 성공적으로 저장되었습니다! (파일명: result.txt)")
        print(f"🔓 최종 해독된 문장: {final_password}")
        print("==================================================")

    except Exception as e:
        print(f"[파일 저장 오류] 결과를 저장하는 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()