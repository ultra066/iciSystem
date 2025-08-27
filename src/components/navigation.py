import flet as ft

class AdminNavigation(ft.Container):
    """
    A reusable navigation sidebar for the admin pages.
    """
    def __init__(self, page: ft.Page):
        super().__init__(
            content=ft.Column(
                [
                    ft.TextButton(
                        content=ft.Text("Dashboard", size=20, weight="bold"),
                        style=ft.ButtonStyle(color="white"),
                        on_click=lambda _: page.go("/admin/dashboard")
                    ),
                    ft.TextButton(
                        content=ft.Text("Employees", size=20, weight="bold"),
                        style=ft.ButtonStyle(color="white"),
                        on_click=lambda _: page.go("/admin/employees")
                    ),
                    ft.TextButton(
                        content=ft.Text("Departments", size=20, weight="bold"),
                        style=ft.ButtonStyle(color="white"),
                        on_click=lambda _: page.go("/admin/departments")
                    ),
                    ft.TextButton(
                        content=ft.Text("Attendance", size=20, weight="bold"),
                        style=ft.ButtonStyle(color="white"),
                        on_click=lambda _: page.go("/admin/attendance")
                    ),
                    ft.TextButton(
                        content=ft.Text("Statistics", size=20, weight="bold"),
                        style=ft.ButtonStyle(color="white"),
                        on_click=lambda _: page.go("/admin/statistics")
                    ),
                    ft.TextButton(
                        content=ft.Text("Logout", size=20, weight="bold"),
                        style=ft.ButtonStyle(color="white"),
                        on_click=lambda _: page.go("/")
                    ),
                ],
                spacing=25,
            ),
            padding=20,
            width=250,
            bgcolor="#263238",
            border_radius=ft.border_radius.all(10),
        )
