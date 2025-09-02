import peewee
from database import db
from datetime import datetime
from models.department import Department
import uuid

class Employee(peewee.Model):
    """
    Represents an employee in the database.

    Fields:
        - id (str): Randomized UUID primary key for uniqueness.
        - employee_id (str): Unique identifier for the employee.
        - first_name (str): Employee's first name.
        - middle_name (str): Employee's middle name.
        - last_name (str): Employee's last name.
        - initials (str): Employee's initials.
        - department (ForeignKey): Link to the Department model.
        - qr_code (str): Unique string for QR code login.
        - created_at (datetime): Timestamp of creation.
        - updated_at (datetime): Timestamp of the last update.
    """
    id = peewee.CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = peewee.CharField(unique=True)
    first_name = peewee.CharField()
    middle_name = peewee.CharField(null=True)
    last_name = peewee.CharField()
    initials = peewee.CharField(null=True)
    department = peewee.ForeignKeyField(Department, backref='employees')
    qr_code = peewee.CharField(unique=True)
    created_at = peewee.DateTimeField(default=datetime.now)
    updated_at = peewee.DateTimeField(null=True)

    class Meta:
        database = db

