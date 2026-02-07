"""Class Variables demonstration.

Reference: https://youtu.be/BJ-VvGyQxho?si=PkKi03VpJ43HqUgs
"""


class Employee():
    """Basic Employee class without class variables."""

    def __init__(self, firstname, lastname, salary):
        # Instance as the first arg, self is just a convention, we can use any
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + lastname + "@gmail.com"
        self.salary = salary

    def fullname(self):
        """Return the full name of the employee."""
        # self refers to this instance of the class
        return self.firstname + " " + self.lastname

    def applyraise(self):
        """Apply a salary raise."""
        self.salary = int(self.salary * 1.05)


pvp = Employee("Prashant", "Vikram", 10000)
print("Starting salary : ", pvp.salary)
pvp.applyraise()
print("After raise salary : ", pvp.salary)

# The perecentage by which the salary is increasing is hidden rn
# Use case : What if I want to know/update the raise percentage
# This would be manual effort as it could be at multiple locations
# Hence make this a class variable


class Employee():
    """Employee class with raise percentage as class variable."""

    raise_perc = 1.05

    def __init__(self, firstname, lastname, salary):
        # Instance as the first arg, self is just a convention, we can use any
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + lastname + "@gmail.com"
        self.salary = salary

    def fullname(self):
        # self refers to this instance of the class
        return self.firstname + " " + self.lastname

    def applyraise(self):
        # Can't directly pass this variable directly
        # Either we've to pass is using class or instance of the class
        self.salary = int(self.salary * Employee.raise_perc)


pvp = Employee("Prashant", "Vikram", 10000)
print("Starting salary : ", pvp.salary)
pvp.applyraise()
print("After raise salary : ", pvp.salary)

# Class variables can be accessed using class or instance of the class
# When we access the class variable using instance/class it searches the class
# or the upper class the sub-class is derived from and fetches the class var
print(Employee.raise_perc)
print(pvp.raise_perc)

# Get namespace of an instance, this doesn't return the raise_perc
print(pvp.__dict__)

# Class does contain raise_perc attribute
print(Employee.__dict__)


# How to change the raise_perc for all the instances of the class
# We can change the class variable using the class name, this will change the
# value for all the instances of the class
Employee.raise_perc = 1.07
print(Employee.raise_perc)
print(pvp.raise_perc)

# What if we change the class variable using the instance of the class
# This will create a new instance variable with the same name as the class var
pvp.raise_perc = 1.08
print(Employee.raise_perc)
print(pvp.raise_perc)


class Employee():
    """Employee class with employee count tracking."""

    # employee_count should be consistent throughout the instances and class
    employee_count = 0
    raise_perc = 1.05

    def __init__(self, firstname, lastname, salary):
        # Instance as the first arg, self is just a convention, we can use any
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + lastname + "@gmail.com"
        self.salary = salary

        # As soon as any object of this class in instantiated
        # Increase the employee count by 1
        Employee.employee_count += 1

    def fullname(self):
        # self refers to this instance of the class
        return self.firstname + " " + self.lastname

    def applyraise(self):
        # Can't directly pass this variable directly
        # Either we've to pass is using class or instance of the class
        self.salary = int(self.salary * Employee.raise_perc)


print(Employee.employee_count)

pvp = Employee("Prashant", "Vikram", 10000)
print(pvp.employee_count)
print(Employee.employee_count)

gpt = Employee("CHAT", "gpt", "5000")
print(gpt.employee_count)
print(Employee.employee_count)
