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

        # Initialize employees data
        self.all_employees = []

        # Create the search field
        self.search_field = ft.TextField(
            hint_text="Search Employee",
            on_change=self.filter_employees,
            expand=True,
        )

        # Create the employees table
        self.employees_table = self.create_employees_table()

        self.controls = [
            AdminLayout(
                page=self.page,
                main_content=ft.Column(
                    [
                        AdminHeader("EMPLOYEES"),
                        ft.Divider(height=20),
                        ft.Container(
                            content=self.search_field,
                            padding=ft.padding.symmetric(horizontal=10, vertical=10),
                        ),
                        ft.Container(
                            content=ft.ListView(
                                [self.employees_table],
                                height=400,
                                auto_scroll=True,
                            ),
                        ),
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
        self.all_employees = list(Employee.select().order_by(Employee.last_name))
        if db.is_connection_usable():
            db.close()
        self.populate_table(self.all_employees)

    def populate_table(self, employees_list):
        self.employees_table.rows.clear()
        for emp in employees_list:
            full_name = f"{emp.first_name} {emp.middle_name + ' ' if emp.middle_name else ''}{emp.last_name}"
            self.employees_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(full_name)),
                        ft.DataCell(ft.Text(emp.initials if emp.initials else "")),
                        ft.DataCell(ft.Text(emp.department.name)),
                        ft.DataCell(ft.ElevatedButton("View QR", on_click=lambda e, qr_code=emp.qr_code: self.show_qr_code(e, qr_code))),
                        ft.DataCell(ft.Row([
                            ft.IconButton(ft.Icons.EDIT, tooltip="Edit", on_click=lambda e, emp_id=emp.id: self.edit_employee(e, emp_id)),
                            ft.IconButton(ft.Icons.DELETE, tooltip="Delete", on_click=lambda e, emp_id=emp.id: self.delete_employee(e, emp_id))
                        ])),
                    ]
                )
            )
        self.page.update()

    def filter_employees(self, e):
        search_term = self.search_field.value.lower()
        if search_term:
            filtered_employees = [emp for emp in self.all_employees
                                  if search_term in f"{emp.first_name} {emp.middle_name + ' ' if emp.middle_name else ''}{emp.last_name}".lower()
                                  or search_term in (emp.initials or "").lower()
                                  or search_term in emp.department.name.lower()]
        else:
            filtered_employees = self.all_employees
        self.populate_table(filtered_employees)


        
    def show_qr_code(self, e, qr_code):
        self.page.qr_code = qr_code
        self.page.go("/admin/employees/view_qr")

    def edit_employee(self, e, emp_id):
        self.page.edit_emp_id = emp_id
        self.page.go("/admin/employees/edit")

    def delete_employee(self, e, emp_id):
        self.page.delete_emp_id = emp_id
        self.page.go("/admin/employees/delete")


