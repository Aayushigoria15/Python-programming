class Father:
    def skills(self):
        print("Father: Knows driving.")

class Mother:
    def talents(self):
        print("Mother: Good at cooking.")

class Child(Father, Mother):
    def own(self):
        print("Child: Good at programming.")

obj = Child()
obj.skills()
obj.talents()
obj.own()
