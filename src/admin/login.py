# admin/login.py

import flet as ft
from auth import check_admin_credentials

class AdminLoginView(ft.View):
    """
    The login view for administrators.
    Allows admins to enter credentials and handles authentication.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/login"
        self.page.bgcolor = "#F0F2F5"

        self.username_field = ft.TextField(label="Username", icon=ft.Icons.PERSON)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
        self.login_button = ft.ElevatedButton(
            text="Login",
            on_click=self.handle_login,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15)),
                bgcolor=ft.Colors.DEEP_PURPLE_ACCENT_400,
                color="white"
            )
        )

        self.controls = [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Admin Login", size=36, weight="bold"),
                            ft.Text("Please enter your credentials to proceed.", size=18, color="gray"),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        self.username_field,
                                        self.password_field,
                                        self.login_button,
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=ft.padding.all(30),
                                border_radius=ft.border_radius.all(20),
                                bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.RED),
                                alignment=ft.alignment.center
                            ),
                            ft.TextButton("Employee Login", on_click=lambda _: self.page.go("/"))
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

    def handle_login(self, e):
        username = self.username_field.value
        password = self.password_field.value

        if check_admin_credentials(username, password):
            # Navigate to the admin dashboard on successful login
            self.page.go("/admin/dashboard")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Invalid username or password."), open=True)
            self.page.update()

