# Core application package
# Strict hypothesis-driven development protocol enforced

__version__ = "0.1.0"

class ValidationError(Exception):
    """Base exception for validation failures"""
    def __init__(self, message: str, hypothesis_id: str):
        super().__init__(f"[{hypothesis_id}] {message}")
        self.hypothesis_id = hypothesis_id