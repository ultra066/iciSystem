import peewee
from database import db
from datetime import datetime
from models.employee import Employee

class Attendance(peewee.Model):
    """
    Represents an attendance record in the database.
    
    Fields:
        - employee (ForeignKey): Link to the Employee model.
        - time_in (datetime): Timestamp when the employee clocked in.
        - time_out (datetime): Timestamp when the employee clocked out.
        - date (date): The date of the attendance record.
        - status (str): The attendance status (e.g., 'Present', 'Late').
    """
    employee = peewee.ForeignKeyField(Employee, backref='attendance')
    time_in = peewee.DateTimeField(null=True)
    time_out = peewee.DateTimeField(null=True)
    date = peewee.DateField()
    status = peewee.CharField()

    class Meta:
        database = db

