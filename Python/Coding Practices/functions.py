def square(n):
    return n ** 2

# Store in a variable
operation = square
print(operation(5))       # 25 — same function, different name

# Store in a data structure
transforms = [square, abs, str]
print([f(-4) for f in transforms])   # [16, 4, '-4']

# Pass as an argument
def apply(func, value):
    return func(value)

print(apply(square, 7))   # 49