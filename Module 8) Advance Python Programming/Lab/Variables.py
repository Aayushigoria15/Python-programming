message = "Hello from Global Scope!"

class Demo:
    def show(self):
        message = "Hello from Local Scope!"
        print("Local message:", message)  

obj = Demo()
obj.show()

print("Global message:", message)
