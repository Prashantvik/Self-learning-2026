### Day 1 Checkpoint :  Python Execution Model, Namespaces, Scope (LEGB), Mutability

#### Q1. What is the difference between a namespace and a scope in Python?  
A1. Good intuition. The sharper version to lock in:
Namespace = a dictionary mapping names → objects ({'x': 42, 'foo': <function>})
Scope = the visibility rule that determines which namespaces Python searches, and in what order (LEGB)
One namespace can be searched by multiple scopes. The global namespace is searched both from global scope and as a fallback from local scope. They're related but distinct — namespace is the storage, scope is the search rule.

#### Q2. Why does Python's mutable default argument bug happen — what's the underlying memory model reason?  
A2. You got the core idea. The precise version to internalize:
Default argument objects are created once at function definition time and stored in function.__defaults__. They are not recreated per call. So a mutable default is the same object every call — mutations accumulate on it.

#### Q3. If a function reads a global variable but never uses the global keyword, can it modify that variable? What happens if it tries?  
A3. The rule is:  
    * Read a global → works fine, no keyword needed    
    * Assign to a global → Python creates a new local variable instead, silently  
    * Modify in place (like x += 1) → UnboundLocalError because Python commits to treating x as local (due to the assignment) before it's been defined locally  

The global keyword tells Python: "when I assign to this name, write to the global frame's dictionary, not a new local one.

```
x = 10

def foo():
    print(x)   # READING a global — always works, no keyword needed

def bar():
    x = 99     # Creates a LOCAL x — does NOT touch the global x

def baz():
    x += 1     # UnboundLocalError — Python sees the assignment
               # treats x as local, but it hasn't been assigned yet locally
```

#### LEGB = Local → Enclosing → Global → Built-in. 
You search your desk before the archive.  
* L → Local       (your desk — inside the current function)
* E → Enclosing   (your manager's desk — outer function, if nested)
* G → Global      (department cabinet — module level)
* B → Built-in    (company archive — len, print, range, etc.)

And for mutability: "Variables are nametags, not boxes. Two nametags can hang on the same object.

#### Before any line runs, Python does two things:  
* Compiles your .py file to bytecode (.pyc) — checks syntax, identifies all names.  
* Executes that bytecode in the CPython interpreter  

---

### Day 2 Checkpoint : Functions Deep Dive: First-Class Functions, Closures, *args/**kwargs
* The analogy: Functions as physical objects you can hand around, in python function is an object.  
* "First-class" means: functions can be passed as arguments, returned from other functions, stored in variables and data structures — everything you can do with an integer or string.  


#### Closures — the important one  
* A closure is a function that remembers the environment it was defined in, even after that environment no longer exists.  
```
def make_multiplier(factor):
    def multiply(n):         # inner function
        return n * factor    # 'factor' is from enclosing scope
    return multiply          # return the function object itself

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))    # 10
print(triple(5))    # 15
```