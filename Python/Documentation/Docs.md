## Object-Oriented Programming (OOP) Concepts

#### Good Reference : https://www.youtube.com/watch?v=Mf2RdpEiXjU
#### Default Reference : https://www.youtube.com/@coreyms

### Class and Object
- **Class**: A blueprint for creating objects. It defines a set of attributes and methods that the created objects will have. For example, a `Car` class might have attributes like `make`, `model`, and `year`, and methods like `start_engine()` and `stop_engine()`.
- **Object**: An instance of a class. It is a specific realization of the class with actual values for the attributes. For example, an object of the `Car` class could be `my_car = Car(make='Toyota', model='Corolla', year=2020)`

### Class Methods and Static Methods
- **Class Methods**: These methods are bound to the class and not the instance of the class. They can modify the class state that applies across all instances of the class. They are defined using the `@classmethod` decorator and take `cls` as the first parameter.
- **Static Methods**: These methods are not bound to the class or instance. They do not modify class or instance state. They are defined using the `@staticmethod` decorator and do not take `self` or `cls` as a parameter.


### Self Parameter
- The `self` parameter in Python is a reference to the current instance of the class. It is used to access variables that belong to the class. It must be the first parameter of any method in the class, and it allows you to access attributes and methods of the instance. 
- For example, in a method defined as `def start_engine(self):`, you can access the instance's attributes using `self.attribute_name`.
- The `self` parameter is not a keyword in Python, but it is a strong convention that should be followed to maintain code readability and consistency.


### Inheritance
Inheritance is a fundamental concept in object-oriented programming (OOP) that allows a new class (called a child or subclass) to inherit properties and behaviors (attributes and methods) from an existing class (called a parent or superclass). This promotes code reusability and establishes a natural hierarchical relationship between classes.


### Inheritance vs Composition: A Real-Life Example
Using composition to create a relationship between Employee and Department
Has a relationship: A Department has Employees, but an Employee is not a Department
This design allows for greater flexibility and modularity, as we can easily
Is a relationship: An Employee is a Department, but a Department is not an Employee
This design can lead to a rigid and tightly coupled system, as changes to
the Department class may require changes to the Employee class, and vice versa.


Think about **Building a burger**.

### Inheritance way (not great in real life)

You say:

* A **CheeseBurger IS A Burger**
* A **DoubleCheeseBurger IS A CheeseBurger**
* A **BaconDoubleCheeseBurger IS A DoubleCheeseBurger**

Now your class hierarchy is a mess.
What if someone wants:

* no cheese
* extra bacon
* gluten-free bun
* vegan patty

You’d need **hundreds of subclasses**. Chaos.

---

### Composition way (how real life actually works)

A burger is **made of parts**:

* Bun
* Patty
* Cheese
* Bacon
* Sauce

You *compose* a burger by **putting things together**, not by inheriting.

```text
Burger
 ├── Bun
 ├── Patty
 ├── Cheese (optional)
 ├── Bacon (optional)
 └── Sauce
```

You don’t say:

> “This burger *is a* cheese burger”

You say:

> “This burger **has cheese**”

That’s composition.

---

### Why composition wins in real life

**Flexible** – add/remove parts without redesigning everything
**Reusable** – cheese can go on burgers, fries, tacos
**No fragile hierarchies** – changing cheese doesn’t break burgers
**Matches reality** – objects are usually *made of* things, not *types of* things

### Another quick real-life example

**Car**

Bad (inheritance):

* ElectricCar extends Car
* HybridCar extends Car
* SolarHybridCarWithHeatedSeats extends HybridCar

Good (composition):

* Car **has** Engine
* Car **has** Battery
* Car **has** Seats

Swap parts, not parents.

---

### One-line takeaway

> **Inheritance models “what something IS”**
> **Composition models “what something HAS”**


### Encapsulation
- Encapsulation is the concept of bundling data (attributes) and methods that operate on that data into a single unit, or class. It also involves restricting direct access to some of an object's components, which is a means of preventing accidental interference and misuse of the data. In Python, this is typically achieved using private attributes (prefixing with `_` or `__`) and providing public getter and setter methods to access and modify those attributes.
- For example, a `BankAccount` class might have a private attribute `_balance` and public methods `deposit(amount)` and `withdraw(amount)` to manipulate the balance while keeping it protected from direct access.
- Encapsulation helps to maintain the integrity of the data and ensures that the internal representation of an object is hidden from the outside. This allows for better modularity and makes it easier to change the implementation without affecting other parts of the code that rely on the class.
- Encapsulation also promotes code maintainability and readability by clearly defining the interface through which the class can be interacted with, while keeping the internal workings hidden and protected from unintended interference.

### Abstraction
- Abstraction is the concept of hiding the complex implementation details of a system and exposing only the necessary and relevant parts to the user. It allows developers to focus on what an object does rather than how it does it. In Python, abstraction can be achieved using abstract classes and interfaces, which define a common interface for a group of related classes without providing a complete implementation.
- For example, an `Animal` abstract class might define an abstract method `make_sound()`, which must be implemented by any subclass (like `Dog` or `Cat`). The user of the `Animal` class can call the `make_sound()` method without needing to know the specific implementation details of how each animal makes its sound.
- Abstraction helps to reduce complexity and allows for better code organization by separating the interface from the implementation. It also promotes code reusability and flexibility, as changes to the implementation of a class do not affect the code that uses the class, as long as the interface remains consistent.