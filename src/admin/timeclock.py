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

        self.all_records = []

        self.date_picker = ft.DatePicker(
            on_change=self.handle_date_change,
            first_date=datetime(2023, 1, 1),
            last_date=datetime(2025, 12, 31)
        )
        self.page.overlay.append(self.date_picker)

        self.search_field = ft.TextField(
            hint_text="Search by Initials, Name or Status",
            on_change=self.filter_attendance,
            expand=True,
        )
        
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
                            content=self.search_field,
                            padding=ft.padding.symmetric(horizontal=10, vertical=10),
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
        self.search_field.value = ""  # Clear search when date changes
        self.load_attendance_data()

    def load_attendance_data(self):
        if not db.is_connection_usable():
            db.connect()
        try:
            query = Attendance.select().where(Attendance.date == self.selected_date)
            self.all_records = list(query)
            self.populate_table(self.all_records)
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error loading data: {ex}"), open=True)
            self.page.update()
        finally:
            if db.is_connection_usable():
                db.close()

    def populate_table(self, records):
        self.data_table.rows.clear()
        for record in records:
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
        self.page.update()

    def filter_attendance(self, e):
        search_term = self.search_field.value.lower()
        if search_term:
            filtered_records = [record for record in self.all_records
                                if search_term in (record.employee.initials or "").lower()
                                or search_term in f"{record.employee.first_name} {record.employee.last_name}".lower()
                                or search_term in record.status.lower()]
        else:
            filtered_records = self.all_records
        self.populate_table(filtered_records)

    def did_mount(self):
        self.load_attendance_data()
