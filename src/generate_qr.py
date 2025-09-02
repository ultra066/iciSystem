import sys
import os
sys.path.append('.')

from database import db
from models.employee import Employee
from qr_manager import generate_qr_code

db.connect()
try:
    emp = Employee.get(Employee.name == 'Harold Vonn Abayon Ultra')
    print(f"Employee ID: {emp.employee_id}")
    filename = f"{emp.employee_id}_qr.png"
    qr_path = os.path.join('qr_codes', filename)
    if not os.path.exists(qr_path):
        generate_qr_code(emp.qr_code, filename)
        print(f"QR code generated: {qr_path}")
    else:
        print(f"QR code already exists: {qr_path}")
except Employee.DoesNotExist:
    print("Employee not found.")
finally:
    db.close()
