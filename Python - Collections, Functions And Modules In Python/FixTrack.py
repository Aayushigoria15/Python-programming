import datetime

orders = []
next_id = 1


def create_repair_order():
    global next_id

    print("\n--- Create New Repair Order ---")
    customer = input("Customer name: ")
    device = input("Device type: ")
    issue = input("Issue description: ")
    due_date = input("Due date (YYYY-MM-DD): ")

    order = {
        "id": next_id,
        "customer": customer,
        "device": device,
        "issue": issue,
        "due_date": due_date,
        "status": "Open",
        "parts": [],
        "repair_fee": 0.0,
        "total": 0,
        "parts_total": 0,
        "subtotal": 0,
        "discount": 0,
        "tax_amount": 0,
        "tax": 0
    }

    orders.append(order)
    print(f"Order #{order['id']} created for {customer}.\n")
    next_id += 1


def list_orders():
    print("\n--- All Orders ---")
    if len(orders) == 0:
        print("No orders yet.\n")
        return

    for o in orders:
        print("ID:", o["id"])
        print("Customer:", o["customer"])
        print("Device:", o["device"])
        print("Issue:", o["issue"])
        print("Due Date:", o["due_date"])
        print("Status:", o["status"])
        print("------------------------")


def complete_order():
    print("\n--- Complete an Order ---")
    order_id = input("Enter Order ID: ")

    found = None
    for o in orders:
        if str(o["id"]) == order_id:
            found = o
            break

    if found is None:
        print("Order not found.\n")
        return

    print("\nAdding parts (leave part name empty to stop):")
    while True:
        part = input("Part name: ")
        if part == "":
            break
        price = float(input("Price: "))
        qty = int(input("Quantity: "))
        found["parts"].append({"name": part, "price": price, "qty": qty})

    found["repair_fee"] = float(input("Repair fee: "))
    tax = float(input("Tax %: "))
    discount = float(input("Discount amount: "))


    parts_total = 0
    for p in found["parts"]:
        parts_total += p["price"] * p["qty"]

    subtotal = parts_total + found["repair_fee"]
    subtotal = subtotal - discount
    tax_amount = subtotal * tax / 100
    total = subtotal + tax_amount

    # Store billing details
    found["parts_total"] = parts_total
    found["subtotal"] = subtotal
    found["discount"] = discount
    found["tax_amount"] = tax_amount
    found["tax"] = tax
    found["total"] = total
    found["status"] = "Completed"

    print_invoice(found)


def print_invoice(order):
    print("\n========== FIXTRACK INVOICE ==========")
    print("Order ID:", order["id"])
    print("Customer:", order["customer"])
    print("Device:", order["device"])
    print("Issue:", order["issue"])
    print("--------------------------------------")

    print("Parts Used:")
    if len(order["parts"]) == 0:
        print("No parts replaced.")
    else:
        for p in order["parts"]:
            line_total = p["price"] * p["qty"]
            print(f"{p['name']} x {p['qty']} = {line_total}")

    print("--------------------------------------")
    print("Parts Total:", order["parts_total"])
    print("Repair Fee:", order["repair_fee"])
    print("Subtotal (after discount):", order["subtotal"])
    print("Discount Applied:", order["discount"])
    print(f"Tax ({order['tax']}%):", order["tax_amount"])
    print("--------------------------------------")
    print("FINAL TOTAL:", order["total"])
    print("======================================\n")


def save_to_file():
    f = open("orders.txt", "w")
    for o in orders:
        f.write(str(o) + "\n")
    f.close()
    print("Orders saved to orders.txt\n")


def menu():
    while True:
        print("===== FIXTRACK MENU =====")
        print("1. Create Order")
        print("2. List Orders")
        print("3. Complete Order")
        print("4. Save to File")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_repair_order()
        elif choice == "2":
            list_orders()
        elif choice == "3":
            complete_order()
        elif choice == "4":
            save_to_file()
        elif choice == "5":
            print("Exiting FixTrack...")
            break
        else:
            print("Invalid choice. Try again.\n")


menu()
