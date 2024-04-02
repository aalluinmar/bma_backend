from time import time


def generate_unique_integer_number():
    # Generate a unique 12-digit number based on the current timestamp
    return int(time() * 1000) % 1000000000000
