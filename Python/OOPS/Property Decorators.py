"""Property Decorators - Getters, Setters, and Deleters demonstration.
Encapsulation, Setters, and Getters — Key Points
- Encapsulation is about controlling access, not completely hiding data
- Setters act as gatekeepers for writing data
- Setters validate input and enforce rules/invariants
- They centralize logic, so changes happen safely in one place
- They prevent the object from entering an invalid state

Getters — important caveats
- Getters can leak internal state if they return mutable objects
- They may create tight coupling by exposing internal structure
- Prefer returning immutable values or copies
- Expose behavior over raw data when possible

Rule of thumb
- Setters protect writes
- Getters must protect representation
"""


class Employee:
    def __init__(self, firstname, lastname, department, experince,
                 employee_id):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__department = department
        self.__experience = experince
        self.__employee_id = employee_id
        # Initially acccessing this as an attribute
        self.email = self.__firstname + self.__lastname + "@gmail.com"

    def get_employee_details(self):
        print(f"Here's the employee detials : \n"
              f"Id : {self.__employee_id}\n"
              f"Name : {self.__firstname} + " " + {self.__lastname}\n"
              f"Department : {self.__department}\n"
              f"Experience : {self.__experience} years."
              )

    def update_department(self, depatment):
        if isinstance(depatment, str) and len(depatment) > 0 \
                and len(depatment) < 10:
            self.__department = depatment
            print(f"Department of employee [ID : {self.__employee_id} "
                  f"has been updated]")

    def get_fullname(self):
        return "{} {}".format(self.__firstname, self.__lastname)


pvp = Employee("Prashant", "Vikram", "Data & Product", 4, 1)

pvp.get_employee_details()

try:
    print(pvp.__department)
except AttributeError as e:
    print(f"Can't get the department of the user - {e}")

# A new attribute is added dynamically
pvp.__department = "DevOps"
print(pvp.__department)

pvp.get_employee_details()

print(pvp.email)


# Getters and Setter
class Employee:
    """We can use property decorator in python, we can created a method but can
    access it like an attribute"""
    def __init__(self, firstname, lastname, department, experince,
                 employee_id):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__department = department
        self.__experience = experince
        self.__employee_id = employee_id
        # Initially acccessing this as an attribute
        # self.email = self.__firstname + self.__lastname + "@gmail.com"

    def get_employee_details(self):
        print(f"Here's the employee detials : \n"
              f"Id : {self.__employee_id}\n"
              f"Name : {self.__firstname} + " " + {self.__lastname}\n"
              f"Department : {self.__department}\n"
              f"Experience : {self.__experience} years."
              )

    def update_department(self, depatment):
        if isinstance(depatment, str) and len(depatment) > 0 \
                and len(depatment) < 10:
            self.__department = depatment
            print(f"Department of employee [ID : {self.__employee_id} "
                  f"has been updated]")

    def get_fullname(self):
        return "{} {}".format(self.__firstname, self.__lastname)

    @property
    def email(self):
        return "{}.{}@gmail.com".format(self.__firstname, self.__lastname)


pvp = Employee("Prashant", "Vikram", "Data & Product", 4, 1)

pvp.get_employee_details()
print(pvp.email)

# After method implementation | This would break existing code
# pvp.email vs pvp.email()
# print(pvp.email())      # Throws : TypeError: 'str' object is not callable


# We can used "property" decorator to call method as an attribute
print(pvp.email)
