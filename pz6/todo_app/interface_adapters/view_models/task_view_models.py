from dataclasses import dataclass

@dataclass
class TaskViewModel:
    id: str
    title: str
    status: str
    message: str

@dataclass
class ErrorViewModel:
    success: bool
    error_code: str
    message: str
    