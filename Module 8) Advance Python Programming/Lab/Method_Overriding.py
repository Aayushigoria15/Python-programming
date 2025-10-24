class Parent:
    def show(self):
        print("This is the Parent class method.")

class Child(Parent):
    def show(self):  
        print("This is the Child class method (Overridden).")

parent_obj = Parent()
child_obj = Child()

parent_obj.show() 
child_obj.show()  
