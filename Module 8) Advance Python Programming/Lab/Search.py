import re

text = input("Enter a string: ")
word = input("Enter a word to search: ")

result = re.search(word, text)

if result:
    print(f" The word '{word}' was found in the string at position {result.start()}.")
else:
    print(f" The word '{word}' was NOT found in the string.")
