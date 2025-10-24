class Parent:
    def __init__(self):
        print("Parent class constructor.")

class Child(Parent):
    def __init__(self):
        super().__init__() 
        print("Child class constructor.")

obj = Child()
