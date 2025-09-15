import flet as ft
from datetime import date, datetime
from database import db
from models.attendance import Attendance
from components.admin_layout import AdminLayout

class AdminAttendanceView(ft.View):
    """
    The attendance view for the admin.
    Displays a table of employee attendance records for a selected date.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/timeclock"
        self.page.bgcolor = "#F0F2F5"
        self.selected_date = date.today()

        self.date_picker = ft.DatePicker(
            on_change=self.handle_date_change,
            first_date=datetime(2023, 1, 1),
            last_date=datetime(2025, 12, 31)
        )
        self.page.overlay.append(self.date_picker)
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Initials")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Day")),
                ft.DataColumn(ft.Text("Time-in")),
                ft.DataColumn(ft.Text("Time-out")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[]
        )
        
        self.controls = [
            AdminLayout(
                page=self.page,
                main_content=ft.Column(
                    [
                        ft.Text("Employee Attendance", size=36, weight="bold"),
                        ft.Row(
                            [
                                ft.Text(f"Selected Date: {self.selected_date.strftime('%B %d, %Y')}", size=18),
                                ft.ElevatedButton(
                                    "Select Date",
                                    icon=ft.Icons.CALENDAR_MONTH,
                                    on_click=lambda e: self.page.open(self.date_picker),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(
                            content=ft.ListView(
                                [self.data_table],
                                height=400,
                                auto_scroll=True,
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            )
        ]
        
    def handle_date_change(self, e):
        self.selected_date = self.date_picker.value
        self.load_attendance_data()
        
    def load_attendance_data(self):
        self.data_table.rows.clear()
        if not db.is_connection_usable():
            db.connect()
        try:
            query = Attendance.select().where(Attendance.date == self.selected_date)
            for record in query:
                self.data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(record.employee.initials)),
                            ft.DataCell(ft.Text(str(record.date))),
                            ft.DataCell(ft.Text(record.date.strftime('%A'))),
                            ft.DataCell(ft.Text(record.time_in.strftime('%I:%M %p'))),
                            ft.DataCell(ft.Text(record.time_out.strftime('%I:%M %p') if record.time_out else '---')),
                            ft.DataCell(ft.Text(record.status)),
                        ]
                    )
                )
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error loading data: {ex}"), open=True)
        finally:
            if db.is_connection_usable():
                db.close()
            self.page.update()

    def did_mount(self):
        self.load_attendance_data()
