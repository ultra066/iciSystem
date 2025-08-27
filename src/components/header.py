import flet as ft

class AdminHeader(ft.Row):
    """
    A reusable header component for the admin pages.
    """
    def __init__(self, page_title: str):
        super().__init__(
            [
                ft.Text(page_title, size=40, weight="bold", color="white"),
                ft.Row(
                    [
                        ft.Icon(name=ft.Icons.ACCOUNT_CIRCLE, color="white", size=30),
                        ft.Text("Admin 0", size=16, color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
