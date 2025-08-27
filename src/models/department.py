import peewee
from database import db

class Department(peewee.Model):
    """
    Represents a department in the database.
    
    Fields:
        - initials (str): Unique initials for the department.
        - name (str): Full name of the department.
        - description (str): Description of the department.
    """
    initials = peewee.CharField(unique=True)
    name = peewee.CharField()
    description = peewee.TextField(null=True)

    class Meta:
        database = db

