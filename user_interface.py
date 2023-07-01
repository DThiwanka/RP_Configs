# user_interface.py

def get_mode():
    print("Please select a mode:")
    print("1. Recommendation")
    print("2. CSV Modification")

    while True:
        mode = input("Enter the mode number (1 or 2): ")
        if mode in ["1", "2"]:
            if mode == "1":
                return "recommendation"
            else:
                return "csv_modification"
        else:
            print("Invalid mode number. Please try again.")

def get_user_inputs():
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (Male or Female): ")
    color = input("Enter your preferred cloth color: ")
    cloth_type = input("Enter the type of cloth you desire: ")

    user_inputs = {
        "age": age,
        "gender": gender,
        "color": color,
        "type": cloth_type
    }

    return user_inputs
