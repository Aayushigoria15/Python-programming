try:
    file = open("example.txt", "r")
    print("File Content:", file.read())
except FileNotFoundError:
    print("Error: File not found!")
finally:
    try:
        file.close()
        print("File closed successfully (inside finally block).")
    except NameError:
        print("File was never opened, so no need to close.")
