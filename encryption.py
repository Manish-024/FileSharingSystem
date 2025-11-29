from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os


class FileEncryption:
    """Handle file encryption and decryption"""
    
    @staticmethod
    def generate_key_from_password(password: str, salt: bytes = None) -> tuple:
        """Generate encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    @staticmethod
    def encrypt_file(file_path: str, password: str) -> tuple:
        """
        Encrypt a file with password
        Returns: (encrypted_file_path, salt)
        """
        # Generate key from password
        key, salt = FileEncryption.generate_key_from_password(password)
        cipher = Fernet(key)
        
        # Read original file
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        # Encrypt data
        encrypted_data = cipher.encrypt(file_data)
        
        # Write encrypted file
        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)
        
        return encrypted_file_path, salt
    
    @staticmethod
    def decrypt_file(encrypted_file_path: str, password: str, salt: bytes, 
                    output_path: str = None) -> str:
        """
        Decrypt a file with password
        Returns: decrypted_file_path
        """
        # Generate key from password and salt
        key, _ = FileEncryption.generate_key_from_password(password, salt)
        cipher = Fernet(key)
        
        # Read encrypted file
        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Decrypt data
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
        except Exception as e:
            raise ValueError("Invalid password or corrupted file")
        
        # Write decrypted file
        if output_path is None:
            output_path = encrypted_file_path.replace('.encrypted', '.decrypted')
        
        with open(output_path, 'wb') as file:
            file.write(decrypted_data)
        
        return output_path
    
    @staticmethod
    def verify_password(encrypted_file_path: str, password: str, salt: bytes) -> bool:
        """Verify if password is correct"""
        try:
            key, _ = FileEncryption.generate_key_from_password(password, salt)
            cipher = Fernet(key)
            
            with open(encrypted_file_path, 'rb') as file:
                encrypted_data = file.read()
            
            cipher.decrypt(encrypted_data)
            return True
        except:
            return False
