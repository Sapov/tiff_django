import hashlib

# mystring = input('Enter String to hash: ')
mystring = 'san-cd:100::VvwzVpx9qWXpVX806om5'

# Предположительно по умолчанию UTF-8
hash_object = hashlib.md5(mystring.encode())
print(hash_object.hexdigest())