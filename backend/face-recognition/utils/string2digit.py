import hashlib

def hash_string2digit(s):
    result = int(hashlib.sha256(s.encode('utf-8')).hexdigest(),16)%(10**8)
    return result