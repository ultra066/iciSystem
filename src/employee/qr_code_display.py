import flet as ft
from models.employee import Employee
import os
import base64
from PIL import Image
import io

class QRCodeDisplayView(ft.View):
    """
    View to display the generated QR code after account creation.
    Provides Download and Next buttons.
    """
    def __init__(self, page: ft.Page, employee: Employee, qr_image_path: str):
        super().__init__()
        self.page = page
        self.employee = employee
        self.qr_image_path = qr_image_path
        self.route = "/qr_display"

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

        # Next Button
        self.next_button = ft.ElevatedButton(
            text="Next",
            on_click=self.handle_next,
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
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text(
                                                    "Your QR Code",
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
                                                        self.next_button
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
        # For download, we can use file picker or direct download
        # Since Flet doesn't have direct download, we'll use file picker to save
        self.file_picker.save_file(
            dialog_title="Save QR Code",
            file_name=f"{self.employee.employee_id}_qr.png",
            allowed_extensions=["png"]
        )
        self.page.update()

    def on_save_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            # Copy the QR image to the selected path
            import shutil
            shutil.copy(self.qr_image_path, e.path)
            self.page.snack_bar = ft.SnackBar(ft.Text("QR Code downloaded successfully!"), open=True)
            self.page.update()

    def handle_next(self, e):
        # Proceed to user dashboard
        self.page.employee = self.employee
        self.page.go("/employee/dashboard")
