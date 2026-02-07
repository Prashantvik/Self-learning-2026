"""Creating a Fraction class to represent a fraction and perform operations.

Reference: https://www.tutorialsteacher.com/python/magic-methods-in-python
"""


class Fraction:
    """A class to represent mathematical fractions and perform operations on them."""
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        """Return string representation of the fraction."""
        return f"{self.numerator}/{self.denominator}"

    # Dunder/Magic method implementation
    def __add__(self, other):
        """Add two fractions."""
        new_numerator = (self.numerator * other.denominator 
                        + other.numerator * self.denominator)
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __sub__(self, other):
        """Subtract two fractions."""
        new_numerator = (self.numerator * other.denominator 
                        - other.numerator * self.denominator)
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other):
        """Multiply two fractions."""
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other):
        """Divide two fractions."""
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return Fraction(new_numerator, new_denominator)


fraction1 = Fraction(6, 2)
fraction2 = Fraction(5, 2)

print(f"Fractions : {fraction1} and {fraction2}")

print(fraction1 + fraction2)
print(fraction1 - fraction2)
print(fraction1 * fraction2)
print(fraction1 / fraction2)
