import sqlite3

class Employee:
    def __init__(self, name, department, performance_rating, salary):
        self.name = name
        self.department = department
        self.performance_rating = performance_rating
        self.salary = salary
        self.bonus = 0

    def calculate_bonus(self):
        # Bonus calculation logic based on performance_rating
        bonus_percentage = 0.05 * self.performance_rating
        self.bonus = self.salary * bonus_percentage

    def calculate_final_salary(self, hike_percentage):
        # Calculate final salary with bonus and user-provided hike
        return self.salary + self.bonus + (self.salary * hike_percentage)

def connect_to_database():
    # Connect to SQLite database
    connection = sqlite3.connect('appraisal_system.db')
    cursor = connection.cursor()

    # Create Employee table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            performance_rating REAL,
            salary REAL,
            bonus REAL DEFAULT 0
        )
    ''')
    connection.commit()

    return connection, cursor

def insert_employee_to_database(cursor, employee):
    cursor.execute('''
        INSERT INTO employees (name, department, performance_rating, salary, bonus)
        VALUES (?, ?, ?, ?, ?)
    ''', (employee.name, employee.department, employee.performance_rating, employee.salary, employee.bonus))

def get_employee_name():
    # Function to get a valid employee name
    while True:
        name = input("Enter employee name: ")
        if name.isalpha():
            return name
        else:
            print("Invalid input. Name should only contain alphabets. Please try again.")

def get_employee_performance_rating():
    # Function to get a valid performance rating from the user
    while True:
        try:
            rating = float(input("Enter the performance rating (0.0 to 5.0): "))
            if 0.0 <= rating <= 5.0:
                return rating
            else:
                print("Rating should be between 0.0 and 5.0. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_employee_salary():
    # Function to get a valid employee salary
    while True:
        try:
            salary = float(input("Enter employee's current salary: "))
            if salary > 0:
                return salary
            else:
                print("Salary should be greater than 0. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_hike_percentage():
    # Function to get a valid hike percentage
    while True:
        try:
            hike = float(input("Enter the hike percentage for this employee (0 to 100): "))
            if 0 <= hike <= 100:
                return hike / 100  # Convert percentage to decimal
            else:
                print("Hike should be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def main():
    # Connect to SQLite database
    connection, cursor = connect_to_database()

    # Create a few departments
    departments = ["IT", "HR", "Sales", "Finance", "Marketing"]

    for department in departments:
        print(f"\n----- {department} Department -----")
        num_employees = 0

        while True:
            try:
                num_employees = int(input("Enter the number of employees: "))
                if num_employees > 0:
                    break
                else:
                    print("Number of employees should be greater than 0. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        for _ in range(num_employees):
            employee_name = get_employee_name()
            performance_rating = get_employee_performance_rating()
            salary = get_employee_salary()
            hike_percentage = get_hike_percentage()

            # Create an Employee object
            employee = Employee(employee_name, department, performance_rating, salary)

            # Calculate bonus and final salary with user-provided hike
            employee.calculate_bonus()
            final_salary = employee.calculate_final_salary(hike_percentage)

            # Insert employee into the database
            insert_employee_to_database(cursor, employee)

            # Display employee details
            print(f"{employee.name}'s Final Salary: ${final_salary:.2f}")

    # Commit changes and close the database connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
