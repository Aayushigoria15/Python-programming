import re

text = input("Enter a string: ")
word = input("Enter a word to match from the beginning: ")

result = re.match(word, text)

# Display result
if result:
    print(f" The string starts with the word '{word}'.")
else:
    print(f" The string does NOT start with the word '{word}'.")
