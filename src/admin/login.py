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
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Column(
                                [
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
                                        gradient=ft.LinearGradient(
                                            begin=ft.Alignment(0, -1),  # top
                                            end=ft.Alignment(0, 1),    # bottom
                                            colors=["#EF3334", "#613636"]
                                        ),
                                        alignment=ft.alignment.center,
                                        width=650,
                                        height=400
                                    ),
                                    ft.TextButton("Employee Login", on_click=lambda _: self.page.go("/"))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True
                            ),
                            margin=ft.margin.only(right=50),
                            width=450,
                            height=600
                        )
                    ],
                    expand=True
                ),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1, 1),  # bottom-left
                    end=ft.Alignment(1, -1),    # top-right
                    colors=["#7B2727", "#DB7929", "#D9D9D9"]
                ),
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

