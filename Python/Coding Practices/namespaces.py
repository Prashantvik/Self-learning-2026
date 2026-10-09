"""Namespaces
LEGB = Local → Enclosing → Global → Built-in. You search your desk before the archive.
L → Local       (your desk — inside the current function)
E → Enclosing   (your manager's desk — outer function, if nested)
G → Global      (department cabinet — module level)
B → Built-in    (company archive — len, print, range, etc.)

And for mutability: "Variables are nametags, not boxes. Two nametags can hang on the same object.

Before any line runs, Python does two things:

Compiles your .py file to bytecode (.pyc) — checks syntax, identifies all names
Executes that bytecode in the CPython interpreter
"""

global_var = 42
print(global_var)
print(globals())   # {'global_var': 42, '__name__': '__main__', ...}


def new_function():
    local_var = 99
    print(local_var)
    print(locals())  # {'local_var': 99}

new_function()


# Coding Practice
# Exercise 1 — Guided: LEGB scavenger hunt
x = "global"

def outer():
    x = "enclosing"

    def inner():
        # x = "local"   # try uncommenting this
        print(x)        # which x?

    inner()

outer()
print(x)                # which x?


# Exercise 2 — Semi-guided: The mutable default trap
# Questions to answer:
# Why does each call "remember" previous records?
# Answer: Because the default value for the log parameter is a mutable list, and it is created only once when the function 
# is defined. Therefore, all calls to the function share the same list object in memory.
# Where does the log default object live in memory across calls?
# Answer: The root cause you need to know: Default argument objects are evaluated once at function definition time and stored on
# the function object itself — not recreated on each call. So log=[] creates one list that lives on add_record.__defaults__.
# Fix it so each call starts with a fresh log unless one is explicitly passed in.
# Answer : Below

def add_record(record, log=[]):
    log.append(record)
    return log

print(add_record("pipeline_run_1"))
print(add_record("pipeline_run_2"))
print(add_record("pipeline_run_3"))


def add_record_new(record, log=None):   # None is immutable — safe default
    if log is None:
        log = []                    # new list created only when needed
    log.append(record)
    return log

print(add_record_new("pipeline_run_1"))
print(add_record_new("pipeline_run_2"))
print(add_record_new("pipeline_run_3"))


# Exercise 3 — Real-world mini-project: Config namespace manager
# You're building a lightweight config system for a data pipeline. Configs can be set globally, overridden per-environment, and functions should never silently mutate the global config.

# Build this system:
DEFAULT_CONFIG = {
    "batch_size": 100,
    "timeout": 30,
    "retries": 3
}

def run_pipeline(env_overrides=None):
    # Should use DEFAULT_CONFIG as base
    # Apply env_overrides on top WITHOUT mutating DEFAULT_CONFIG
    # Print the final config used for this run
    new_env_override = DEFAULT_CONFIG.copy()
    if env_overrides:
        for keys, values in env_overrides.items():
            new_env_override[keys] = env_overrides[keys]
        
    print(new_env_override)

run_pipeline({"batch_size": 500, "timeout": 60})
print("Global config unchanged:", DEFAULT_CONFIG)  # must still be original

# Idiomatic Python — dict.update() does exactly this
# new_env_override.update(env_overrides)