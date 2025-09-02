from peewee import SqliteDatabase

# Create a single database connection object
db = SqliteDatabase('attendance.db')

def initialize_db():
    """
    Connects to the database and creates all tables.
    """
    from models.admin import Admin
    from models.department import Department
    from models.employee import Employee
    from models.attendance import Attendance

    if not db.is_connection_usable():
        db.connect()
    # Drop and recreate Employee table to apply schema changes
    if Employee.table_exists():
        Employee.drop_table()
    # Create tables if they don't exist
    db.create_tables([Admin, Department, Employee, Attendance])
    if db.is_connection_usable():
        db.close()

