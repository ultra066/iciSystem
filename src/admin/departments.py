import flet as ft
from database import db
from models.department import Department
from components.navigation import AdminNavigation
from components.header import AdminHeader

class AdminDepartmentsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/departments"
        self.page.bgcolor = "#F0F2F5"
        
        self.add_department_dialog = self.create_add_department_dialog()
        
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
                                AdminHeader("Department Management"),
                                ft.Divider(height=20),
                                ft.Row(
                                    [
                                        ft.TextField(hint_text="Search Department", expand=True),
                                        ft.ElevatedButton(text="Add New Department", on_click=self.open_add_department_dialog),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Container(
                                    content=ft.ListView(
                                        [self.create_departments_table()],
                                        height=400,
                                        auto_scroll=True,
                                    ),
                                ),
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
        
    def create_add_department_dialog(self):
        self.name_field = ft.TextField(label="Department Name")
        self.initials_field = ft.TextField(label="Initials (e.g., HR, IT)")
        
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("Add New Department"),
            content=ft.Column(
                [
                    self.name_field,
                    self.initials_field,
                ]
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.ElevatedButton("Add", on_click=self.add_department)
            ]
        )

    def create_departments_table(self):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Initials")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[]
        )

    def did_mount(self):
        self.load_departments_data()

    def load_departments_data(self):
        db.connect()
        all_departments = Department.select().order_by(Department.name)
        
        # Access the table correctly - it's now in a Container
        table = self.controls[0].controls[1].content.controls[3]
        table.rows.clear()
        
        for dept in all_departments:
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(dept.name)),
                        ft.DataCell(ft.Text(dept.initials)),
                        ft.DataCell(ft.Row([
                            ft.IconButton(ft.Icons.EDIT, tooltip="Edit"),
                            ft.IconButton(ft.Icons.DELETE, tooltip="Delete")
                        ])),
                    ]
                )
            )
        
        db.close()
        self.page.update()

    def open_add_department_dialog(self, e):
        self.page.dialog = self.add_department_dialog
        self.add_department_dialog.open = True
        self.page.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

    def add_department(self, e):
        db.connect()
        try:
            name = self.name_field.value
            initials = self.initials_field.value
            
            if not name or not initials:
                self.page.snack_bar = ft.SnackBar(ft.Text("Please fill all fields."), open=True)
                self.page.update()
                return

            Department.create(name=name, initials=initials)
            self.close_dialog(e)
            self.load_departments_data()
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Department {name} added."), open=True)
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
        finally:
            db.close()
        self.page.update()
