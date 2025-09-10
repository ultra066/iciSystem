import flet as ft
from database import db
from models.employee import Employee

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
        self.page.bgcolor = "#F0F2F5"

        self.controls = [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("My Profile", size=36, weight="bold"),
                            ft.Divider(height=20),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.CircleAvatar(
                                            content=ft.Text(self.employee.initials if self.employee.initials else f"{self.employee.first_name[0]}{self.employee.last_name[0]}".upper(), size=30, weight="bold", color="white"),
                                            radius=50,
                                            bgcolor=ft.Colors.DEEP_PURPLE_ACCENT_400
                                        ),
                                        ft.Text(f"{self.employee.first_name} {self.employee.last_name}", size=28, weight="bold"),
                                        ft.Text(f"Employee ID: {self.employee.employee_id}", size=18, color="gray"),
                                        ft.Text(f"Department: {self.employee.department.name}", size=18, color="gray"),
                                    ],
                                    alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=ft.padding.all(30),
                                border_radius=ft.border_radius.all(20),
                                bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                alignment=ft.alignment.center
                            ),
                            ft.ElevatedButton(
                                text="Logout",
                                on_click=lambda _: self.page.go("/"),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.RED_ACCENT_400,
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
