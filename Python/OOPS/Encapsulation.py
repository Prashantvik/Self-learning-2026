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


# Example 1: ATM class WITHOUT encapsulation (poor practice)
class ATM():
    """Simple ATM machine implementation with basic banking operations."""
    # Class variable
    wrong_pin_entered = 0

    def __init__(self, amount=0):
        self.pin = None
        self.amount = amount

    def start(self):
        self.menu()

    # Created this just to get the output purpose
    def atm_details(self):
        return f"User's atm pin is {self.pin} and balance is {self.amount}"

    def menu(self):
        """Display the main menu and handle user input."""
        user_input = input("Hello, welcome to SBI ATM. "
                           "Please select an option from the menu below : \n"
                           "1. Set pin \n"
                           "2. Check balance \n"
                           "3. Withdraw money \n"
                           "4. Deposit money \n"
                           "5. Exit \n")

        # After once operation is done, menu will be shown again to the
        # user until user selects exit option
        if user_input == "1":
            self.set_pin()
            self.menu()
        elif user_input == "2":
            self.check_balance()
            self.menu()
        elif user_input == "3":
            self.withdraw_money()
            self.menu()
        elif user_input == "4":
            self.deposit_money()
            self.menu()
        elif user_input == "5":
            return
        else:
            print("Invalid input. Please try again.")
            self.menu()

    def enter_and_validated_pin(self):
        """Validate user entered PIN and handle wrong attempts."""
        pin_entered = input("Please enter your pin : ")
        if self.pin is None:
            print("Please set your pin first.")
            self.set_pin()
        if self.pin == pin_entered:
            return True
        print("Wrong pin entered, after 3 wrong tries atm will be blocked.")
        if ATM.wrong_pin_entered == 3:
            print("Your ATM is blocked now due to multiple wrong pins tries.")
        else:
            ATM.wrong_pin_entered += 1
        return False

    def set_pin(self):
        """Allow user to set their PIN."""
        pin = input("Please enter pin : ")
        self.pin = pin
        print("Pin set successfully")

    def check_balance(self):
        """Display current account balance after PIN validation."""
        if self.enter_and_validated_pin():
            print(f"Current balance of the account - {self.amount}")

    def withdraw_money(self):
        """Allow user to withdraw money after PIN validation."""
        if self.enter_and_validated_pin():
            amount_to_be_withdrawn = int(input("Please enter the amount : "))
            if amount_to_be_withdrawn > self.amount:
                print("Insufficient balance")
            else:
                self.amount -= amount_to_be_withdrawn
                print("Please collect your cash")

    def deposit_money(self):
        """Allow user to deposit money after PIN validation."""
        if self.enter_and_validated_pin():
            amount_to_be_deposited = int(input("Please enter the amount : "))
            self.amount += amount_to_be_deposited
            print("Amount has been deposited, thank-you!")


Prashant = ATM(amount=1000)

# Prashant.start()    # Use this carefully

# Problem: We can directly access and modify attributes from outside
# This violates encapsulation principles and can lead to data integrity issues
print(f"Before unauthorized changes details: {Prashant.atm_details()}")
print(Prashant.pin)
Prashant.pin = 5555    # Direct access - not secure
Prashant.amount = -10    # Invalid pin - no validation
print(f"After unauthorized changes details: {Prashant.atm_details()}")


# Example 2: ATM class WITH encapsulation (good practice)
class EncapsulatedATM():
    """Simple ATM machine implementation with basic banking operations."""
    # Class variable
    wrong_pin_entered = 0

    def __init__(self, amount=0):
        self.__pin = None       # Private attribute
        self.__amount = amount  # Private attribute

    # Public methods to access private data (getters)
    def atm_details(self):
        return f"User's atm pin is {self.__pin} and balance is {self.__amount}"

    # Public methods to modify private data (setters) with validation
    def set_pin_setter(self, pin):
        """Set atm pin with validation."""
        if isinstance(pin, int) and pin > 0 and len(str(pin)) == 4:
            self.__pin = pin
        else:
            print("Invalid pin! PIN must be a non-empty integer of 4 digits.")

    def start(self):
        self.menu()

    def menu(self):
        """Display the main menu and handle user input."""
        user_input = input("Hello, welcome to SBI ATM. "
                           "Please select an option from the menu below : \n"
                           "1. Set pin \n"
                           "2. Check balance \n"
                           "3. Withdraw money \n"
                           "4. Deposit money \n"
                           "5. Exit \n")

        # After once operation is done, menu will be shown again to the
        # user until user selects exit option
        if user_input == "1":
            self.set_pin()
            self.menu()
        elif user_input == "2":
            self.check_balance()
            self.menu()
        elif user_input == "3":
            self.withdraw_money()
            self.menu()
        elif user_input == "4":
            self.deposit_money()
            self.menu()
        elif user_input == "5":
            return
        else:
            print("Invalid input. Please try again.")
            self.menu()

    def enter_and_validated_pin(self):
        """Validate user entered PIN and handle wrong attempts."""
        pin_entered = input("Please enter your pin : ")
        if self.pin is None:
            print("Please set your pin first.")
            self.set_pin()
        if self.pin == pin_entered:
            return True
        print("Wrong pin entered, after 3 wrong tries atm will be blocked.")
        if ATM.wrong_pin_entered == 3:
            print("Your ATM is blocked now due to multiple wrong pins tries.")
        else:
            ATM.wrong_pin_entered += 1
        return False

    def set_pin(self):
        """Allow user to set their PIN."""
        pin = input("Please enter pin : ")
        self.pin = pin
        print("Pin set successfully")

    def check_balance(self):
        """Display current account balance after PIN validation."""
        if self.enter_and_validated_pin():
            print(f"Current balance of the account - {self.amount}")

    def withdraw_money(self):
        """Allow user to withdraw money after PIN validation."""
        if self.enter_and_validated_pin():
            amount_to_be_withdrawn = int(input("Please enter the amount : "))
            if amount_to_be_withdrawn > self.amount:
                print("Insufficient balance")
            else:
                self.amount -= amount_to_be_withdrawn
                print("Please collect your cash")

    def deposit_money(self):
        """Allow user to deposit money after PIN validation."""
        if self.enter_and_validated_pin():
            amount_to_be_deposited = int(input("Please enter the amount : "))
            self.amount += amount_to_be_deposited
            print("Amount has been deposited, thank-you!")

    # Private method - can only be accessed within the class
    def __calculate_interest(self):
        """Calculate interest gained on the amount (private method)."""
        return self.__amount * 0.1

    def get_base_amount(self):
        """Get annual package including bonus."""
        bonus = self.__calculate_interest()
        return self.__amount + bonus


pvp = EncapsulatedATM(10000)


# Now we cannot directly access private attributes
# These will raise AttributeError or create new (not accessing the private)
try:
    print(pvp.__pin)  # This won't work
except AttributeError:
    print("Cannot access private attribute __pin directly")

# We must use public methods to interact with the object
pvp.set_pin_setter(1234)              # Valid change
pvp.set_pin_setter("Prashant")        # Invalid - will be rejected
pvp.set_pin_setter(67890)             # Invalid - will be rejected
print(f"Updated details: {pvp.atm_details()}")
print(f"Annual package: ${pvp.get_base_amount()}")

# Trying to access private method directly won't work
# pvp.__calculate_interest()  # This would raise AttributeError


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
        return f"Manager: {self.name}, Department: {self._department},"\
               f"Team Size: {self.team_size}.\n"\
               f"{internal_info}"


# Demonstrating protected vs private access
manager = Manager("Alice Johnson", "Engineering", 10)
print(manager.get_manager_info())

# Protected attributes can be accessed (but shouldn't be from outside)
# Works but not recommended
print(f"Department (protected): {manager._department}")

# Private attributes from parent cannot be accessed
# print(manager.__social_security)  # This would raise AttributeError


print("="*50, "\nENCAPSULATION SUMMARY:\n1. Public attributes: accessible from\
 anywhere (no underscore)\n2. Protected attributes: intended for class\
 and subclasses (single _)\n3. Private attributes: only accessible within\
 the class (double __)\n4. Use getters/setters for controlled access to\
 private data\n5. Encapsulation prevents unauthorized access and ensures\
 data integrity")

# Nothing in python is truly private, but these conventions helps

# Getter and Setter in Encapsulation
# Refer : Python/OOPS/Property Decorators.py


class ATM():
    """Simple ATM machine implementation with basic banking operations."""
    # Class variable
    wrong_pin_entered = 0

    def __init__(self, amount=0):
        self.pin = None
        self.amount = amount

    def start(self):
        self.menu()

    def menu(self):
        """Display the main menu and handle user input."""
        user_input = input("Hello, welcome to SBI ATM. "
                           "Please select an option from the menu below : \n"
                           "1. Set pin \n"
                           "2. Check balance \n"
                           "3. Withdraw money \n"
                           "4. Deposit money \n"
                           "5. Exit \n")

        # After once operation is done, menu will be shown again to the
        # user until user selects exit option
        if user_input == "1":
            self.set_pin()
            self.menu()
        elif user_input == "2":
            self.check_balance()
            self.menu()
        elif user_input == "3":
            self.withdraw_money()
            self.menu()
        elif user_input == "4":
            self.deposit_money()
            self.menu()
        elif user_input == "5":
            return
        else:
            print("Invalid input. Please try again.")
            self.menu()

    def enter_and_validated_pin(self):
        """Validate user entered PIN and handle wrong attempts."""
        pin_entered = input("Please enter your pin : ")
        if self.pin is None:
            print("Please set your pin first.")
            self.set_pin()
        if self.pin == pin_entered:
            return True
        print("Wrong pin entered, after 3 wrong tries atm will be blocked.")
        if ATM.wrong_pin_entered == 3:
            print("Your ATM is blocked now due to multiple wrong pins tries.")
        else:
            ATM.wrong_pin_entered += 1
        return False

    def set_pin(self):
        """Allow user to set their PIN."""
        pin = input("Please enter pin : ")
        self.pin = pin
        print("Pin set successfully")

    def check_balance(self):
        """Display current account balance after PIN validation."""
        if self.enter_and_validated_pin():
            print(f"Current balance of the account - {self.amount}")

    def withdraw_money(self):
        """Allow user to withdraw money after PIN validation."""
        if self.enter_and_validated_pin():
            amount_to_be_withdrawn = int(input("Please enter the amount : "))
            if amount_to_be_withdrawn > self.amount:
                print("Insufficient balance")
            else:
                self.amount -= amount_to_be_withdrawn
                print("Please collect your cash")

    def deposit_money(self):
        """Allow user to deposit money after PIN validation."""
        if self.enter_and_validated_pin():
            amount_to_be_deposited = int(input("Please enter the amount : "))
            self.amount += amount_to_be_deposited
            print("Amount has been deposited, thank-you!")


Prashant = ATM(amount=1000)

# Prashant.start()
