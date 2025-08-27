import flet as ft

class InfoCard(ft.Container):
    """
    A reusable card component to display summary information.
    """
    def __init__(self, title: str, value: str, icon_name: str, color: str):
        super().__init__(
            padding=ft.padding.all(20),
            border_radius=ft.border_radius.all(10),
            bgcolor=color,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(title, size=16, weight="bold", color="white"),
                            ft.Icon(name=icon_name, color="white", size=24),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text(value, size=28, weight="bold", color="white"),
                ]
            )
        )
