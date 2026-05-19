import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# ==========================================
# 1. 카이사르 암호 (고전 암호)
# ==========================================
def caesar_cipher_decode(target_text: str):
    dictionary = ["LOVE", "YOU", "SECRET", "MARS", "KEY"]
    decoded_results = {}

    print("\n[카이사르 암호 해독 진행 중...]")
    for shift in range(1, 26):
        decoded_text = ""
        for char in target_text:
            if char.isupper():
                decoded_text += chr((ord(char) - 65 - shift) % 26 + 65)
            elif char.islower():
                decoded_text += chr((ord(char) - 97 - shift) % 26 + 97)
            else:
                decoded_text += char
        
        decoded_results[shift] = decoded_text
        print(f"[{shift:2d}번째 자리수 이동] : {decoded_text}")

        found_word = [word for word in dictionary if word in decoded_text.upper()]
        if found_word:
            print("\n==================================================")
            print(f"✨ [보너스 과제 성공] 사전에 등록된 단어 {found_word}를 발견했습니다!")
            print(f"💡 자동으로 반복을 중단합니다. 유력한 암호 힌트: [{shift}번]")
            print("==================================================")
            break 

    return decoded_results

def run_caesar_cipher():
    print("\n--- [고전 암호: 카이사르 암호 해독] ---")
    try:
        if not os.path.exists("password.txt"):
            print("[오류] password.txt 파일이 없습니다. 먼저 파일을 생성해 주세요.")
            return
            
        with open("password.txt", "r", encoding="utf-8") as f:
            encrypted_text = f.read().strip()
            
        if not encrypted_text:
            print("[경고] password.txt 파일이 비어 있습니다.")
            return
            
        print(f"🔒 읽어온 암호문: {encrypted_text}")
        
    except Exception as e:
        print(f"[파일 읽기 오류] {e}")
        return

    decoded_table = caesar_cipher_decode(encrypted_text)

    try:
        user_choice = input("\n눈으로 식별된 올바른 해독 번호(자리수)를 입력하세요: ").strip()
        
        if not user_choice.isdigit() or int(user_choice) not in decoded_table:
            print("[오류] 화면에 표시된 유효한 숫자를 입력해야 합니다.")
            return
            
        selected_shift = int(user_choice)
        final_password = decoded_table[selected_shift]

        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(final_password)
            
        print(f"\n💾 성공적으로 저장되었습니다! (파일명: result.txt)")
        print(f"🔓 최종 해독된 문장: {final_password}")

    except Exception as e:
        print(f"[파일 저장 오류] {e}")


# ==========================================
# 2. 대칭키 암호 (AES / Fernet)
# ==========================================
def run_symmetric_cipher():
    print("\n--- [대칭키(Symmetric) 암호화: AES(Fernet)] ---")
    message = input("암호화할 문장을 입력하세요: ")
    
    # 1. 키 생성
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    print(f"\n🔑 발급된 대칭키: {key.decode('utf-8')}")

    # 2. 암호화
    encoded_message = message.encode('utf-8')
    encrypted_text = cipher_suite.encrypt(encoded_message)
    print(f"🔒 암호문: {encrypted_text}")

    # 3. 복호화 
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode('utf-8')
    print(f"🔓 복호화된 평문: {decrypted_text}")


# ==========================================
# 3. 비대칭키 암호 (RSA)
# ==========================================
def run_asymmetric_cipher():
    print("\n--- [비대칭키(Asymmetric) 암호화: RSA] ---")
    message = input("암호화할 문장을 입력하세요: ")
    
    # 1. 키 쌍 생성
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    print("\n🔑 개인키(Private Key)와 공개키(Public Key)가 생성되었습니다.")

    # 2. 암호화 (공개키 사용)
    encoded_message = message.encode('utf-8')
    encrypted_text = public_key.encrypt(
        encoded_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"🔒 암호문 (앞부분만 출력): {encrypted_text[:50]}...")

    # 3. 복호화 (개인키 사용)
    decrypted_text = private_key.decrypt(
        encrypted_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode('utf-8')
    print(f"🔓 복호화된 평문: {decrypted_text}")


# ==========================================
# 메인 메뉴
# ==========================================
def main():
    while True:
        print("\n==================================================")
        print("🛡️  통합 암호화/복호화 프로그램 🛡️")
        print("==================================================")
        print("1. 고전 암호: 카이사르 암호 해독 (password.txt 필요)")
        print("2. 현대 암호: 대칭키 암호화 시뮬레이션 (AES)")
        print("3. 현대 암호: 비대칭키 암호화 시뮬레이션 (RSA)")
        print("0. 프로그램 종료")
        print("==================================================")
        
        choice = input("원하는 메뉴의 번호를 입력하세요: ").strip()
        
        if choice == '1':
            run_caesar_cipher()
        elif choice == '2':
            run_symmetric_cipher()
        elif choice == '3':
            run_asymmetric_cipher()
        elif choice == '0':
            print("\n프로그램을 종료합니다. 안녕히 가세요!")
            break
        else:
            print("\n[오류] 0~3 사이의 숫자를 입력해 주세요.")

if __name__ == "__main__":
    main()
