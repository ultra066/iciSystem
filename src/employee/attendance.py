import flet as ft
from database import db
from models.employee import Employee
from models.attendance import Attendance
from datetime import datetime
from components.employee_navigation import EmployeeNavigation
from components.employee_top_nav import EmployeeTopNavigation

class UserAttendanceView(ft.View):
    """
    The attendance view for an employee.
    Displays the daily time record in a table.
    """
    def __init__(self, page: ft.Page, employee: Employee):
        super().__init__()
        self.page = page
        self.employee = employee
        self.route = "/employee/attendance"
        self.page.bgcolor = "#F9F1E0"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.bgcolor = "#F9F1E0"

        self.top_nav = EmployeeTopNavigation(self.page)
        self.side_nav = EmployeeNavigation(self.page)

        # Title
        self.title = ft.Text("DAILY TIME RECORD", size=32, weight="bold", text_align=ft.TextAlign.CENTER)

        # Table for attendance records
        self.attendance_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("DATE")),
                ft.DataColumn(ft.Text("DAY")),
                ft.DataColumn(ft.Text("TIME IN")),
                ft.DataColumn(ft.Text("TIME OUT")),
            ],
            rows=[]
        )

        # Load attendance data
        self.load_attendance_data()

        main_content = ft.Column(
            [
                self.title,
                ft.Container(height=20),  # Spacer
                ft.Container(
                    content=self.attendance_table,
                    height=400,
                    scroll="auto",
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        self.controls = [
            ft.Column(
                [
                    self.top_nav,
                    ft.Row(
                        [
                            self.side_nav,
                            main_content
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    )
                ],
                expand=True
            )
        ]

    def load_attendance_data(self):
        if not db.is_connection_usable():
            db.connect()
        try:
            records = Attendance.select().where(Attendance.employee == self.employee).order_by(Attendance.date.desc())
            rows = []
            for record in records:
                date_str = record.date.strftime("%Y-%m-%d")
                day_str = record.date.strftime("%A")
                time_in_str = record.time_in.strftime("%H:%M") if record.time_in else "--:--"
                time_out_str = record.time_out.strftime("%H:%M") if record.time_out else "--:--"
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(date_str)),
                            ft.DataCell(ft.Text(day_str)),
                            ft.DataCell(ft.Text(time_in_str)),
                            ft.DataCell(ft.Text(time_out_str)),
                        ]
                    )
                )
            self.attendance_table.rows = rows
        finally:
            db.close()
