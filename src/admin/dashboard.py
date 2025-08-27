import flet as ft
from datetime import datetime
from database import db
from models.employee import Employee
from models.attendance import Attendance
from components.navigation import AdminNavigation
from components.header import AdminHeader
from components.cards import InfoCard
from peewee import fn

class AdminDashboardView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/dashboard"
        self.page.bgcolor = "#F0F2F5"  # A light, modern background color
        
        self.page.appbar = ft.AppBar(
            title=ft.Text("Dashboard", size=24, weight="bold"),
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
        )

        self.controls = [
            ft.Row(
                [
                    # Sidebar navigation
                    AdminNavigation(page=self.page),
                    # Main content area
                    ft.Container(
                        content=ft.Column(
                            [
                                AdminHeader("Admin Dashboard"),
                                ft.Divider(height=20),
                                ft.Row(
                                    [
                                        self.create_info_cards(),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    expand=True
                                ),
                                ft.Divider(height=20),
                                self.create_attendance_table_container(),
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.all(30),
                        expand=True
                    )
                ],
                expand=True
            )
        ]

    def create_info_cards(self):
        try:
            db.connect()
            # Calculate stats
            total_employees = Employee.select().count()
            today_date = datetime.now().date()
            present_employees = Attendance.select().where(Attendance.date == today_date).count()
        finally:
            db.close()
        
        return ft.Row(
            [
                InfoCard("Total Employees", str(total_employees), ft.Icons.PEOPLE, "#007BFF"),
                InfoCard("Present Today", str(present_employees), ft.Icons.CHECK_CIRCLE, "#28A745"),
                InfoCard("Absent Today", str(total_employees - present_employees), ft.Icons.CANCEL, "#DC3545"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )

    def create_attendance_table_container(self):
        return ft.Container(
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(10),
            content=ft.Column(
                [
                    ft.Text("Today's Attendance", size=20, weight="bold"),
                    ft.Divider(height=10),
                    self.create_attendance_table()
                ]
            )
        )
    
    def create_attendance_table(self):
        # We'll populate this table dynamically
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Department")),
                ft.DataColumn(ft.Text("Time-in")),
                ft.DataColumn(ft.Text("Time-out")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[]
        )

    def did_mount(self):
        self.load_daily_attendance_data()

    def load_daily_attendance_data(self):
        try:
            db.connect()
            today_date = datetime.now().date()
            
            attendance_query = (Attendance
                                .select(Attendance, Employee, Employee.name, Employee.initials)
                                .join(Employee)
                                .where(Attendance.date == today_date))
            
            table = self.controls[0].controls[1].controls[2].content.controls[2]
            table.rows.clear()
            
            if attendance_query.count() == 0:
                # Add a message row if no attendance records found
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("No attendance records for today", italic=True, color="gray")),
                            ft.DataCell(ft.Text("")),
                            ft.DataCell(ft.Text("")),
                            ft.DataCell(ft.Text("")),
                            ft.DataCell(ft.Text("")),
                        ]
                    )
                )
            else:
                for record in attendance_query:
                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(record.employee.name)),
                                ft.DataCell(ft.Text(record.employee.department.name)),
                                ft.DataCell(ft.Text(record.time_in.strftime("%I:%M %p"))),
                                ft.DataCell(ft.Text(record.time_out.strftime("%I:%M %p") if record.time_out else "N/A")),
                                ft.DataCell(ft.Text(record.status)),
                            ]
                        )
                    )
            
            self.page.update()
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error loading attendance data: {e}"), open=True)
            self.page.update()
        finally:
            db.close()
