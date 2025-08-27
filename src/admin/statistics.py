import flet as ft
from components.navigation import AdminNavigation
from components.header import AdminHeader

class AdminStatisticsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/statistics"
        self.page.bgcolor = "#F0F2F5"
        
        self.controls = [
            ft.Row(
                [
                    ft.Container(
                        content=AdminNavigation(page=self.page),
                        width=250,
                        bgcolor="#263238",
                        padding=ft.padding.all(20),
                        border_radius=ft.border_radius.all(10),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                AdminHeader("Statistics & Reports"),
                                ft.Divider(height=20),
                                ft.Text("This page will show detailed statistics and reports.", size=24, color="gray"),
                            ],
                            expand=True,
                        ),
                        padding=ft.padding.all(30),
                        expand=True
                    )
                ],
                expand=True
            )
        ]
