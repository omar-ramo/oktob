from random import choice
def get_random_string(length=2, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'):
    """
    Returns a generated random string.
    The default length of 2 with the a-z, A-Z, 0-9 character set.
    """
    return ''.join(choice(allowed_chars) for i in range(length))