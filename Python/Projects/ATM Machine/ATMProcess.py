"""Implementation of simple ATM Machine logic using class."""


class ATM():
    """Simple ATM machine implementation with basic banking operations."""
    # Class variable
    wrong_pin_entered = 0

    def __init__(self, amount=0):
        self.pin = None
        self.amount = amount
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
            exit()
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

# Real ATM machine implementation will be more complex and have more features
# 1. Multiple accounts handling
# 2. Account number and pin validation
# 3. Transaction history
# 4. Different types of accounts (savings, current, etc.)
