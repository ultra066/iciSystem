import flet as ft
from database import db
from models.employee import Employee
from models.department import Department
from components.navigation import AdminNavigation
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

        self.add_employee_dialog = self.create_add_employee_dialog()
        
        self.controls = [
            ft.Row(
                [
                    ft.Container(
                        content=AdminNavigation(page=self.page),
                        width=250,
                        bgcolor="#263238",
                        padding=ft.padding.all(20),
                        border_radius=ft.border_radius.all(10),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                AdminHeader("Employee Management"),
                                ft.Divider(height=20),
                                ft.Row(
                                    [
                                        ft.TextField(hint_text="Search Employee", expand=True),
                                        ft.ElevatedButton(text="Add New Employee", on_click=self.open_add_employee_dialog),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                self.create_employees_table(),
                            ],
                            expand=True,
                        ),
                        padding=ft.padding.all(30),
                        expand=True
                    )
                ],
                expand=True
            )
        ]

    def create_add_employee_dialog(self):
        self.name_field = ft.TextField(label="Full Name")
        self.initials_field = ft.TextField(label="Initials", read_only=True)
        self.department_dropdown = ft.Dropdown(label="Department")
        
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("Add New Employee"),
            content=ft.Column(
                [
                    self.name_field,
                    self.initials_field,
                    self.department_dropdown,
                ]
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.ElevatedButton("Add", on_click=self.add_employee)
            ]
        )

    def create_employees_table(self):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
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
        db.connect()
        all_employees = Employee.select().order_by(Employee.name)
        
        # Access the table correctly - it's now in a Container
        table = self.controls[0].controls[1].content.controls[3]
        table.rows.clear()
        
        for emp in all_employees:
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(emp.employee_id)),
                        ft.DataCell(ft.Text(emp.name)),
                        ft.DataCell(ft.Text(emp.initials)),
                        ft.DataCell(ft.Text(emp.department.name)),
                        ft.DataCell(ft.ElevatedButton("View QR", on_click=lambda e, qr_code=emp.qr_code: self.show_qr_code(e, qr_code))),
                        ft.DataCell(ft.Row([
                            ft.IconButton(ft.Icons.EDIT, tooltip="Edit"),
                            ft.IconButton(ft.Icons.DELETE, tooltip="Delete")
                        ])),
                    ]
                )
            )
        
        db.close()
        self.page.update()

    def open_add_employee_dialog(self, e):
        db.connect()
        departments = Department.select()
        self.department_dropdown.options = [ft.dropdown.Option(d.name, value=d.id) for d in departments]
        db.close()
        
        self.page.dialog = self.add_employee_dialog
        self.add_employee_dialog.open = True
        self.page.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

    def add_employee(self, e):
        db.connect()
        try:
            name = self.name_field.value
            department_id = self.department_dropdown.value
            
            if not name or not department_id:
                self.page.snack_bar = ft.SnackBar(ft.Text("Please fill all fields."), open=True)
                self.page.update()
                return

            initials = get_initials(name)
            employee_id = generate_unique_employee_id()
            qr_code_data = employee_id

            new_employee = Employee.create(
                employee_id=employee_id,
                name=name,
                initials=initials,
                department=department_id,
                qr_code=qr_code_data
            )
            
            # Generate and save the QR code image
            img = qrcode.make(qr_code_data)
            qr_dir = "qr_codes"
            if not os.path.exists(qr_dir):
                os.makedirs(qr_dir)
            img.save(os.path.join(qr_dir, f"{qr_code_data}.png"))

            self.close_dialog(e)
            self.load_employees_data()
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Employee {name} added."), open=True)

        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
        finally:
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
                    ft.ElevatedButton("Close", on_click=self.close_dialog)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.page.dialog = qr_dialog
        qr_dialog.open = True
        self.page.update()
