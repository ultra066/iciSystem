import flet as ft

class AdminNavigation(ft.Container):
    """
    A reusable navigation sidebar for the admin pages.
    """
    def __init__(self, page: ft.Page):
        self.page = page
        
        # Create the column content
        column_content = ft.Column(
            [
                
                # Profile Button
                ft.Container(
                    content=ft.Icon(name=ft.Icons.ACCOUNT_CIRCLE, color="white"),
                    width=60,
                    height=60,
                    border_radius=ft.border_radius.all(30),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    alignment=ft.alignment.center,
                    on_click=lambda _: self.page.go("/admin/profile")
                ),
                
                # Time Clock Button
                ft.Container(
                    content=ft.Icon(name=ft.Icons.ACCESS_TIME, color="white"),
                    width=60,
                    height=60,
                    border_radius=ft.border_radius.all(30),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    alignment=ft.alignment.center,
                    on_click=lambda _: self.page.go("/admin/timeclock")
                ),

                # Placeholder to fill remaining space
                ft.Column(
                    [],
                    expand=True
                ),

                # Logout Button at the bottom
                ft.Container(
                    content=ft.Icon(name=ft.Icons.EXIT_TO_APP, color="white"),
                    width=60,
                    height=60,
                    border_radius=ft.border_radius.all(30),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    alignment=ft.alignment.center,
                    on_click=lambda _: self.page.go("/")
                ),
            ],
            spacing=25,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # Wrap the column in a container for padding and styling
        super().__init__(
            content=column_content,
            padding=ft.padding.all(20),
            width=100,
            bgcolor="transparent"
        )
