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


class BankAccount:
    """A bank account class that demonstrates encapsulation with private attributes."""

    def __init__(self, account_number, balance):
        self.__account_number = account_number  # Private attribute
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: {amount}. New Balance: {self.__balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew: {amount}. New Balance: {self.__balance}")
        else:
            print("Insufficient funds or invalid withdrawal amount.")

    def get_balance(self):
        """Get the current account balance."""
        return print(f"Current balance is - {self.__balance}")

    def know_your_account_number(self):
        return print(f"Your account number is - {self.__account_number}")


pvp = BankAccount(999999, 10000)

pvp.withdraw(5000)
pvp.know_your_account_number()
pvp.get_balance()
pvp.deposit(4000)
pvp.get_balance()
