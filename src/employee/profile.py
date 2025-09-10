import flet as ft
from database import db
from models.employee import Employee
from utils import get_initials
from components.employee_navigation import EmployeeNavigation
from components.employee_top_nav import EmployeeTopNavigation

class UserProfileView(ft.View):
    """
    The profile view for an employee.
    Displays personal information and a logout button.
    """
    def __init__(self, page: ft.Page, employee: Employee):
        super().__init__()
        self.page = page
        self.employee = employee
        self.route = "/employee/profile"
        self.page.bgcolor = "#F9F1E0"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.bgcolor = "#F9F1E0"

        self.top_nav = EmployeeTopNavigation(self.page)
        self.side_nav = EmployeeNavigation(self.page)

        main_content = ft.Column(
            [
                ft.Text("My Profile", size=36, weight="bold"),
                ft.Divider(height=20),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.CircleAvatar(
                                content=ft.Text(self.employee.initials if self.employee.initials else get_initials(f"{self.employee.first_name} {self.employee.middle_name or ''} {self.employee.last_name}"), size=30, weight="bold", color="white"),
                                radius=50,
                                bgcolor=ft.Colors.DEEP_PURPLE_ACCENT_400
                            ),
                            ft.Text(f"{self.employee.first_name} {self.employee.middle_name + ' ' if self.employee.middle_name else ''}{self.employee.last_name}", size=28, weight="bold"),
                            ft.Text(f"Employee ID: {self.employee.employee_id}", size=18, color="gray"),
                            ft.Text(f"Department: {self.employee.department.name}", size=18, color="gray"),
                        ],
                        alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(30),
                    border_radius=ft.border_radius.all(20),
                    bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
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
