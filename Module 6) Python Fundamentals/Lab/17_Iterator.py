class NumberIterator:
    def __init__(self, numbers):
        self.numbers = numbers
        self.position = 0  

    def __iter__(self):
        return self 

    def __next__(self):
        if self.position < len(self.numbers):
            value = self.numbers[self.position]
            self.position += 1
            return value
        else:
            raise StopIteration  

nums = [1, 2, 3, 4, 5]

for n in NumberIterator(nums):
    print(n)
