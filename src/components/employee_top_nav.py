import flet as ft

class EmployeeTopNavigation(ft.Container):
    """
    Transparent top navigation for employee pages with Dashboard button only
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Create the logo container
        self.logo = ft.Container(
            content=ft.Image(
                src=r"images/INNOVATIVE-LOGO.png",  # Placeholder for your image path
                fit=ft.ImageFit.CONTAIN
            ),
            on_click=lambda _: self.page.go("/employee/dashboard"),
            height=50,
            alignment=ft.alignment.center
        )

        # Create navigation buttons
        self.dashboard_btn = ft.TextButton(
            text="Dashboard",
            icon=ft.Icons.DASHBOARD,
            on_click=lambda e: self.page.go("/employee/dashboard"),
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            )
        )

        # Create the navigation container
        self.content = ft.Row(
            controls=[
                # Logo area
                self.logo,

                # Navigation buttons positioned in the middle left
                ft.Container(
                    content=ft.Row(
                        controls=[self.dashboard_btn],
                        spacing=20
                    ),
                    margin=ft.margin.only(left=20),  # Adjust this value based on your logo width
                    alignment=ft.alignment.center_left
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )

        # Style the navigation container
        self.bgcolor = ft.Colors.TRANSPARENT
        self.padding = ft.padding.symmetric(vertical=20, horizontal=20)
        self.width = self.page.width

    def update_width(self):
        self.width = self.page.width
