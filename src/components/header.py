import flet as ft
from datetime import datetime

class AdminHeader(ft.Row):
    """
    A reusable header component for the admin pages.
    """
    def __init__(self, page_title: str):
        today_date = datetime.now().strftime("%B %d, %Y")
        super().__init__(
            [
                ft.Text(page_title, size=40, weight="bold", color="white"),
                ft.Text(today_date, size=16, color="white"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
