# auth.py

import bcrypt
from database import db
from models.admin import Admin
from config import DEFAULT_ADMIN_USER

def initialize_admin():
    """
    Initializes a default admin user if one does not exist.
    """
    db.connect()
    try:
        # Check if any admin user exists
        if not Admin.select().count():
            # Hash the default password
            password = DEFAULT_ADMIN_USER["password"].encode('utf-8')
            password_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            # Create the default admin user
            Admin.create(
                username=DEFAULT_ADMIN_USER["username"],
                password_hash=password_hash
            )
            print("Default admin user created.")
    except Exception as e:
        print(f"Error initializing admin: {e}")
    finally:
        db.close()

def check_admin_credentials(username: str, password: str) -> bool:
    """
    Verifies admin credentials.
    """
    db.connect()
    try:
        admin = Admin.get(Admin.username == username)
        return bcrypt.checkpw(password.encode('utf-8'), admin.password_hash.encode('utf-8'))
    except Admin.DoesNotExist:
        return False
    finally:
        db.close()

