# main.py

import flet as ft
from database import initialize_db
from auth import initialize_admin
from employee.qr_login import QRLoginView
from employee.create_account import CreateAccountView
from employee.qr_code_display import QRCodeDisplayView
from employee.dashboard import UserDashboardView
from employee.attendance import UserAttendanceView
from employee.profile import UserProfileView
from admin.dashboard import AdminDashboardView
from admin.employees import AdminEmployeesView
from admin.edit_employee import AdminEditEmployeeView
from admin.delete_employee import AdminDeleteEmployeeView
from admin.view_qr import AdminViewQRView
from admin.login import AdminLoginView
from admin.profile import AdminProfileView
from admin.timeclock import AdminAttendanceView as AdminTimeclockView

def main(page: ft.Page):
    """
    The main Flet application function.
    """
    page.title = "Attendance System"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    
    # Initialize the database and default admin user on app start
    initialize_db()
    initialize_admin()

    def route_change(route):
        page.views.clear()
        
        # User Views
        if page.route == "/":
            page.views.append(QRLoginView(page=page))
        elif page.route == "/create_account":
            page.views.append(CreateAccountView(page=page))
        elif page.route == "/qr_display":
            page.views.append(QRCodeDisplayView(page=page, employee=page.employee, qr_image_path=page.qr_image_path))
        elif page.route == "/employee/dashboard":
            page.views.append(UserDashboardView(page=page, employee=page.employee))
        elif page.route == "/employee/attendance":
            page.views.append(UserAttendanceView(page=page, employee=page.employee))
        elif page.route == "/employee/profile":
            page.views.append(UserProfileView(page=page, employee=page.employee))
        
        # Admin Views
        elif page.route == "/admin/login":
            page.views.append(AdminLoginView(page=page))
        elif page.route == "/admin/dashboard":
            page.views.append(AdminDashboardView(page=page))
        elif page.route == "/admin/employees":
            page.views.append(AdminEmployeesView(page=page))
        elif page.route == "/admin/employees/edit":
            page.views.append(AdminEditEmployeeView(page=page, emp_id=page.edit_emp_id))
        elif page.route == "/admin/employees/delete":
            page.views.append(AdminDeleteEmployeeView(page=page, emp_id=page.delete_emp_id))
        elif page.route == "/admin/employees/view_qr":
            page.views.append(AdminViewQRView(page=page))
        elif page.route == "/admin/profile":
            page.views.append(AdminProfileView(page=page))
        elif page.route == "/admin/timeclock":
            page.views.append(AdminTimeclockView(page=page))
            
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

