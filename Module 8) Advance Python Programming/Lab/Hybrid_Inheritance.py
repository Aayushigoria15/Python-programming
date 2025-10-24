class GrandParent:
    def show_gp(self):
        print("This is GrandParent.")

class Parent1(GrandParent):
    def show_p1(self):
        print("This is Parent1.")

class Parent2:
    def show_p2(self):
        print("This is Parent2.")

class Child(Parent1, Parent2):
    def show_child(self):
        print("This is Child class.")

obj = Child()
obj.show_gp()    
obj.show_p1() 
obj.show_p2()  
obj.show_child() 
