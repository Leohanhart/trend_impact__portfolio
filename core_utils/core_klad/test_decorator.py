# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 14:28:05 2023

@author: Gebruiker
"""


def variable_printer_decorator(func):
    def wrapper(*args, **kwargs):
        print("Received arguments:")
        print("Positional arguments:", args)
        print("Keyword arguments:", kwargs)
        return func(*args, **kwargs)

    return wrapper


@variable_printer_decorator
def example_function(a, b, c=0):
    print("Inside the function")
    return a + b + c


# Call the decorated function
result = example_function(1, 2, c=3)
print("Result:", result)
