class AgeTooLowError(Exception):
    def __init__(self, message):
        self.message = message

try:
    age = int(input("Enter your age: "))
    if age < 18:
        raise AgeTooLowError("Age is too low to vote!")
    else:
        print("You are eligible to vote.")
except AgeTooLowError as e:
    print("Custom Exception:", e.message)
except ValueError:
    print("Invalid input! Please enter an integer.")
