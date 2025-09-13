import flet as ft
from database import db
from models.employee import Employee
from models.department import Department
from components.admin_layout import AdminLayout
from components.header import AdminHeader

class AdminEditEmployeeView(ft.View):
    def __init__(self, page: ft.Page, emp_id):
        super().__init__()
        self.page = page
        self.emp_id = emp_id
        self.route = "/admin/employees/edit"
        self.page.bgcolor = "#F0F2F5"

        # Load employee
        if not db.is_connection_usable():
            db.connect()
        self.employee = Employee.get_by_id(self.emp_id)
        departments = Department.select()
        self.department_options = [ft.dropdown.Option(key=dept.id, text=dept.name) for dept in departments]
        if db.is_connection_usable():
            db.close()

        # Create form fields
        self.first_name_field = ft.TextField(label="First Name", value=self.employee.first_name)
        self.middle_name_field = ft.TextField(label="Middle Name", value=self.employee.middle_name or "")
        self.last_name_field = ft.TextField(label="Last Name", value=self.employee.last_name)
        self.department_dropdown = ft.Dropdown(
            label="Department",
            options=self.department_options,
            value=self.employee.department.id
        )

        self.controls = [
            AdminLayout(
                page=self.page,
                main_content=ft.Column(
                    [
                        AdminHeader("EDIT EMPLOYEE"),
                        ft.Divider(height=20),
                        ft.Column(
                            [
                                self.first_name_field,
                                self.middle_name_field,
                                self.last_name_field,
                                self.department_dropdown,
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Save", on_click=self.save_employee),
                                        ft.TextButton("Cancel", on_click=self.cancel_edit),
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ],
                            spacing=20
                        )
                    ],
                    expand=True,
                )
            )
        ]

    def save_employee(self, e):
        if not db.is_connection_usable():
            db.connect()
        emp = Employee.get_by_id(self.emp_id)
        emp.first_name = self.first_name_field.value
        emp.middle_name = self.middle_name_field.value if self.middle_name_field.value else None
        emp.last_name = self.last_name_field.value
        emp.department = Department.get_by_id(self.department_dropdown.value)
        emp.save()
        if db.is_connection_usable():
            db.close()
        self.page.go("/admin/employees")

    def cancel_edit(self, e):
        self.page.go("/admin/employees")
