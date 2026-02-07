"""Inheritance - Creating Subclasses demonstration.

Reference: https://youtu.be/RSl87lqOXDE?si=edal_68UsPPfdRnu
"""


class Employee():
    """Base Employee class for inheritance examples."""
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


pvp_emp = Employee("Prashant", "Vikram", 10000)
joe = Employee("Joe", "Smith", 20000)


class Developers(Employee):
    """Developer class that extends Employee with programming language."""

    def __init__(self, firstname, lastname, salary, primary_language):
        super().__init__(firstname, lastname, salary)
        self.primary_language = primary_language

    def get_primary_language(self):
        """Get the developer's name and primary programming language."""
        return super().fullname() + " - " + self.primary_language


chatgpt = Developers("Chat", "GPT", 10000, "Python")
print(chatgpt.get_primary_language())

John = Developers("John", "Doe", 35000, "Java")
Grok = Developers("Grok", "XMusk", 67890, "LLM")


class Managers(Developers):
    """Manager class that extends Developers with team management capabilities."""

    level = "E4"

    def __init__(self, firstname, lastname, salary, primary_language,
                 designation, emps=None):
        super().__init__(firstname, lastname, salary, primary_language)
        self.designation = designation
        if emps is None:
            self.emps = []
        else:
            self.emps = emps

    def get_name_designation(self):
        return super().fullname() + " - " + self.designation

    def add_employee(self, emp):
        if emp not in self.emps:
            self.emps.append(emp)

    def remove_employee(self, emp):
        if emp in self.emps:
            self.emps.remove(emp)

    def get_subordinates_names(self):
        if self.emps:
            print(f"Subordinates names for : {self.fullname()}")
            for index in range(len(self.emps)):
                print(index, " : ", self.emps[index].fullname())
        return None

    @classmethod
    def get_level(cls):
        return Managers.level


pvp = Managers("Prashant", "Vikram", 10000, "C++", "SWE Lead",
               emps=[chatgpt, John])
print(pvp.get_name_designation())
print(pvp.get_primary_language())
print(pvp.get_level())
pvp.get_subordinates_names()
pvp.add_employee(Grok)
pvp.get_subordinates_names()


# Method Resolution Order (MRO) | Python earches for methods & attributes
# print(help(Developers))
#  | Method resolution order:
#        Developers
#        Employee
#        builtins.object
#  | Methods defined here:
#  | Methods inherited from Employee:
#  | Data descriptors inherited from Employee:
#  | Data and other attributes inherited from Employee:


# To check if an object is an instance of a class
print(isinstance(pvp, Managers))            # --> Note
print(isinstance(pvp, Employee))            # --> Note
print(isinstance(pvp, Developers))          # --> Note

print(isinstance(chatgpt, Developers))
print(isinstance(chatgpt, Managers))
print(isinstance(chatgpt, Employee))


# Method overriding
# If a method is defined in both the parent class and the child class,
# the method in the child class will override the method in the parent class.
# This is called method overriding.
class Managers(Developers):
    level = "E4"

    # Method overriding
    def __init__(self, firstname, lastname, salary, primary_language,
                 designation, emps=None):
        super().__init__(firstname, lastname, salary, primary_language)
        self.designation = designation
        if emps is None:
            self.emps = []
        else:
            self.emps = emps

    def get_name_designation(self):
        return super().fullname() + " - " + self.designation

    def get_primary_language(self):
        return super().fullname() + " - " + self.designation + \
               " - " + self.primary_language

    def add_employee(self, emp):
        if emp not in self.emps:
            self.emps.append(emp)


# Method overloading
# Method overloading in general refers to the ability to define multiple
# methods with the same name but different parameters.
# Python does not support method overloading in the traditional sense.
# We can achieve similar functionality using default args or *args & **kwargs.
class Calculator:
    """Calculator class demonstrating method overloading simulation."""

    def add(self, nums1, nums2, nums3=0):
        """Add two or three numbers."""
        return nums1 + nums2 + nums3


calc = Calculator()
print(calc.add(1, 2))      # Output: 3
print(calc.add(1, 2, 3))   # Output: 6


# Diamond problem (Python style)
# The diamond problem occurs in an inheritance hierarchy that forms a diamond
# Class A is the base class.
# Classes B and C both inherit from Class A.
# Class D inherits from both Classes B and C.
# If a method is defined in Class A but is overridden in both Class B and
# Class C, the ambiguity arises when you call that method from an instance of D
# Which version (B's or C's) should be executed?

class A:
    """Base class A for diamond problem demonstration."""

    def method(self):
        print("Method in class A")


class B(A):
    """Class B inheriting from A."""

    def method(self):
        print("Method in class B")


class C(A):
    """Class C inheriting from A."""

    def method(self):
        print("Method in class C")


class D(B, C):
    """Class D inheriting from both B and C (diamond problem)."""
    pass


d = D()
d.method()  # Output: Method in class B


# Rule of thumb: Prefer composition over inheritance
# The principle of "prefer composition over inheritance" is a guideline in OOP
# that advocates designing systems using a "has-a" relationship (composition)
# rather than an "is-a" relationship (inheritance) in most scenarios.
# This preference is based on the idea that composition leads to more flexible,
# modular, and maintainable code, while inheritance can create rigid, tightly
# coupled systems that are difficult to adapt to future changes.

# Real life example of Prefer composition over inheritance
class Employee:
    """Employee class for composition example."""

    def __init__(self, name):
        self.name = name


class Department:
    """Department class demonstrating composition over inheritance."""

    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        """Add an employee to the department."""
        self.employees.append(employee)

# Refer Docs.md for more details on composition vs inheritance
