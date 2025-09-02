import flet as ft
from .employee_navigation import EmployeeNavigation
from .employee_top_nav import EmployeeTopNavigation

class EmployeeLayout(ft.Container):
    """
    Layout component that combines top navigation and sidebar navigation for employee pages.
    This ensures the navigations don't stack and the content doesn't pass through them.
    """
    def __init__(self, page: ft.Page, main_content: ft.Control = None):
        super().__init__()
        self.page = page

        # Create instances of the navigation components
        self.top_nav = EmployeeTopNavigation(page)
        self.side_nav = EmployeeNavigation(page)

        # Create the main layout structure
        self.content = ft.Column(
            controls=[
                # Top navigation bar
                self.top_nav,

                # Main content area with sidebar and content
                ft.Row(
                    controls=[
                        # Sidebar navigation
                        self.side_nav,

                        # Main content area (passed as parameter)
                        ft.Container(
                            content=main_content if main_content else ft.Text("No content provided"),
                            expand=True,
                            padding=ft.padding.all(20),
                            margin=ft.margin.only(top=2)  # Reduced margin to push content closer to top_nav
                        )
                    ],
                    expand=True
                )
            ],
            expand=True
        )

        # Style the layout container
        self.padding = ft.padding.all(0)
        self.bgcolor = ft.Colors.TRANSPARENT
        self.expand = True
