#Muhammad Usman    Project No 1  Password Strength Checker
COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "qwerty",
    "abc123", "password1", "111111", "letmein", "iloveyou",
}

#Symbols considered for password strength checking
SYMBOLS = set("!@#$%^&*()-_=+[]{}|;:,.<>?/~`")

def add_common_password(password: str) -> bool:
    normalized = password.strip().lower()
    if not normalized:
        return False
    if normalized in COMMON_PASSWORDS:
        return False

    COMMON_PASSWORDS.add(normalized)
    return True


def check_password_strength(password: str) -> dict:
    length_ok = len(password) >= 8
    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(char in SYMBOLS for char in password)
    is_leaked = password.lower() in COMMON_PASSWORDS

    score = sum([length_ok, has_lower, has_upper, has_digit, has_symbol])

    if is_leaked:
        strength = "Weak (found in common leaked password list)"
    elif not length_ok:
        strength = "Weak (too short)"
    elif score <= 2:
        strength = "Weak"
    elif score in (3, 4):
        strength = "Medium"
    else:
        strength = "Strong"

    return {
        "length_ok": length_ok,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "is_leaked": is_leaked,
        "score": score,
        "strength": strength,
    }


def print_report(password: str, result: dict) -> None:
    print(f"\nPassword: {password}")
    print("-" * 40)
    print(f"  Length >= 8 chars : {'✔' if result['length_ok'] else '✘'}")
    print(f"  Has lowercase     : {'✔' if result['has_lower'] else '✘'}")
    print(f"  Has uppercase     : {'✔' if result['has_upper'] else '✘'}")
    print(f"  Has digit         : {'✔' if result['has_digit'] else '✘'}")
    print(f"  Has symbol        : {'✔' if result['has_symbol'] else '✘'}")
    print(f"  In leaked list?   : {'YES ⚠' if result['is_leaked'] else 'No'}")
    print(f"  Score             : {result['score']}/5")
    print(f"  STRENGTH          : {result['strength']}")

def print_menu():
    print("\n=== Phantom Password Strength Checker ===")
    print("1. Enter a password to check")
    print("2. Add a password to the common/leaked list")
    print("3. View how many common passwords are stored")
    print("4. Quit")

# Main Program loop
def main():
    while True:
        print_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            password = input("Enter a password to check: ")
            result = check_password_strength(password)
            print_report(password, result)

        elif choice == "2":
            new_pwd = input("Enter a password to add to the common list: ")
            added = add_common_password(new_pwd)
            if added:
                print(f"'{new_pwd}' has been added to the common password list.")
            else:
                print("That password is already in the list or was empty.")

        elif choice == "3":
            print(f"There are {len(COMMON_PASSWORDS)} common passwords .")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option, please choose 1-4.")


if __name__ == "__main__":
    main()
