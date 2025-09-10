import flet as ft
from database import db
from models.employee import Employee
from models.attendance import Attendance
from datetime import datetime
from peewee import fn
from utils import get_initials
from components.employee_navigation import EmployeeNavigation
from components.employee_top_nav import EmployeeTopNavigation

class UserDashboardView(ft.View):
    """
    The main dashboard view for an employee.
    Displays attendance status and provides clock-in/out functionality.
    """
    def __init__(self, page: ft.Page, employee: Employee):
        super().__init__()
        self.page = page
        self.employee = employee
        self.route = "/employee/dashboard"
        self.page.bgcolor = "#F9F1E0"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.bgcolor = "#F9F1E0"
        print(f"UserDashboardView created with employee: {employee}")
        if employee:
            print(f"Dashboard for: {employee.first_name} {employee.last_name}")

        self.top_nav = EmployeeTopNavigation(self.page)
        self.side_nav = EmployeeNavigation(self.page)

        self.status_text = ft.Text(size=24, weight="bold")
        self.time_text = ft.Text(datetime.now().strftime("%H:%M:%S"), size=48, weight="bold")

        # User status dropdown
        self.current_status = "Active"
        self.status_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option(
                    key="Active",
                    text="Active",
                    content=ft.Row([
                        ft.Container(width=10, height=10, bgcolor=ft.Colors.GREEN, border_radius=5),
                        ft.Text("Active", size=14)
                    ], spacing=5)
                ),
                ft.dropdown.Option(
                    key="Absent",
                    text="Absent",
                    content=ft.Row([
                        ft.Container(width=10, height=10, bgcolor=ft.Colors.RED, border_radius=5),
                        ft.Text("Absent", size=14)
                    ], spacing=5)
                ),
                ft.dropdown.Option(
                    key="Leave",
                    text="Leave",
                    content=ft.Row([
                        ft.Container(width=10, height=10, bgcolor=ft.Colors.BLUE, border_radius=5),
                        ft.Text("Leave", size=14)
                    ], spacing=5)
                ),
                ft.dropdown.Option(
                    key="Off-Site",
                    text="Off-Site",
                    content=ft.Row([
                        ft.Container(width=10, height=10, bgcolor=ft.Colors.ORANGE, border_radius=5),
                        ft.Text("Off-Site", size=14)
                    ], spacing=5)
                ),
            ],
            value=self.current_status,
            on_change=self.handle_status_change,
            width=200,
            border=ft.border.all(0, ft.Colors.TRANSPARENT),
        )
        # Set initial content for selected value
        self.status_dropdown.content = ft.Row([
            ft.Container(width=10, height=10, bgcolor=ft.Colors.GREEN, border_radius=5),
            ft.Text("Active", size=14)
        ], spacing=5)

        # Removed old clock_button since replaced by two buttons
        # self.clock_button = ft.ElevatedButton(
        #     text="Time In",
        #     on_click=self.handle_clock,
        #     bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
        #     style=ft.ButtonStyle(
        #         shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
        #     )
        # )

        # Create time and day text for top-left corner
        self.time_day_text = ft.Text(datetime.now().strftime("%I:%M %p") + "  " + datetime.now().strftime("%A"), size=20, weight="bold")
        self.date_text = ft.Text(datetime.now().strftime("%B %d, %Y"), size=16)

        # Create time-in and time-out display texts
        self.time_in_display = ft.Text("Time-in: --:--", size=16)
        self.time_out_display = ft.Text("Time-Out: --:--", size=16)

        # Create initials and department text
        full_name = f"{self.employee.first_name} {self.employee.middle_name or ''} {self.employee.last_name}".strip()
        initials = self.employee.initials if self.employee and self.employee.initials else get_initials(full_name)
        department_name = self.employee.department.name if self.employee and self.employee.department else "No Department"

        self.initials_text = ft.Text(initials, size=36, weight="bold")
        self.department_text = ft.Text(department_name, size=18)

        # Create separate Time In and Time Out buttons
        self.time_in_button = ft.ElevatedButton(
            text="Time In",
            on_click=self.handle_time_in,
            bgcolor=ft.Colors.RED,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
            )
        )
        self.time_out_button = ft.ElevatedButton(
            text="Time Out",
            on_click=self.handle_time_out,
            bgcolor=ft.Colors.RED,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
            )
        )

        main_content = ft.Stack(
            [
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        self.time_day_text,
                                        self.date_text,
                                        self.time_in_display,
                                        self.time_out_display
                                    ],
                                    alignment=ft.CrossAxisAlignment.START,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                    expand=False
                                ),
                                ft.Container(expand=True)  # Spacer
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            expand=True
                        ),
                        ft.Column(
                            [
                                self.initials_text,
                                self.department_text,
                                ft.Row(
                                    [
                                        self.time_in_button,
                                        self.time_out_button
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20
                                ),
                                self.status_text
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                ft.Container(
                    content=self.status_dropdown,
                    top=0,
                    right=0,
                )
            ],
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

    def handle_time_in(self, e):
        if not db.is_connection_usable():
            db.connect()
        today_date = datetime.now().date()
        try:
            today_record = Attendance.get(
                Attendance.employee == self.employee,
                Attendance.date == today_date
            )
            if today_record.time_in is not None:
                self.page.snack_bar = ft.SnackBar(ft.Text("You have already clocked in for the day."), open=True)
            else:
                today_record.time_in = datetime.now()
                today_record.status = "Present"
                today_record.save()
                self.page.snack_bar = ft.SnackBar(ft.Text("Successfully clocked in!"), open=True)
        except Attendance.DoesNotExist:
            Attendance.create(
                employee=self.employee,
                time_in=datetime.now(),
                date=today_date,
                status="Present"
            )
            self.page.snack_bar = ft.SnackBar(ft.Text("Successfully clocked in!"), open=True)
        finally:
            db.close()
            self.update_status()

    def handle_time_out(self, e):
        if not db.is_connection_usable():
            db.connect()
        today_date = datetime.now().date()
        try:
            today_record = Attendance.get(
                Attendance.employee == self.employee,
                Attendance.date == today_date
            )
            if today_record.time_out is not None:
                self.page.snack_bar = ft.SnackBar(ft.Text("You have already clocked out for the day."), open=True)
            else:
                today_record.time_out = datetime.now()
                today_record.save()
                self.page.snack_bar = ft.SnackBar(ft.Text("Successfully clocked out!"), open=True)
        except Attendance.DoesNotExist:
            self.page.snack_bar = ft.SnackBar(ft.Text("You have not clocked in yet."), open=True)
        finally:
            db.close()
            self.update_status()

    def update_status(self):
        if not db.is_connection_usable():
            db.connect()
        try:
            today_record = Attendance.get(
                Attendance.employee == self.employee,
                Attendance.date == datetime.now().date()
            )
            # Set time displays
            if today_record.time_in:
                self.time_in_display.value = f"Time-in: {today_record.time_in.strftime('%H:%M')}"
            else:
                self.time_in_display.value = "Time-in: --:--"
            if today_record.time_out:
                self.time_out_display.value = f"Time-Out: {today_record.time_out.strftime('%H:%M')}"
            else:
                self.time_out_display.value = "Time-Out: --:--"

            # Set status and button states
            if today_record.time_in is None:
                self.status_text.value = "Status: Not Clocked In"
                self.time_in_button.disabled = False
                self.time_out_button.disabled = True
            elif today_record.time_out is None:
                self.status_text.value = "Status: Clocked In"
                self.time_in_button.disabled = True
                self.time_out_button.disabled = False
            else:
                self.status_text.value = "Status: Clocked Out"
                self.time_in_button.disabled = True
                self.time_out_button.disabled = True
        except Attendance.DoesNotExist:
            self.time_in_display.value = "Time-in: --:--"
            self.time_out_display.value = "Time-Out: --:--"
            self.status_text.value = "Status: Not Clocked In"
            self.time_in_button.disabled = False
            self.time_out_button.disabled = True
        finally:
            db.close()
            self.page.update()

    def update_dropdown_content(self):
        color_map = {
            "Active": ft.Colors.GREEN,
            "Absent": ft.Colors.RED,
            "Leave": ft.Colors.BLUE,
            "Off-Site": ft.Colors.ORANGE,
        }
        selected_color = color_map.get(self.current_status, ft.Colors.BLACK)
        self.status_dropdown.content = ft.Row([
            ft.Container(width=10, height=10, bgcolor=selected_color, border_radius=5),
            ft.Text(self.current_status, size=14)
        ], spacing=5)
        self.status_dropdown.update()

    def handle_status_change(self, e):
        self.current_status = e.control.value
        self.update_dropdown_content()
        # TODO: Add logic to update user status in database or session
        print(f"User status changed to: {self.current_status}")

    def did_mount(self):
        self.update_status()
        self.update_dropdown_content()

