class Parent:
    def display(self):
        print("This is the Parent class.")

class Child(Parent):
    def show(self):
        print("This is the Child class.")

obj = Child()
obj.display()
obj.show()
