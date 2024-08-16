import hashlib
import os

def hash_key_with_salt(key):
    salt = os.urandom(16)  
    key_salt = key.encode('utf-8') + salt
    hashed_key = hashlib.sha256(key_salt).hexdigest()
    return hashed_key, salt

def verify_key(key, salt, hashed_key):
    key_salt = key.encode('utf-8') + salt
    computed_hash = hashlib.sha256(key_salt).hexdigest()
    return computed_hash == hashed_key

