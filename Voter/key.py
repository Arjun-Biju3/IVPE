import uuid
import hashlib
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

#function to generate login key
def generate_log_key(param1, param2):
    str_param1 = str(param1)
    str_param2 = str(param2)
    combined = str_param1 + str_param2
    unique_key = uuid.uuid5(uuid.NAMESPACE_DNS, combined)
    short_key = str(unique_key)[:8]
    return short_key


#function to generate vote key
def generate_vote_key(param1, param2):
    str_param1 = str(param1)
    str_param2 = str(param2)
    combined = str_param1 + str_param2
    hash_object = hashlib.sha256(combined.encode())
    key = hash_object.hexdigest()
    unique_key=key[:10]
    return unique_key

#function to generate id
def generate_log_id(param1, param2):
    str_param1 = str(param1)
    str_param2 = str(param2)
    combined = str_param1 + str_param2
    unique_key = uuid.uuid5(uuid.NAMESPACE_DNS, combined)
    short_key = str(unique_key)[31:]
    return short_key

#function to add separator
def add_string_with_random_separator(base_string, add_string):
    separators = ['!', '#', '$', '%', '^', '&', '*']
    separator = random.choice(separators) 
    return base_string + separator + add_string


#AES IMPLEMENTATION

def encrypt_aes(data, key):
    if isinstance(data, str):
        data = data.encode()  # Convert string data to bytes
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad data to be a multiple of 16 bytes
    pad_length = 16 - (len(data) % 16)
    padded_data = data + bytes([pad_length] * pad_length)
    
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return IV and encrypted data concatenated
    return iv + encrypted_data

def decrypt_aes(encrypted_data, key):
    # Extract the IV from the beginning of the encrypted data
    iv = encrypted_data[:16]
    actual_encrypted_data = encrypted_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(actual_encrypted_data) + decryptor.finalize()
    
    # Remove padding
    pad_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad_length]
    
    return decrypted_data





