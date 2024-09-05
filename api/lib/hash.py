from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

class Hash:
    @staticmethod
    def hash_generator(data: str):
        hash_object = hashlib.sha256(data.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig
        
    @staticmethod
    def _bcrypt(password: str):        
        return generate_password_hash(password)


    @staticmethod
    def _verify(plain_password: str, hashed_password: str):        
        return check_password_hash(hashed_password, plain_password)