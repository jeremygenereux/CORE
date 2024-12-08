from datetime import datetime, timedelta
import os
import hashlib
import jwt

# Secret key to encode the JWT token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def check_password(password: str, password_hash: str) -> bool:
    return password_hash == hashlib.sha256(password.encode()).hexdigest()

# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
