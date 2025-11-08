text = "python programming"

char_count = {}

for ch in text:
    if ch in char_count:
        char_count[ch] += 1
    else:
        char_count[ch] = 1

print("Character Frequency:")
for key, value in char_count.items():
    print(f"{key}: {value}")
