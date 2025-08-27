import flet as ft
from database import db
from models.attendance import Attendance
from models.employee import Employee
from components.navigation import AdminNavigation
from components.header import AdminHeader

class AdminAttendanceView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/attendance"
        self.page.bgcolor = "#F0F2F5"
        
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
                                AdminHeader("Attendance Records"),
                                ft.Divider(height=20),
                                ft.TextField(hint_text="Search by Name or Date", expand=True),
                                self.create_attendance_table(),
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

    def create_attendance_table(self):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Time-in")),
                ft.DataColumn(ft.Text("Time-out")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[]
        )

    def did_mount(self):
        self.load_attendance_data()

    def load_attendance_data(self):
        try:
            db.connect()
            # Join Attendance with Employee to get the name
            attendance_records = (Attendance.select(Attendance, Employee)
                                            .join(Employee)
                                            .order_by(Attendance.date.desc()))
            
            table = self.controls[0].controls[1].controls[2]
            table.rows.clear()
            
            for record in attendance_records:
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(record.employee.name)),
                            ft.DataCell(ft.Text(record.date.strftime("%Y-%m-%d"))),
                            ft.DataCell(ft.Text(record.time_in.strftime("%I:%M %p"))),
                            ft.DataCell(ft.Text(record.time_out.strftime("%I:%M %p") if record.time_out else "N/A")),
                            ft.DataCell(ft.Text(record.status)),
                        ]
                    )
                )
        finally:
            db.close()
            self.page.update()
