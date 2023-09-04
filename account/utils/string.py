import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_string = ''.join(random.choice(letters) for i in range(length))
    return result_string

def get_random_digits(lenght):
    letters = string.digits
    result_string = ''.join(random.choice(letters) for i in range(lenght))
    return result_string