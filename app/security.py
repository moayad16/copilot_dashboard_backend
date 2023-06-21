import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Optional

secret_key = "your-secret-key"
algorithm = "HS256"


def create_jwt_token(username: str, expires_delta: Optional[timedelta] = None):
    to_encode = {
        "sub": username,
        "iat": datetime.utcnow(),
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def encrypt_string_sha256(string):
    # Create a SHA256 hash object
    sha256_hash = hashlib.sha256()

    # Encode the string to bytes before hashing
    encoded_string = string.encode('utf-8')

    # Update the hash object with the encoded string
    sha256_hash.update(encoded_string)

    # Get the hexadecimal representation of the hash
    encrypted_string = sha256_hash.hexdigest()

    return encrypted_string
