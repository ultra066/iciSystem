import peewee
from database import db
from datetime import datetime
from models.department import Department

class Employee(peewee.Model):
    """
    Represents an employee in the database.
    
    Fields:
        - employee_id (str): Unique identifier for the employee.
        - name (str): Employee's full name.
        - initials (str): Employee's initials.
        - department (ForeignKey): Link to the Department model.
        - qr_code (str): Unique string for QR code login.
        - created_at (datetime): Timestamp of creation.
        - updated_at (datetime): Timestamp of the last update.
    """
    employee_id = peewee.CharField(unique=True)
    name = peewee.CharField()
    initials = peewee.CharField(null=True)
    department = peewee.ForeignKeyField(Department, backref='employees')
    qr_code = peewee.CharField(unique=True)
    created_at = peewee.DateTimeField(default=datetime.now)
    updated_at = peewee.DateTimeField(null=True)

    class Meta:
        database = db

