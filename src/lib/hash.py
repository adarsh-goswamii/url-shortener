from src.configs.env import get_settings


class HashEncoder:
    BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, secret_key: int):
        self.secret_key = secret_key
        self.base = len(self.BASE62_ALPHABET)

    def encode(self, num: int) -> str:
        """XOR the number with secret_key and Base62-encode the result."""
        obfuscated = num ^ self.secret_key
        return self._base62_encode(obfuscated)

    def decode(self, encoded: str) -> int:
        """Decode Base62, then XOR with secret_key to get original number."""
        obfuscated = self._base62_decode(encoded)
        return obfuscated ^ self.secret_key

    def _base62_encode(self, num: int) -> str:
        if num == 0:
            return self.BASE62_ALPHABET[0]
        result = []
        while num > 0:
            num, rem = divmod(num, self.base)
            result.append(self.BASE62_ALPHABET[rem])
        return ''.join(reversed(result))

    def _base62_decode(self, encoded: str) -> int:
        num = 0
        for char in encoded:
            num = num * self.base + self.BASE62_ALPHABET.index(char)
        return num

configs = get_settings()
hash = HashEncoder(configs.hash_secret_key)