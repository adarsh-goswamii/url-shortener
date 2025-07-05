from typing import Optional, Dict, Any, Union

class JWTValidationResult:
    def __init__(self, valid: bool, payload: Optional[Dict] = None, error: Optional[str] = None):
        self.valid = valid
        self.payload = payload
        self.error = error

class ApiResponseResult:
    def __init__(
        self,
        success: bool,
        data: Optional[Union[Dict, Any]] = None,
        error: Optional[Union[str, Dict[str, Any]]] = None,
        message: Optional[str] = None,
    ):
        self.success = success
        self.data = data
        self.error = error
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "message": self.message,
        }