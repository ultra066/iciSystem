# utils.py

import uuid
from datetime import datetime

def get_initials(full_name: str) -> str:
    """
    Generates initials from a full name.
    """
    if not full_name:
        return ""
    initials_list = [name[0] for name in full_name.split() if name]
    return "".join(initials_list).upper()

def generate_unique_employee_id() -> str:
    """
    Generates a unique employee ID based on a UUID.
    """
    return str(uuid.uuid4())[:8].upper()

def get_current_time_str() -> str:
    """
    Returns the current time formatted as a string.
    """
    return datetime.now().strftime("%I:%M %p")

