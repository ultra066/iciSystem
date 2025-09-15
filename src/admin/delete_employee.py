import flet as ft
from database import db
from models.employee import Employee
from components.admin_layout import AdminLayout
from components.header import AdminHeader

class AdminDeleteEmployeeView(ft.View):
    def __init__(self, page: ft.Page, emp_id):
        super().__init__()
        self.page = page
        self.emp_id = emp_id
        self.route = "/admin/employees/delete"
        self.page.bgcolor = "#F0F2F5"

        # Load employee
        if not db.is_connection_usable():
            db.connect()
        self.employee = Employee.get_by_id(self.emp_id)
        if db.is_connection_usable():
            db.close()

        self.controls = [
            AdminLayout(
                page=self.page,
                main_content=ft.Column(
                    [
                        AdminHeader("DELETE EMPLOYEE"),
                        ft.Divider(height=20),
                        ft.Text(f"Are you sure you want to delete employee: {self.employee.first_name} {self.employee.last_name}?"),
                        ft.Row(
                            [
                                ft.ElevatedButton("Delete", bgcolor="red", on_click=self.delete_employee),
                                ft.TextButton("Cancel", on_click=self.cancel_delete),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            spacing=10
                        )
                    ],
                    spacing=20,
                    expand=True,
                )
            )
        ]

    def delete_employee(self, e):
        if not db.is_connection_usable():
            db.connect()
        emp = Employee.get_by_id(self.emp_id)
        emp.delete_instance()
        if db.is_connection_usable():
            db.close()
        self.page.go("/admin/employees")

    def cancel_delete(self, e):
        self.page.go("/admin/employees")
