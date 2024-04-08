from cryptography.fernet import Fernet
import uuid


def generate_key() -> bytes:
    """
    Generates a key for encryption/decryption.
    """
    return Fernet.generate_key()


def encrypt_token(key: bytes):
    """
    Generates a unique UUID and encrypts it using the provided key.

    Parameters:
    - key: A bytes object representing the encryption key.

    Returns:
    - A tuple containing the encrypted token and the original UUID.
    """
    # Generate a unique UUID
    token = str(uuid.uuid4())

    # Initialize Fernet with the provided key
    f = Fernet(key)

    # Encrypt the UUID
    encrypted_token = f.encrypt(token.encode())

    return encrypted_token, token


def decrypt_token(encrypted_token: bytes, key) -> str:
    """
    Decrypts an encrypted token using the provided key.

    Parameters:
    - encrypted_token: The encrypted token as bytes.
    - key: A bytes object representing the encryption key.

    Returns:
    - The decrypted token as a string.
    """
    # Initialize Fernet with the provided key
    f = Fernet(key)

    # Decrypt the token
    decrypted_token = f.decrypt(encrypted_token).decode()

    return decrypted_token


# # # # Example usage
# key = generate_key()
# encrypted_token, original_token = encrypt_token(key)
# print(f"Encryption Key: {key}", type(key))
# print(f"Encrypted Token: {encrypted_token}", type(encrypted_token))
# print(f"Original Token: {original_token}", type(original_token))
#
# decrypted_token = decrypt_token(encrypted_token, key)
# print(f"Decrypted Token: {decrypted_token}")
#
#
# import base64
# encrypted_token_bytes = base64.urlsafe_b64decode(encrypted_token).decode()
# key_bytes = base64.urlsafe_b64decode(key).decode()
# print(type(encrypted_token_bytes))
# print(type(key_bytes))
# print(encrypted_token_bytes)
# print(key_bytes)

# decrypted_token_str = decrypt_token(encrypted_token_str, key_str)
# print(decrypted_token_str)

