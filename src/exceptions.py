from fastapi import HTTPException

class TodoError(HTTPException):
    """Base exception for todo-related errors"""
    pass

class TodoNotFoundError(TodoError):
    def __init__(self, todo_id=None):
        message = "Todo not found" if todo_id is None else f"Todo with id {todo_id} not found"
        super().__init__(status_code=404, detail=message)

class TodoCreationError(TodoError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create todo: {error}")

class UserError(HTTPException):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)

class PasswordMismatchError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="New passwords do not match")

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=401, detail="Current password is incorrect")

class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Could not validate user"):
        super().__init__(status_code=401, detail=message)

# Patient-related exceptions
class PatientError(HTTPException):
    """Base exception for patient-related errors"""
    pass

class PatientNotFoundError(PatientError):
    def __init__(self, patient_id=None):
        message = "Patient not found" if patient_id is None else f"Patient with id {patient_id} not found"
        super().__init__(status_code=404, detail=message)

class PatientCreationError(PatientError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create patient: {error}")

# Test Result-related exceptions
class TestResultError(HTTPException):
    """Base exception for test result-related errors"""
    pass

class TestResultNotFoundError(TestResultError):
    def __init__(self, result_id=None):
        message = "Test result not found" if result_id is None else f"Test result with id {result_id} not found"
        super().__init__(status_code=404, detail=message)

class TestResultCreationError(TestResultError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create test result: {error}")

# Clinic-related exceptions
class ClinicError(HTTPException):
    """Base exception for clinic-related errors"""
    pass

class ClinicNotFoundError(ClinicError):
    def __init__(self, clinic_id=None):
        message = "Clinic not found" if clinic_id is None else f"Clinic with id {clinic_id} not found"
        super().__init__(status_code=404, detail=message)

class ClinicCreationError(ClinicError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create clinic: {error}")
