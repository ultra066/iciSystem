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

        # Create a large centered profile icon
        profile_icon = ft.CircleAvatar(
            content=ft.Icon(name=ft.Icons.PERSON, size=40, color="white"),
            radius=60,
            bgcolor=ft.Colors.DEEP_PURPLE_ACCENT_400
        )

        main_content = ft.Column(
            [
                ft.Text("Employee Profile", size=36, weight="bold"),
                ft.Container(
                    content=ft.Column(
                        [
                            # Large centered profile icon
                            ft.Container(
                                content=profile_icon,
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(bottom=20)
                            ),

                            # Name field
                            ft.Container(
                                content=ft.Text(f"{self.employee.first_name} {self.employee.middle_name + ' ' if self.employee.middle_name else ''}{self.employee.last_name}", size=24, weight="bold"),
                                alignment=ft.alignment.center
                            ),
                            ft.Divider(height=10, color="transparent"),

                            # Initials field
                            ft.Row(
                                [
                                    ft.Text("Initials:", size=18, weight="bold", width=100),
                                    ft.Text(self.employee.initials if self.employee.initials else get_initials(f"{self.employee.first_name} {self.employee.middle_name or ''} {self.employee.last_name}"), size=18),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Divider(height=10, color="transparent"),

                            # Department field
                            ft.Row(
                                [
                                    ft.Text("Department:", size=18, weight="bold", width=100),
                                    ft.Text(self.employee.department.name, size=18),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                        ],
                        alignment=ft.CrossAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(40),
                    border_radius=ft.border_radius.all(20),
                    bgcolor=ft.Colors.TRANSPARENT,
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
