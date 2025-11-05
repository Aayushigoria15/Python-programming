text = "  hello world  "

print("Original string:", text)
print("Uppercase:", text.upper())           # convert to uppercase
print("Lowercase:", text.lower())           # convert to lowercase
print("Title case:", text.title())          # capitalize each word
print("Stripped:", text.strip())            # remove spaces
print("Replace:", text.replace("world", "Python"))  # replace word
print("Starts with 'h':", text.startswith("h"))     # check start
print("Ends with 'd':", text.endswith("d"))         # check end
print("Count of 'l':", text.count("l"))             # count letters
print("Length of string:", len(text))               # find length
