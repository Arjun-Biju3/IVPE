import uuid
import hashlib

#function to generate security key
def generate_unique_key(param1, param2):
    str_param1 = str(param1)
    str_param2 = str(param2)
    combined = str_param1 + str_param2
    unique_key = uuid.uuid5(uuid.NAMESPACE_DNS, combined)
    short_key = str(unique_key)[:8]
    return short_key

# Example usage
param1 = "example1"
param2 = 789
key = generate_unique_key(param1, param2)
print(key)

#function to generate vote key
def generate_unique_key(param1, param2):
    str_param1 = str(param1)
    str_param2 = str(param2)
    combined = str_param1 + str_param2
    hash_object = hashlib.sha256(combined.encode())
    key = hash_object.hexdigest()
    unique_key=key[:10]
    return unique_key

# Example usage
param1 = "user123"
param2 = 456
key = generate_unique_key(param1, param2)
print(key)

