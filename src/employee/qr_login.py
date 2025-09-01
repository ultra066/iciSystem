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
        self.qr_code_field = ft.TextField(
            label="Enter QR Code (Simulated)",
            helper_text="For demonstration, manually enter an employee's QR code string."
        )

        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Image(
                                        src="images/INNOVATIVE-LOGO.png",
                                        width=300,
                                        height=300,
                                        fit=ft.ImageFit.CONTAIN
                                    ),
                                    ft.Text(
                                        "INNOVATIVE CONTROLS, INC.",
                                        size=30,
                                        color=ft.Colors.BLACK,
                                        text_align=ft.TextAlign.CENTER,
                                        weight=ft.FontWeight.BOLD
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True
                            ),
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
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
                                        gradient=ft.LinearGradient(
                                            begin=ft.Alignment(0, -1),  # top
                                            end=ft.Alignment(0, 1),    # bottom
                                            colors=["#EF3334", "#613636",]
                                        ),
                                        alignment=ft.alignment.center,
                                        width="70%",
                                        height="80%"
                                    ),
                                    ft.TextButton("Admin Login", on_click=lambda _: self.page.go("/admin/login"))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True
                            ),
                            margin=ft.margin.only(right=50),
                            width="75%",
                            height="90%"
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

