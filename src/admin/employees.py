import flet as ft
from database import db
from models.employee import Employee
from models.department import Department
from components.admin_layout import AdminLayout
from components.header import AdminHeader
from utils import generate_unique_employee_id, get_initials
import qrcode
import os

class AdminEmployeesView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/employees"
        self.page.bgcolor = "#F0F2F5"

        # Create the employees table
        self.employees_table = self.create_employees_table()

        self.controls = [
            AdminLayout(
                page=self.page,
                main_content=ft.Column(
                    [
                        AdminHeader("EMPLOYEES"),
                        ft.Divider(height=20),
                        ft.TextField(hint_text="Search Employee", expand=True),
                        self.employees_table,
                    ],
                    expand=True,
                )
            )
        ]



    def create_employees_table(self):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Initials")),
                ft.DataColumn(ft.Text("Department")),
                ft.DataColumn(ft.Text("QR Code")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[]
        )

    def did_mount(self):
        self.load_employees_data()

    def load_employees_data(self):
        if not db.is_connection_usable():
            db.connect()
        all_employees = Employee.select().order_by(Employee.last_name)

        # Access the table correctly
        self.employees_table.rows.clear()

        for emp in all_employees:
            full_name = f"{emp.first_name} {emp.middle_name + ' ' if emp.middle_name else ''}{emp.last_name}"
            self.employees_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(full_name)),
                        ft.DataCell(ft.Text(emp.initials if emp.initials else "")),
                        ft.DataCell(ft.Text(emp.department.name)),
                        ft.DataCell(ft.ElevatedButton("View QR", on_click=lambda e, qr_code=emp.qr_code: self.show_qr_code(e, qr_code))),
                        ft.DataCell(ft.Row([
                            ft.IconButton(ft.Icons.EDIT, tooltip="Edit"),
                            ft.IconButton(ft.Icons.DELETE, tooltip="Delete")
                        ])),
                    ]
                )
            )

        if db.is_connection_usable():
            db.close()
        self.page.update()


        
    def show_qr_code(self, e, qr_code):
        qr_path = os.path.join("qr_codes", f"{qr_code}.png")

        qr_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Employee QR Code"),
            content=ft.Column(
                [
                    ft.Text(f"Scan this QR code to log in.", size=16),
                    ft.Image(src=qr_path, width=250, height=250),
                    ft.ElevatedButton("Close", on_click=lambda e: self.close_qr_dialog(e))
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.page.dialog = qr_dialog
        qr_dialog.open = True
        self.page.update()

    def close_qr_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()
