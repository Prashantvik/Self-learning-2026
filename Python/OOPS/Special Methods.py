# Reference : https://youtu.be/3ohzBxoFHAY?si=2RxSZpfrHL5Sn5mH

# Special Methods : Magic/Dunder methods [Double Underscore Methods]
# Use case : When we want to define how our objects should behave with
# built-in functions or operators, we can use special methods. These
# methods allow us to customize the behavior of our objects when they
# are used with certain operations.

# Special methods are not called directly, but are invoked by the Python
# interpreter when certain operations are performed on the objects.
# Magic methods gets trigered automatically like init when object is created.
class Employee():
    raise_perc = 1.05

    # Dunder method : __init__() - Constructor
    def __init__(self, firstname, lastname, salary):
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + lastname + "@gmail.com"
        self.salary = salary

    def fullname(self):
        return self.firstname + " " + self.lastname

    def applyraise(self):
        self.salary = int(self.salary * Employee.raise_perc)

    # Dunder method : __str__() - String representation of the object
    # This method is called when we print the object or when we use str()
    # function on the object
    def __str__(self):
        return f"Employee: {self.fullname()} - {self.email}"

    # Dunder method : __repr__() - Official string representation of the object
    # This method is called when we use repr() function on the object or when
    # we inspect the object in the console
    def __repr__(self):
        return f"Employee('{self.firstname}','{self.lastname}',{self.salary})"

    def __add__(self, other):
        if isinstance(other, Employee):
            return self.salary + other.salary
        return NotImplemented
        # Fallback to default behavior if other is not an Employee

    def __len__(self):
        return len(self.fullname())

    def __del__(self):
        print(f"Employee {self.fullname()} is being deleted.")


pvp_emp = Employee("Prashant", "Vikram", 10000)
corey = Employee("Corey", "Schafer", 75000)

# Printing the object will print the memory location of the object normally
print(pvp_emp)          # Output : <__main__.Employee object at 0x7f8c8c8c8c8>
print(pvp_emp.__str__())
print(pvp_emp.__repr__())

# Dunder method : __add__()
print(pvp_emp + corey)

print(pvp_emp.__add__(corey))
print(int.__add__(1, 2))
print(str.__add__("Hello", " World"))

print(len(pvp_emp))

# Dunder method : __del__()
# Note : The __del__() method is called when an object is about to be
# destroyed. However, the exact timing of when this method is called can be
# unpredictable, as it depends on the garbage collection process. Therefore,
# it's generally not recommended to rely on the __del__() method for critical
# cleanup tasks.
print("About to delete pvp_emp explicitly...")
del pvp_emp
print("pvp_emp deleted explicitly.")
print("Script continuing... corey object still exists.")
print(f"Corey's name: {corey.fullname()}")
print("Script ending... Python will clean up remaining objects.")
