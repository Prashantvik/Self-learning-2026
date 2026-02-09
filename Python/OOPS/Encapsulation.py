"""Encapsulation

Encapsulation allows you to bundle data and methods that operate
on that data within a single unit, typically a class. It helps to protect the
internal state of an object from unauthorized access and modification,
ensuring that the object's data is accessed and modified only through
well-defined interfaces.

Access modifiers: public, private, protected in C++

In python, there's no special keywords to define the protectiveness of the
attributes and methods, but we can use naming conventions to indicate their
intended usage.

Public attributes and methods: These can be accessed from anywhere. They are
defined without any special prefix.

Private attributes and methods: These are intended to be accessed only
within the class. They are defined with a double underscore prefix
(e.g., __attribute).

Protected attributes and methods: These are intended to be accessed within
the class and its subclasses. They are defined with a single underscore
prefix (e.g., _attribute).
"""


# Example 1: Employee class WITHOUT encapsulation (poor practice)
class Employee:
    """Basic Employee class without encapsulation."""

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        """Get employee details."""
        return f"Name: {self.name}, Salary: ${self.salary}"


# Creating an employee instance
emp1 = Employee("John Doe", 50000)
print(emp1.get_details())

# Problem: We can directly access and modify attributes from outside
# This violates encapsulation principles and can lead to data integrity issues
emp1.name = "Hacker"        # Direct access - not secure
emp1.salary = -999999       # Invalid salary - no validation
print(f"After unauthorized changes: {emp1.get_details()}")


# Example 2: Employee class WITH encapsulation (good practice)
class EncapsulatedEmployee:
    """Employee class with proper encapsulation using private attributes."""

    def __init__(self, name, salary):
        self.__name = name          # Private attribute
        self.__salary = salary      # Private attribute
        self.__employee_id = None   # Private attribute

    # Public methods to access private data (getters)
    def get_name(self):
        """Get employee name."""
        return self.__name

    def get_salary(self):
        """Get employee salary."""
        return self.__salary

    def get_employee_id(self):
        """Get employee ID."""
        return self.__employee_id

    # Public methods to modify private data (setters) with validation
    def set_name(self, name):
        """Set employee name with validation."""
        if isinstance(name, str) and len(name) > 0:
            self.__name = name
        else:
            print("Invalid name! Name must be a non-empty string.")

    def set_salary(self, salary):
        """Set employee salary with validation."""
        if isinstance(salary, (int, float)) and salary >= 0:
            self.__salary = salary
        else:
            print("Invalid salary! Salary must be a positive number.")

    def set_employee_id(self, emp_id):
        """Set employee ID with validation."""
        if isinstance(emp_id, str) and emp_id.startswith("EMP"):
            self.__employee_id = emp_id
        else:
            print("Invalid employee ID! Must start with 'EMP'.")

    def get_details(self):
        """Get employee details."""
        return f"Name: {self.__name}, Salary: ${self.__salary}, ID: {self.__employee_id}"

    # Private method - can only be accessed within the class
    def __calculate_bonus(self):
        """Calculate employee bonus (private method)."""
        return self.__salary * 0.1

    def get_annual_package(self):
        """Get annual package including bonus."""
        bonus = self.__calculate_bonus()
        return self.__salary + bonus


# Creating an encapsulated employee instance
emp2 = EncapsulatedEmployee("Jane Smith", 60000)
emp2.set_employee_id("EMP001")
print(emp2.get_details())

# Now we cannot directly access private attributes
# These will raise AttributeError or create new attributes (not accessing the private ones)
try:
    print(emp2.__name)  # This won't work
except AttributeError:
    print("Cannot access private attribute __name directly")

# We must use public methods to interact with the object
emp2.set_name("Jane Doe")       # Valid change
emp2.set_salary(-5000)          # Invalid - will be rejected
emp2.set_salary(65000)          # Valid change
print(f"Updated details: {emp2.get_details()}")
print(f"Annual package: ${emp2.get_annual_package()}")

# Trying to access private method directly won't work
# emp2.__calculate_bonus()  # This would raise AttributeError


# Example 3: Protected attributes (single underscore)
class BaseEmployee:
    """Base employee class with protected attributes."""

    def __init__(self, name, department):
        self.name = name                    # Public
        self._department = department       # Protected (convention)
        self.__social_security = None       # Private

    def _internal_method(self):
        """Protected method - intended for subclasses."""
        return f"Internal processing for {self.name}"


class Manager(BaseEmployee):
    """Manager class that inherits from BaseEmployee."""

    def __init__(self, name, department, team_size):
        super().__init__(name, department)
        self.team_size = team_size

    def get_manager_info(self):
        """Get manager information."""
        # Can access protected attributes from parent class
        internal_info = self._internal_method()  # Accessing protected method
        return f"Manager: {self.name}, Department: {self._department}, Team Size: {self.team_size}"


# Demonstrating protected vs private access
manager = Manager("Alice Johnson", "Engineering", 10)
print(manager.get_manager_info())

# Protected attributes can be accessed (but shouldn't be from outside)
print(f"Department (protected): {manager._department}")  # Works but not recommended

# Private attributes from parent cannot be accessed
# print(manager.__social_security)  # This would raise AttributeError


print("="*50, "\nENCAPSULATION SUMMARY:\n1. Public attributes: accessible from\
      anywhere (no underscore)\n2. Protected attributes: intended for class\
      and subclasses (single _)\n3. Private attributes: only accessible within\
      the class (double __)\n4. Use getters/setters for controlled access to\
      private data\n5. Encapsulation prevents unauthorized access and ensures\
      data integrity")
