
import secrets
import string


def show_banner():
    print("\n" + "=" * 50)
    print("          PASSWORD GENERATOR PRO")
    print("=" * 50)
    print("Generate secure and customized passwords!")
    print("-" * 50)


def get_password_length():
    while True:
        try:
            length = int(input("Enter password length (4-128): "))

            if 4 <= length <= 128:
                return length

            print("Please enter a length between 4 and 128.")

        except ValueError:
            print("Invalid input! Please enter a number.")


def get_password_count():
    while True:
        try:
            count = int(input("How many passwords do you want? "))

            if 1 <= count <= 20:
                return count

            print("Please choose between 1 and 20.")

        except ValueError:
            print("Invalid input! Enter a valid number.")


def generate_password(length, use_upper, use_lower,
                      use_digits, use_symbols):

    character_groups = []

    if use_upper:
        character_groups.append(string.ascii_uppercase)

    if use_lower:
        character_groups.append(string.ascii_lowercase)

    if use_digits:
        character_groups.append(string.digits)

    if use_symbols:
        character_groups.append(string.punctuation)

    if not character_groups:
        raise ValueError("Select at least one character type.")

    if length < len(character_groups):
        raise ValueError("Password length is too short.")

    all_characters = "".join(character_groups)

    password = [
        secrets.choice(group)
        for group in character_groups
    ]

    for _ in range(length - len(password)):
        password.append(secrets.choice(all_characters))

    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def check_strength(length, types):
    if length >= 16 and types >= 3:
        return "Very Strong"

    elif length >= 12 and types >= 3:
        return "Strong"

    elif length >= 8 and types >= 2:
        return "Moderate"

    else:
        return "Basic"


def main():

    while True:

        show_banner()

        length = get_password_length()
        count = get_password_count()

        print("\n--- Customize Your Password ---")

        upper = input("Include uppercase letters? (y/n): ").lower()
        lower = input("Include lowercase letters? (y/n): ").lower()
        digits = input("Include numbers? (y/n): ").lower()
        symbols = input("Include special characters? (y/n): ").lower()

        options = [upper, lower, digits, symbols]

        if any(option not in ("y", "n") for option in options):
            print("\nInvalid choice! Please enter only y or n.")
            continue

        selected_types = sum(option == "y" for option in options)

        if selected_types == 0:
            print("\nPlease select at least one character type.")
            continue

        if length < selected_types:
            print("\nPassword length is too short for selected options.")
            continue

        print("\n" + "=" * 50)
        print("          GENERATED PASSWORDS")
        print("=" * 50)

        for i in range(count):

            password = generate_password(
                length,
                upper == "y",
                lower == "y",
                digits == "y",
                symbols == "y"
            )

            strength = check_strength(length, selected_types)

            print(f"\nPassword {i + 1}: {password}")
            print(f"Strength: {strength}")

        print("\n" + "-" * 50)

        again = input("Generate more passwords? (y/n): ").lower()

        if again != "y":
            print("\nThank you for using Password Generator Pro!")
            print("Stay safe and keep your passwords private.")
            break


if __name__ == "__main__":
    main()
