import peewee
from database import db
from datetime import datetime

class Admin(peewee.Model):
    """
    Represents an administrator user in the database.
    
    Fields:
        - username (str): Unique username for login.
        - password_hash (str): Securely hashed password.
        - created_at (datetime): Timestamp of creation.
    """
    username = peewee.CharField(unique=True)
    password_hash = peewee.CharField()
    created_at = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db

