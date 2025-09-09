import flet as ft
from database import db
from models.employee import Employee
from models.attendance import Attendance
from datetime import datetime
from peewee import fn

class UserDashboardView(ft.View):
    """
    The main dashboard view for an employee.
    Displays attendance status and provides clock-in/out functionality.
    """
    def __init__(self, page: ft.Page, employee: Employee):
        super().__init__()
        self.page = page
        self.employee = employee
        self.route = "/user/dashboard"
        self.page.bgcolor = "#F0F2F5"
        print(f"UserDashboardView created with employee: {employee}")
        if employee:
            print(f"Dashboard for: {employee.first_name} {employee.last_name}")
        
        self.status_text = ft.Text(size=24, weight="bold")
        self.time_text = ft.Text(datetime.now().strftime("%H:%M:%S"), size=48, weight="bold")
        self.clock_button = ft.ElevatedButton(
            text="Time In",
            on_click=self.handle_clock,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
            )
        )

        self.controls = [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f"Welcome, {self.employee.first_name if self.employee else 'Unknown'} {self.employee.last_name if self.employee else 'User'}!", size=36, weight="bold"),
                            ft.Text("Your Attendance Status", size=24, weight="w600", color="gray"),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        self.time_text,
                                        self.status_text,
                                        ft.Divider(height=20),
                                        self.clock_button
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=ft.padding.all(30),
                                border_radius=ft.border_radius.all(20),
                                bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                alignment=ft.alignment.center
                            ),
                            ft.ElevatedButton(
                                text="View Profile",
                                on_click=lambda _: self.page.go("/user/profile"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ]

    def handle_clock(self, e):
        db.connect()
        today_date = datetime.now().date()
        
        # Check if the user already has an attendance record for today
        try:
            today_record = Attendance.get(
                Attendance.employee == self.employee,
                Attendance.date == today_date
            )
            
            # If a record exists but time_out is null, it means they need to clock out
            if today_record.time_out is None:
                today_record.time_out = datetime.now()
                today_record.save()
                self.page.snack_bar = ft.SnackBar(ft.Text("Successfully clocked out!"), open=True)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("You have already clocked out for the day."), open=True)

        except Attendance.DoesNotExist:
            # If no record exists, create a new one for clock-in
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
            
    def update_status(self):
        db.connect()
        try:
            today_record = Attendance.get(
                Attendance.employee == self.employee,
                Attendance.date == datetime.now().date()
            )
            if today_record.time_out is None:
                self.status_text.value = "Status: Clocked In"
                self.clock_button.text = "Time Out"
            else:
                self.status_text.value = "Status: Clocked Out"
                self.clock_button.text = "Time In"
        except Attendance.DoesNotExist:
            self.status_text.value = "Status: Clocked Out"
            self.clock_button.text = "Time In"
        finally:
            db.close()
            self.page.update()

    def did_mount(self):
        self.update_status()

