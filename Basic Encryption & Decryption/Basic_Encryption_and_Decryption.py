def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            result += char
    return result


def decrypt(text, shift):
    return encrypt(text, -shift)


def get_shift_key():
    while True:
        try:
            shift = int(input("Enter the shift key (1-25): "))
            if 1 <= shift <= 25:
                return shift
            print("Shift key must be between 1 and 25.")
        except ValueError:
            print("Please enter a valid number.")


def get_choice():
    while True:
        print("\n1. Encrypt")
        print("2. Decrypt")
        choice = input("Choose an option (1/2): ").strip()
        if choice in ("1", "2"):
            return choice
        print("Please enter 1 or 2.")


def main():
    print("=== Phantom Cipher Tool ===")
    choice = get_choice()
    shift = get_shift_key()

    if choice == "1":
        text = input("Enter the text you want to encrypt: ")
        encrypted_text = encrypt(text, shift)
        print("\nOriginal Text  :", text)
        print("Encrypted Text :", encrypted_text)
    else:
        text = input("Enter the text you want to decrypt: ")
        decrypted_text = decrypt(text, shift)
        print("\nEncrypted Text :", text)
        print("Decrypted Text :", decrypted_text)


if __name__ == "__main__":
    main()
