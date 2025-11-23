import datetime
import itertools

orders = []
_id_counter = itertools.count(1)

def input_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty — try again.")


def input_date(prompt):
    while True:
        s = input(prompt).strip()
        try:
           
            dt = datetime.datetime.strptime(s, "%Y-%m-%d").date()
            return dt.isoformat()
        except ValueError:
            print("Please enter a date in YYYY-MM-DD format (e.g. 2025-11-23).")


def input_positive_float(prompt):
    while True:
        s = input(prompt).strip()
        try:
            v = float(s)
            if v < 0:
                raise ValueError
            return v
        except ValueError:
            print("Please enter a non-negative number (e.g. 150 or 0).")


def input_yes_no(prompt):
    while True:
        s = input(prompt + " (y/n): ").strip().lower()
        if s in ("y", "yes"):
            return True
        if s in ("n", "no"):
            return False
        print("Please type y or n.")


def find_order_by_id(order_id):
    for o in orders:
        if o["id"] == order_id:
            return o
    return None


def print_divider():
    print("-" * 60)

# Core functionality

def create_repair_order():
    print_divider()
    print("Create new repair order")
    customer = input_nonempty("Customer name: ")
    device = input_nonempty("Device type (e.g. iPhone 12, HP Laptop): ")
    issue = input_nonempty("Issue description: ")
    due_date = input_date("Due date (YYYY-MM-DD): ")

    order = {
        "id": next(_id_counter),
        "customer": customer,
        "device": device,
        "issue": issue,
        "due_date": due_date,
        "status": "Open",
        "created_on": datetime.date.today().isoformat(),
        "parts": [], 
        "repair_fee": 0.0,
    }
    orders.append(order)
    print(f"Order #{order['id']} created for {customer}.")
    print_divider()


def list_orders(show_all=False):
    print_divider()
    title = "All repair orders" if show_all else "Open repair orders"
    print(title)
    if not orders:
        print("No orders found.")
        return
    for o in orders:
        if not show_all and o["status"] != "Open":
            continue
        print(f"ID: {o['id']} | Customer: {o['customer']} | Device: {o['device']}")
        print(f"   Issue: {o['issue']}")
        print(f"   Due: {o['due_date']} | Status: {o['status']} | Created: {o['created_on']}")
    print_divider()


def add_parts_to_order(order):
    print("Add parts replaced (enter part name, qty and unit price). Leave name empty to finish.")
    while True:
        name = input(" Part name (blank to finish): ").strip()
        if name == "":
            break
        qty = None
        while qty is None:
            q_str = input("  Quantity (integer): ").strip()
            if not q_str.isdigit():
                print("  Please enter an integer quantity (e.g. 1).")
            else:
                qty = int(q_str)
        price = input_positive_float("  Unit price (e.g. 45.50): ")
        order["parts"].append({"name": name, "qty": qty, "unit_price": price})
        print(f"  Added {qty} x {name} @ {price:.2f}")
    if not order["parts"]:
        print("No parts added.")


def complete_order_and_generate_invoice():
    print_divider()
    if not any(o["status"] == "Open" for o in orders):
        print("There are no open orders to complete.")
        return

    while True:
        try:
            oid = int(input("Enter order ID to complete: ").strip())
            order = find_order_by_id(oid)
            if order is None:
                print("Order ID not found — try again.")
                continue
            break
        except ValueError:
            print("Please type a numeric order ID (e.g. 3).")

    if order["status"] != "Open":
        print(f"Order #{order['id']} is already {order['status']}.")
        return

    print(f"Completing Order #{order['id']} for {order['customer']} ({order['device']})")
    add_parts_to_order(order)

    repair_fee = input_positive_float("Enter repair service fee (labour) amount: ")
    order["repair_fee"] = repair_fee

    tax_pct = input_positive_float("Enter tax percentage to apply (e.g. 18 for 18%): ")

    discount_apply = input_yes_no("Apply a discount on the subtotal?")
    discount_amt = 0.0
    if discount_apply:
        discount_amt = input_positive_float("Enter discount amount (absolute value, not percent): ")

    parts_total = sum(p["qty"] * p["unit_price"] for p in order["parts"])
    subtotal = parts_total + repair_fee
    taxable_amount = max(0.0, subtotal - discount_amt)
    tax_value = taxable_amount * (tax_pct / 100.0)
    total = taxable_amount + tax_value

    order["status"] = "Completed"
    order["completed_on"] = datetime.date.today().isoformat()

    print_invoice(order, parts_total, subtotal, discount_amt, tax_pct, tax_value, total)


def format_money(x):
    return f"{x:,.2f}"


def print_invoice(order, parts_total, subtotal, discount_amt, tax_pct, tax_value, total):
    print_divider()
    print("FIXTRACK - INVOICE")
    print_divider()
    print(f"Invoice for Order #{order['id']} (Completed: {order.get('completed_on', 'N/A')})")
    print(f"Customer : {order['customer']}")
    print(f"Device   : {order['device']}")
    print(f"Issue    : {order['issue']}")
    print_divider()
    print("Parts Replaced:")
    if order["parts"]:
        print("{:<4} {:<25} {:>6} {:>12} {:>12}".format("No.", "Part", "Qty", "Unit Price", "Line Total"))
        for i, p in enumerate(order["parts"], 1):
            line_total = p["qty"] * p["unit_price"]
            print("{:<4} {:<25} {:>6} {:>12} {:>12}".format(
                i, p["name"][:25], p["qty"], format_money(p["unit_price"]), format_money(line_total)
            ))
    else:
        print("  (No parts replaced)")
    print_divider()
    print(f"Parts total: {format_money(parts_total)}")
    print(f"Repair fee : {format_money(order['repair_fee'])}")
    print(f"Subtotal   : {format_money(subtotal)}")
    if discount_amt > 0:
        print(f"Discount   : -{format_money(discount_amt)}")
        taxable_display = subtotal - discount_amt
        print(f"Taxable amt: {format_money(taxable_display)}")
    else:
        taxable_display = subtotal
    print(f"Tax ({tax_pct:.2f}%): {format_money(tax_value)}")
    print_divider()
    print(f"TOTAL DUE  : {format_money(total)}")
    print_divider()
    print("Thank you for using FixTrack!")
    print_divider()


def show_menu():
    print("\nFixTrack Main Menu")
    print("1. Create new repair order")
    print("2. List open orders")
    print("3. List all orders")
    print("4. Complete order and generate invoice")
    print("5. Exit")


def main_loop():
    print("Welcome to FixTrack — TechFix Solutions (console)")
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            create_repair_order()
        elif choice == "2":
            list_orders(show_all=False)
        elif choice == "3":
            list_orders(show_all=True)
        elif choice == "4":
            complete_order_and_generate_invoice()
        elif choice == "5":
            if input_yes_no("Exit FixTrack now?"):
                print("Goodbye — closing FixTrack.")
                break
        else:
            print("Invalid selection. Please enter a number 1-5.")


if __name__ == "__main__":
    main_loop()
