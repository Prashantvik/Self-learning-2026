"""Class methods and Static methods demonstration.

Reference: https://youtu.be/rq8cL2XMM5M?si=8sVWjSnZxp7LvUc-
"""
import datetime


class Employee():
    """Employee class demonstrating class methods and static methods.

    CLASS METHODS:
    Regular methods in a class automatically take an instance as first arg.
    By convention instance arg is called self.
    """
    raise_perc = 1.05

    def __init__(self, firstname, lastname, salary):
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + lastname + "@gmail.com"
        self.salary = salary

    def fullname(self):
        """Return the full name of the employee."""
        return self.firstname + " " + self.lastname

    def applyraise(self):
        """Apply a salary raise."""
        self.salary = int(self.salary * Employee.raise_perc)

    # Decorator classmethod, common convention for class is cls
    # In class method, class is passed as the first argument
    @classmethod
    def set_raise_pec(cls, raise_perc):
        """Set the raise percentage for all employees (class method)."""
        cls.raise_perc = raise_perc


pvp = Employee("Prashant", "Vikram", 10000)

print(Employee.raise_perc)
print(pvp.raise_perc)

Employee.set_raise_pec(1.10)

print(Employee.raise_perc)
print(pvp.raise_perc)

# Class methods as alternative constructers, multiple ways of creating objects
# Use case : Employee info is coming in string format
# We can create a class method to parse the string and create an object
pvp_str = "Prashant-Vikram-10000"
emp_str = "Jane-Doe-80000"


# Real life example of using class method as constructor
# Click on datetime in vscode and search @class in the datetime.py
# import datetime
class Employee():
    """Employee class with class method as alternative constructor."""
    raise_perc = 1.05

    def __init__(self, firstname, lastname, salary):
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + lastname + "@gmail.com"
        self.salary = salary

    def fullname(self):
        return self.firstname + " " + self.lastname

    def applyraise(self):
        self.salary = int(self.salary * Employee.raise_perc)

    @classmethod
    def set_raise_pec(cls, raise_perc):
        """Set the raise percentage for all employees (class method)."""
        cls.raise_perc = raise_perc

    # Class method to instantiate an object | Alternative constructor
    @classmethod
    def from_string(cls, emp_str):
        """Create Employee object from string format (alternative constructor)."""
        firstname, lastname, salary = emp_str.split("-")
        return cls(firstname, lastname, salary)  # Note


pvp = Employee.from_string(pvp_str)
print(pvp.email)
print(pvp.salary)

jane = Employee.from_string(emp_str)
print(jane.email)
print(jane.salary)


# STATIC METHODS
# Regular methods and class methods take self and cls as first arg
# Meanwhile in static method, nothing is passed as first arg
# Static method exists solely for logical connection within the class
class Employee():
    """Employee class demonstrating static methods."""
    raise_perc = 1.05

    def __init__(self, firstname, lastname, salary):
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + lastname + "@gmail.com"
        self.salary = salary

    def fullname(self):
        return self.firstname + " " + self.lastname

    def applyraise(self):
        self.salary = int(self.salary * Employee.raise_perc)

    @classmethod
    def set_raise_pec(cls, raise_perc):
        cls.raise_perc = raise_perc

    # Class method to instantiate an object | Alternative constructor
    @classmethod
    def from_string(cls, emp_str):
        firstname, lastname, salary = emp_str.split("-")
        return cls(firstname, lastname, salary)

    @staticmethod
    def is_workday(day):
        """Check if a given day is a workday (static method)."""
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True


pvp = Employee("Prashant", "Vikram", 10000)

my_date = datetime.date(2024, 7, 23)

print(pvp.fullname())
print(pvp.is_workday(my_date))
