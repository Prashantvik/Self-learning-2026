### Good Reference : 
https://realpython.com/ref/glossary/generator-expression/

### Object-Oriented Programming (OOP) Concepts

#### Good Reference : https://www.youtube.com/watch?v=Mf2RdpEiXjU
#### Default Reference : https://www.youtube.com/@coreyms
#### End to end : https://medium.com/@aserdargun/advanced-oop-in-python-a5f6130da291

## Class and Object
- **Class**: A blueprint for creating objects. It defines a set of attributes and methods that the created objects will have. For example, a `Car` class might have attributes like `make`, `model`, and `year`, and methods like `start_engine()` and `stop_engine()`.
- **Object**: An instance of a class. It is a specific realization of the class with actual values for the attributes. For example, an object of the `Car` class could be `my_car = Car(make='Toyota', model='Corolla', year=2020)`

## Class Methods and Static Methods
- **Class Methods**: These methods are bound to the class and not the instance of the class. They can modify the class state that applies across all instances of the class. They are defined using the `@classmethod` decorator and take `cls` as the first parameter.
- **Static Methods**: These methods are not bound to the class or instance. They do not modify class or instance state. They are defined using the `@staticmethod` decorator and do not take `self` or `cls` as a parameter.

## Self Parameter
- The `self` parameter in Python is a reference to the current instance of the class. It is used to access variables that belong to the class. It must be the first parameter of any method in the class, and it allows you to access attributes and methods of the instance. 
- For example, in a method defined as `def start_engine(self):`, you can access the instance's attributes using `self.attribute_name`.
- The `self` parameter is not a keyword in Python, but it is a strong convention that should be followed to maintain code readability and consistency.

## Inheritance
Inheritance is a fundamental concept in object-oriented programming (OOP) that allows a new class (called a child or subclass) to inherit properties and behaviors (attributes and methods) from an existing class (called a parent or superclass). This promotes code reusability and establishes a natural hierarchical relationship between classes.

## Inheritance vs Composition: A Real-Life Example
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

* no cheese | extra bacon | gluten-free bun | vegan patty
You’d need **hundreds of subclasses**. Chaos.

---
### Composition way (how real life actually works)

A burger is **made of parts**:

* Bun, Patty, Cheese, Bacon, Sauce
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

## Python Execution Model — Interpreted, Bytecode, CPython (End-to-End)
Source Code → Bytecode → Python Virtual Machine → Machine Code (via C runtime)

**• Execution overview:**
Python does not run source code directly. A `.py` file is first parsed, compiled into platform-independent bytecode, and then executed by the Python Virtual Machine (PVM). The PVM runs inside the Python interpreter.

**• Parsing & AST:**
Before compilation, Python checks syntax and converts code into an Abstract Syntax Tree (AST), an internal representation of program structure. Syntax errors are detected at this stage.

**• Bytecode compilation:**
Python compiles the AST into bytecode (`.pyc` files stored in `__pycache__`). Bytecode is low-level, platform-independent instructions designed for the PVM. This compilation happens automatically.

**• Python Virtual Machine (PVM):**
The PVM interprets bytecode instruction by instruction at runtime. It manages execution stack, function calls, objects, and control flow. Think of it as the runtime engine of Python.

**• CPython:**
CPython is the standard and most widely used Python implementation. It is written in C, and its PVM executes bytecode while interacting with the OS and hardware through C.

**• Interpreted vs Compiled:**
Python is both compiled and interpreted — compiled to bytecode, then interpreted by the PVM. It is not compiled ahead-of-time to native machine code like C/C++.

**• `.pyc` files:**
Compiled bytecode is cached as `.pyc` files to speed up subsequent runs. They are automatically regenerated if the source code changes and can be safely deleted.

**• Performance note:**
Python is slower than languages like C/C++ because execution goes through an interpreter, uses dynamic typing, and has higher object and memory management overhead.

## Generator expression
A generator expression is a concise expression that lets you construct a generator iterator without the need for a function. Generator expressions are similar to list comprehensions, but instead of creating a list and holding the entire data in memory, it returns a generator iterator that produces items on demand. They’re useful when you’re dealing with large datasets or potentially infinite data streams.

> squares = (x**2 for x in range(5))  
> print(squares)  
 returns -- <generator object <genexpr> at 0x102e3acf0>  
> for square in squares:  
...     print(square)

## Generator Expressions — Real-World Uses (Concise Notes)

• Large file processing: Used to read and process big files (logs, CSVs) line by line without loading the entire file into memory.  
```
error_count = sum(1 for line in open("app.log") if "ERROR" in line)  
Reads line-by-line, not the whole file — critical for GB/TB-scale data.
```

• Streaming data / ETL pipelines: Helpful for transforming data in stages while keeping memory usage low, especially in data engineering workflows.

• Memory-efficient aggregations: Ideal when computing results like sum, max, min, any, or all without needing to store intermediate lists.

• Lazy evaluation / early exit: Works efficiently with functions like any() and all() because evaluation stops as soon as the result is determined.

• Real-time or continuous data: Suitable for sensor data, event streams, or any continuously generated input where values are consumed once.


## Default Arguments Pitfalls

Mutable default arguments are evaluated once at function definition time and shared across calls, which can unintentionally preserve state; use None as a safe default instead.  
```
def add_item(x, items=[]):
    items.append(x)
    return items

Calling repeatedly accumulates values in the same list.
```

## Positional-only arguments
Parameters that must be passed by position (not keyword), defined using / in the function signature, primarily to preserve API stability and prevent name-based coupling

```
def func(a, b, /, c, d):
    pass
Here, a and b must be positional; c and d can be positional or keyword.  

func(a=1, b=2, c=3, d=4)  # Error
Passing positional-only parameters by name raises an error.
```

## Keyword-only Arguments in Python

Keyword-only arguments are parameters that must be passed using their names, not by position.

They are defined by placing `*` before them in the function signature.

### Syntax

def func(a, b, *, c, d):

- a, b → positional or keyword
- c, d → keyword-only

### Purpose

- Improves readability
- Prevents argument order bugs
- Makes APIs explicit
- Enables safe evolution of function signatures
- Important for production-quality code

### Example

def read_data(bucket, key, *, retries=3, timeout=30):
    pass

Valid call:

read_data("raw-bucket", "events.json", retries=5, timeout=60)

Invalid call:

read_data("raw-bucket", "events.json", 5, 60)

### Required Keyword-only Argument

def upload(file, *, destination):
    pass

Must be called as:

upload("data.csv", destination="s3://bucket/path")

### Optional Keyword-only Argument

def upload(file, *, destination, compress=False):
    pass

### Forcing All Arguments to be Keyword-only

def configure(*, repassgion, role):
    pass

## *args and **kwargs in Python

These allow functions to accept a variable number of arguments.

- *args → variable positional arguments (tuple)
- **kwargs → variable keyword arguments (dictionary)

### *args — Variable Positional Arguments

Collects extra positional arguments into a tuple.

Example:

def sum_numbers(*args):
    return sum(args)

Call:

sum_numbers(1, 2, 3, 4)

Inside function:
args == (1, 2, 3, 4)

### **kwargs — Variable Keyword Arguments

Collects extra named arguments into a dictionary.

Example:

def print_config(**kwargs):
    for k, v in kwargs.items():
        print(k, v)

Call:

print_config(host="db", port=5432)

Inside function:
kwargs == {"host": "db", "port": 5432}

### Using Both Together

def func(*args, **kwargs):
    pass

args → tuple of positional arguments  
kwargs → dict of named arguments  

### Parameter Order

positional → *args → keyword-only → **kwargs

Example:

def func(a, b, *args, c=10, **kwargs):
    pass

### Argument Unpacking

Use * to unpack iterables into positional arguments.

nums = [1, 2, 3]
sum_numbers(*nums)

Use ** to unpack dictionaries into keyword arguments.

config = {"host": "db", "port": 5432}
connect_db(**config)

### Common Uses in Production

- Wrappers and decorators
- Forwarding arguments
- Flexible APIs
- Configuration-heavy functions
- Library and framework development

## Lambda Functions in Python

A lambda function is a small anonymous function defined using the `lambda` keyword.

- No name
- Single expression only
- Automatically returns the expression result
- Used for short, one-time logic

### Syntax

lambda arguments: expression

Equivalent to:

def func(arguments):
    return expression

### Example

add = lambda a, b: a + b
add(2, 3)  # 5

### Common Use — Sorting

records = [("user1", 100), ("user2", 50)]

sorted(records, key=lambda r: r[1])

### With map()

nums = [1, 2, 3]
list(map(lambda x: x * x, nums))

### With filter()

nums = [1, 2, 3, 4]
list(filter(lambda x: x % 2 == 0, nums))

### Limitations

Lambda can contain only a single expression.

Not allowed:

- assignments
- loops
- multiple statements
- return keyword
- try/except

### Closure Behavior

Lambdas capture variables from surrounding scope.

Late binding pitfall:

funcs = []
for i in range(3):
    funcs.append(lambda: i)

Result of calling all functions:
[2, 2, 2]

Fix:

funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)

Result:
[0, 1, 2]

### Typical Use Cases

- Sorting with key functions
- Short transformations
- Functional operations (map, filter)
- Small callbacks
- Data manipulation tasks
