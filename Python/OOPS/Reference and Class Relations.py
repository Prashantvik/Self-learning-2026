"""
- Pass by reference means that when you pass an object to a function, you are
passing a reference to that object. This means that if you modify the object
inside the function, it will affect the original object outside the function.
- Pass by value means that when you pass an object to a function, you are
passing a copy of that object. This means that if you modify the object inside
the function, it will not affect the original object outside the function.
"""


class Employee():
    """Basic Employee class without class variables."""

    def __init__(self, firstname, lastname, salary):
        # Instance as the first arg, self is just a convention
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


# pvp is a reference variable here
pvp = Employee("Prashant", "Vikram", 1000)


class Customer():
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


mvp = Customer("Raghav", "M")
tks = Customer("Ananya", "F")

print(mvp.name)


# Create a function and pass class as an argument
# In python everything is an object, just like int you can pass the class
def greet(Customer):
    if Customer.gender == "M":
        print(f"Hello! {Customer.name} sir")
    else:
        print(f"Hello! {Customer.name} ma'am")


greet(mvp)
greet(tks)


# Pass by reference
def get_location(Customer):
    print(f"Object is located as {id(Customer)} with name {Customer.name}")
    Customer.name = "Dexter"
    print(Customer.name)


# Both will point to the same location
# Since this is pass by reference any change inside a function is permanent
print(f"Object is located as {id(mvp)} with name {mvp.name}")
get_location(mvp)
print(mvp.name)

# =========================================================================== #
# =========================================================================== #
# Explain Aggregation, Inheritance, and Composition in Python OOPS
"""
- Aggregation is a relationship between two classes where one class contains
a reference to another class. It is a "has-a" relationship. For example, a Car
class can have an Engine class as an attribute. The Car class can exist
without the Engine class, but the Engine class cannot exist without the
Car class.
- Inheritance is a relationship between two classes where one class inherits
the properties and behaviors of another class. It is an "is-a" relationship.
For example, a Dog class can inherit from an Animal class. The Dog class can
have its own properties and behaviors, but it also has access to the properties
and behaviors of the Animal class.
- Composition is a relationship between two classes where one class contains
an instance of another class. It is a "part-of" relationship. For example,
a House class can have a Room class as an attribute. The House class can exist
swithout the Room class, but the Room class cannot exist without the
House class.
"""
