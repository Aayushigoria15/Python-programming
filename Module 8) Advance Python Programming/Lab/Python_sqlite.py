import sqlite3
connection = sqlite3.connect("student.db")
cursor = connection.cursor()
print("Database connected successfully!")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    marks REAL
)
""")
print("Table created successfully!")

cursor.execute("INSERT INTO students (name, age, marks) VALUES ('Aayushi', 21, 89.5)")
cursor.execute("INSERT INTO students (name, age, marks) VALUES ('Rahul', 20, 78.3)")
cursor.execute("INSERT INTO students (name, age, marks) VALUES ('Priya', 22, 92.0)")

connection.commit()
print("Data inserted successfully!")

cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

print("\nStudent Records:")
for row in rows:
    print(row)

connection.close()
print("\nDatabase connection closed.")
