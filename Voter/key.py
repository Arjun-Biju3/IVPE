import uuid
import hashlib

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



