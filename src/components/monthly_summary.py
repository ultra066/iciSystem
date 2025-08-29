import flet as ft

class MonthlySummary(ft.Container):
    def __init__(self, month="JULY", year=2025, active_percent=70, absent_percent=10, 
                 active_change=5, absent_change=-3):
        super().__init__()
        self.month = month
        self.year = year
        self.active_percent = active_percent
        self.absent_percent = absent_percent
        self.active_change = active_change  # Positive means increase, negative means decrease
        self.absent_change = absent_change  # Positive means increase, negative means decrease
        
        # Determine triangle direction and color for active
        if self.active_change > 0:
            active_triangle = ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.GREEN, size=20)
            active_text = "More Active"
        else:
            active_triangle = ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.RED, size=20)
            active_text = "Less Active"
        
        # Determine triangle direction and color for absent
        if self.absent_change > 0:
            absent_triangle = ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.RED, size=20)
            absent_text = "More Absents"
        else:
            absent_triangle = ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.GREEN, size=20)
            absent_text = "Less Absents"
        
        # Create the component content - larger text sizes
        self.content = ft.Column(
            controls=[
                # Title
                ft.Text("MONTHLY SUMMARY", size=18, weight=ft.FontWeight.BOLD),
                
                # Month and Year
                ft.Text(f"{self.month} {self.year}", size=16, weight=ft.FontWeight.W_500),
                
                # Percentages with triangles
                ft.Row(
                    controls=[
                        # Active percentage
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(f"{self.active_percent}%", size=28, weight=ft.FontWeight.BOLD),
                                        active_triangle,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Text("Active", size=14),
                                ft.Text(active_text, size=12, color=ft.Colors.GREEN if self.active_change > 0 else ft.Colors.RED),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=3,
                        ),
                        
                        # Spacer
                        ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                        
                        # Absent percentage
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(f"{self.absent_percent}%", size=28, weight=ft.FontWeight.BOLD),
                                        absent_triangle,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Text("Absent", size=14),
                                ft.Text(absent_text, size=12, color=ft.Colors.RED if self.absent_change > 0 else ft.Colors.GREEN),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=3,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        )
        
        # Style the container - same size as pie_chart container (350x200px)
        self.bgcolor = ft.Colors.GREY_900
        self.padding = 15
        self.border_radius = 15
        self.width = 350
        self.height = 190

# Example usage
def main(page: ft.Page):
    page.title = "Monthly Summary"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Create the monthly summary component
    monthly_summary = MonthlySummary(
        month="JULY",
        year=2025,
        active_percent=70,
        absent_percent=10,
        active_change=5,  # 5% increase from last month
        absent_change=-3  # 3% decrease from last month
    )
    
    page.add(monthly_summary)

if __name__ == "__main__":
    ft.app(target=main)
