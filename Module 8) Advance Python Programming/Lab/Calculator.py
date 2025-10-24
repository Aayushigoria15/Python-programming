try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    operation = input("Enter operation (+, -, *, /): ")

    if operation == '1':
        print("Result:", num1 + num2)
    elif operation == '2':
        print("Result:", num1 - num2)
    elif operation == '3':
        print("Result:", num1 * num2)
    elif operation == '4':
        print("Result:", num1 / num2)  
    else:
        print("Invalid operation!")

except ValueError:
    print("Error: Invalid input! Please enter numeric values.")
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
