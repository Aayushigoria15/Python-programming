List1 = ['apple', 'banana', 'mango']
search_item = input("Enter the fruit name to search: ")

found = False

for fruit in List1:
    if fruit == search_item:
        print(search_item, "is found in the list.")
        found = True
        break

if not found:
    print(search_item, "is not found in the list.")
