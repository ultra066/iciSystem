import flet as ft
from .navigation import AdminNavigation
from .top_nav import AdminTopNavigation

class AdminLayout(ft.Container):
    """
    Layout component that combines top navigation and sidebar navigation for admin pages.
    This ensures the navigations don't stack and the content doesn't pass through them.
    """
    def __init__(self, page: ft.Page, main_content: ft.Control = None):
        super().__init__()
        self.page = page
        
        # Create instances of the navigation components
        self.top_nav = AdminTopNavigation(page)
        self.side_nav = AdminNavigation(page)
        
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
                            margin=ft.margin.only(top=10)  # Add margin to avoid overlap
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
