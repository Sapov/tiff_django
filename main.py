import hashlib


def calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


print(calculate_signature('ddd', 234, 'sasha'))
