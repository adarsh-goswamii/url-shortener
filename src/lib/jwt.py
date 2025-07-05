import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from typing import Optional, Dict
from datetime import datetime, timedelta

from src.configs.env import get_settings
from src.exceptions.errors import JWTValidationResult

configs = get_settings()

class JWTManager:
    def __init__(
        self,
        # private_key: Optional[str] = None,
        algorithm: str = "RS256"
    ):
        self.algorithm = algorithm
        self.public_key = configs.jwt_public_key
        # self.private_key = private_key

    # def generate_token(self, payload: Dict, expires_in: int = 3600) -> str:
    #     """
    #     Generate a JWT using the private key.
    #     """
    #     if not self.private_key:
    #         raise ValueError("Private key not provided. Cannot generate token.")
    #
    #     payload = {
    #         **payload,
    #         "iat": datetime.utcnow(),
    #         "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    #     }
    #
    #     token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
    #     return token

    def verify_token(self, token: str, verify_exp: bool = True) -> JWTValidationResult:
        """
        Verifies JWT and returns a structured result for controller logic.
        """
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=[self.algorithm],
                options={"verify_exp": verify_exp}
            )
            return JWTValidationResult(valid=True, payload=payload)

        except ExpiredSignatureError:
            return JWTValidationResult(valid=False, error="expired")

        except InvalidTokenError as e:
            return JWTValidationResult(valid=False, error=f"invalid: {str(e)}")

jwt_manager = JWTManager()