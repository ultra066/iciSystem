import sys
import os
import uuid
sys.path.append('.')

from database import db
from models.employee import Employee
from models.department import Department

db.connect()
try:
    # Get or create department
    department, created = Department.get_or_create(
        name='Information Technology',
        defaults={'initials': 'IT', 'description': 'Information Technology department'}
    )
    
    employee_id = str(uuid.uuid4())[:8]
    qr_code = str(uuid.uuid4())
    
    Employee.create(
        employee_id=employee_id,
        name='Harold Vonn Abayon Ultra',
        department=department,
        qr_code=qr_code
    )
    
    print(f"Employee created successfully!")
    print(f"Employee ID: {employee_id}")
    print(f"QR Code: {qr_code}")
    
except Exception as ex:
    print(f"Error creating employee: {str(ex)}")
finally:
    db.close()
