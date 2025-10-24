try:
    file = open("example.txt", "r")
    content = file.read()
    num = int(input("Enter a number to divide 100: "))
    result = 100 / num
    print("Result:", result)

except FileNotFoundError:
    print("Error: The file you are trying to open does not exist.")
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")
except ValueError:
    print("Error: Invalid input, please enter an integer.")
