import flet as ft
from database import db
from models.employee import Employee

class QRLoginView(ft.View):
    """
    The initial login view for employees using a QR code.
    Simulates a QR code scan to authenticate and redirect.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/"
        self.page.bgcolor = "#F0F2F5"
        
        self.qr_code_field = ft.TextField(
            label="Enter QR Code (Simulated)",
            helper_text="For demonstration, manually enter an employee's QR code string."
        )

        self.controls = [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Employee Login", size=36, weight="bold"),
                            ft.Text("Scan your QR code to clock in/out", size=18, color="gray"),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(name=ft.Icons.QR_CODE_SCANNER, size=150, color=ft.Colors.DEEP_PURPLE_ACCENT_400),
                                        self.qr_code_field,
                                        ft.ElevatedButton(
                                            text="Simulate Scan & Login",
                                            on_click=self.handle_login
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=ft.padding.all(30),
                                border_radius=ft.border_radius.all(20),
                                bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                alignment=ft.alignment.center
                            ),
                            ft.TextButton("Admin Login", on_click=lambda _: self.page.go("/admin/login"))
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
        qr_code = self.qr_code_field.value
        if not qr_code:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please enter a QR code."), open=True)
            self.page.update()
            return

        db.connect()
        try:
            employee = Employee.get(Employee.qr_code == qr_code)
            self.page.employee = employee
            self.page.go("/user/dashboard")
        except Employee.DoesNotExist:
            self.page.snack_bar = ft.SnackBar(ft.Text("Invalid QR code. Please try again."), open=True)
            self.page.update()
        finally:
            db.close()

