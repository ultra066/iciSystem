import flet as ft
from datetime import datetime  # Importing the datetime module
from database import db  # Importing the database connection
from models.employee import Employee  # Importing the Employee model
from models.attendance import Attendance  # Importing the Attendance model
import math

class EmployeeStatusPieChart(ft.Container):
    def __init__(self, present_count, leave_count, off_site_count, absent_count):
        super().__init__()
        self.present_count = present_count
        self.leave_count = leave_count
        self.off_site_count = off_site_count
        self.absent_count = absent_count
        
        # Calculate total and percentages
        total = present_count + leave_count + off_site_count + absent_count
        present_percent = (present_count / total * 100) if total > 0 else 0
        leave_percent = (leave_count / total * 100) if total > 0 else 0
        off_site_percent = (off_site_count / total * 100) if total > 0 else 0
        absent_percent = (absent_count / total * 100) if total > 0 else 0
        
        # Create pie chart sections
        chart_sections = [
            ft.PieChartSection(
                present_percent,
                color=ft.Colors.GREEN,
                radius=60,
            ),
            ft.PieChartSection(
                leave_percent,
                color=ft.Colors.BLUE,
                radius=60,
            ),
            ft.PieChartSection(
                off_site_percent,
                color=ft.Colors.ORANGE,
                radius=60,
            ),
            ft.PieChartSection(
                absent_percent,
                color=ft.Colors.RED,
                radius=60,
            ),
        ]
        
        # Create the pie chart
        pie_chart = ft.PieChart(
            sections=chart_sections,
            sections_space=0,
            center_space_radius=0,
            expand=True,
        )
        
        # Create legend items
        legend_items = [
            self._create_legend_item("Present", f"{present_percent:.1f}%", ft.Colors.GREEN),
            self._create_legend_item("Leave", f"{leave_percent:.1f}%", ft.Colors.BLUE),
            self._create_legend_item("Off-Site", f"{off_site_percent:.1f}%", ft.Colors.ORANGE),
            self._create_legend_item("Absent", f"{absent_percent:.1f}%", ft.Colors.RED),
        ]
        
        # Create the main content
        self.content = ft.Column(
            controls=[
                # Title - centered at top
                ft.Text("EMPLOYEE STATUS", size=18, weight=ft.FontWeight.BOLD),
                
                ft.Row(
                    controls=[
                        # Pie Chart - smaller size to fit inside container
                        ft.Container(
                            content=pie_chart,
                            width=120,
                            height=120,
                            alignment=ft.alignment.center,
                        ),
                        # Legend
                        ft.Column(
                            controls=legend_items,
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        
        # Style the container - responsive sizing
        self.bgcolor = ft.Colors.GREY_900
        self.padding = 15
        self.border_radius = 15
        self.expand = True
        
    def _create_legend_item(self, label, percentage, color):
        return ft.Row(
            controls=[
                ft.Text(percentage, width=40, text_align=ft.TextAlign.RIGHT),
                ft.Container(
                    width=15,
                    height=15,
                    border_radius=7.5,
                    bgcolor=color,
                ),
                ft.Text(label),
            ],
            spacing=5,
        )

def fetch_employee_status_data():
    try:
        db.connect()
        total_employees = Employee.select().count()
        today_date = datetime.now().date()
        present_count = Attendance.select().where(Attendance.date == today_date, Attendance.status == 'Present').count()
        leave_count = Attendance.select().where(Attendance.date == today_date, Attendance.status == 'Leave').count()
        off_site_count = Attendance.select().where(Attendance.date == today_date, Attendance.status == 'Off-Site').count()
        absent_count = total_employees - (present_count + leave_count + off_site_count)
    finally:
        db.close()
    
    return present_count, leave_count, off_site_count, absent_count
