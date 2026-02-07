# Reference : https://youtu.be/ZDa-Z5JzLYM?si=kgP2W1LxC1ep278l
# Corey Schafer - Python OOPS Tutorial
# Method is a function inside a class, attributed is an variable
# Blueprint of an entity is a class

class Employee:
    pass


# Instantion of class
emp1 = Employee()
emp2 = Employee()

print(emp1)
print(emp2)

emp1.firstname = 'Prashant'
emp1.lastname = 'Vikram'
emp1.email = 'Prashantvikram@gmail.com'

print(emp1.firstname)
print(emp1.lastname)
print(emp1.email)


class Employee():
    def __init__(self, firstname, lastname, salary):
        # Intance as the first arg, self is just a convention, we can use any
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + lastname + "@gmail.com"
        self.salary = salary

    def fullname(self):
        # self refers to this instance of the class
        return self.firstname + " " + self.lastname


pvp = Employee("Prashant", "Vikram", 10000)

print(pvp.firstname)   # Attribute
print(pvp.email)       # Attribute
print(pvp.fullname())  # Method

# Calling method using the class and passing the instance as the arg
Employee.fullname(emp1)


# Self is just a convention. Self is used to refer to the instance of the class
class Person():
    def __init__(self, name):
        self.name = name
        print(id(self))

    def sayhi(self):
        print("Hi, I am " + self.name)


print("=" * 30)
pvp = Person("Prashant")
print(id(pvp))
print("The id of the instance is same as the id of self,\n" \
      "which means self refers to the instance of the class.")
print("=" * 30)
