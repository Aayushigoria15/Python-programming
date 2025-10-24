class GrandParent:
    def property(self):
        print("Property from GrandParent.")

class Parent(GrandParent):
    def money(self):
        print("Money from Parent.")

class Child(Parent):
    def own(self):
        print("Child's own property.")

obj = Child()
obj.property()
obj.money()
obj.own()
