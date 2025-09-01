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
        
        # Create the two button containers
        scan_button = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name=ft.Icons.QR_CODE_SCANNER, size=80, color=ft.Colors.WHITE),
                    ft.Text("SCAN QR", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            padding=ft.padding.all(30),
            border_radius=ft.border_radius.all(20),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),  # top-left
                end=ft.Alignment(1, 1),    # bottom-right
                colors=["#EF3334", "#DB7929"]
            ),
            on_click=self.handle_scan_click,
            alignment=ft.alignment.center,
            width=200,
            height=200
        )
        
        upload_button = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name=ft.Icons.UPLOAD_FILE, size=80, color=ft.Colors.WHITE),
                    ft.Text("UPLOAD QR", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            padding=ft.padding.all(30),
            border_radius=ft.border_radius.all(20),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),  # top-left
                end=ft.Alignment(1, 1),    # bottom-right
                colors=["#EF3334", "#DB7929"]
            ),
            on_click=self.handle_upload_click,
            alignment=ft.alignment.center,
            width=200,
            height=200
        )

        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Image(
                                        src="images/LOGO.png",
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
                                                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                                                ft.Row(
                                                    [
                                                        scan_button,
                                                        ft.VerticalDivider(width=30, color=ft.Colors.TRANSPARENT),
                                                        upload_button
                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER
                                                )
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=10
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
                                        height="70%"
                                    ),
                                    ft.TextButton(
                                        "Admin Login", 
                                        on_click=lambda _: self.page.go("/admin/login"),
                                        style=ft.ButtonStyle(color=ft.Colors.WHITE)
                                    )
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

    def handle_scan_click(self, e):
        # Handle QR code scanning
        self.page.snack_bar = ft.SnackBar(ft.Text("Scan QR code functionality would be implemented here."), open=True)
        self.page.update()

    def handle_upload_click(self, e):
        # Handle QR code upload
        self.page.snack_bar = ft.SnackBar(ft.Text("Upload QR code functionality would be implemented here."), open=True)
        self.page.update()

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