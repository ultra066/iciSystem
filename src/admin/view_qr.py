import flet as ft
from models.employee import Employee
import os
import base64
import shutil

class AdminViewQRView(ft.View):
    """
    View to display the employee's QR code for admin.
    Provides Download and Back buttons.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/employees/view_qr"

        # Get the QR code from page
        qr_code = self.page.qr_code

        # Fetch employee for name
        try:
            employee = Employee.get(Employee.qr_code == qr_code)
        except Employee.DoesNotExist:
            employee = None

        # QR image path
        self.qr_image_path = os.path.join("assets", "qr_codes", f"{employee.employee_id}_qr.png")

        self.file_picker = ft.FilePicker(on_result=self.on_save_result)
        self.page.overlay.append(self.file_picker)

        # Load QR code image as base64
        with open(self.qr_image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # QR Code Image
        self.qr_image = ft.Image(
            src_base64=encoded_string,
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )

        # Download Button
        self.download_button = ft.ElevatedButton(
            text="Download QR Code",
            on_click=self.handle_download,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15)),
                bgcolor=ft.Colors.DEEP_PURPLE_ACCENT_400,
                color="white"
            )
        )

        # Back Button
        self.back_button = ft.ElevatedButton(
            text="Back",
            on_click=self.handle_back,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15)),
                bgcolor=ft.Colors.GREY_400,
                color="white"
            )
        )

        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text(
                                                    f"QR Code for {employee.first_name} {employee.last_name}",
                                                    size=30,
                                                    color=ft.Colors.WHITE,
                                                    text_align=ft.TextAlign.CENTER,
                                                    weight=ft.FontWeight.BOLD
                                                ),
                                                self.qr_image,
                                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                                ft.Row(
                                                    [
                                                        self.download_button,
                                                        ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                                                        self.back_button
                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER
                                                )
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=20
                                        ),
                                        padding=ft.padding.all(30),
                                        border_radius=ft.border_radius.all(20),
                                        gradient=ft.LinearGradient(
                                            begin=ft.Alignment(0, -1),  # top
                                            end=ft.Alignment(0, 1),    # bottom
                                            colors=["#EF3334", "#613636"]
                                        ),
                                        alignment=ft.alignment.center,
                                        width="70%",
                                        height="80%"
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True
                            ),
                            width="75%",
                            height="90%"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
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

    def handle_download(self, e):
        # Use file picker to save
        employee = Employee.get(Employee.qr_code == self.page.qr_code)
        self.file_picker.save_file(
            dialog_title="Save QR Code",
            file_name=f"{employee.employee_id}_qr.png",
            allowed_extensions=["png"]
        )
        self.page.update()

    def on_save_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            # Copy the QR image to the selected path
            shutil.copy(self.qr_image_path, e.path)
            self.page.snack_bar = ft.SnackBar(ft.Text("QR Code downloaded successfully!"), open=True)
            self.page.update()

    def handle_back(self, e):
        # Go back to employees page
        self.page.go("/admin/employees")
