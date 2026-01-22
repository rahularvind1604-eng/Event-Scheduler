class AppError(Exception):
    def __init__(self, message: str, error_code: str = "APP_ERROR"):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class NotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message, "NOT_FOUND")


class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message, "CONFLICT")


class ValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")
