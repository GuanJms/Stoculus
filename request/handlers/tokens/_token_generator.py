from utils.encryption._token_key_encrypt import encrypt_token, decrypt_token, generate_key


class TokenManager:

    @staticmethod
    def generate_token() -> tuple[str, str, str]:
        key = generate_key()
        encrypted_token, original_token = encrypt_token(key)

        key = key.decode()
        encrypted_token = encrypted_token.decode()
        return encrypted_token, key, original_token

    @staticmethod
    def decrypt_token(encrypted_token: bytes | str, key: str | bytes) -> str:

        if isinstance(key, str):
            key = key.encode()
        if isinstance(encrypted_token, str):
            encrypted_token = encrypted_token.encode()
        token = decrypt_token(encrypted_token, key)
        return token

    @classmethod
    def is_valid_token(cls, public_token: str | None, key: str | None) -> bool:
        if public_token is None or key is None:
            return False
        else:
            try:
                cls.decrypt_token(public_token, key)
                return True
            except Exception:
                return False


