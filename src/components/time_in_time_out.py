import flet as ft

class TodayAttendance(ft.Container):
    def __init__(self):
        super().__init__()
        # Initialize with empty attendance data
        self.attendance_data = []
        
        # Create search field
        self.search_field = ft.TextField(
            hint_text="Search employees...",
            on_change=self.filter_table,
            expand=True,
            bgcolor=ft.Colors.GREY_800,
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_600,
        )
        
        # Create data table
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Initials", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Dept", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Time-In", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Time-Out", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ],
            rows=[],  # Start with empty rows
        )
        
        # Create the component content
        self.content = ft.Column(
            controls=[
                # Title
                ft.Text("TIME-IN & TIME-OUT", 
                        size=20, 
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE),
                
                # Search area
                ft.Row(
                    controls=[
                        self.search_field,
                        ft.IconButton(
                            icon=ft.Icons.SEARCH,
                            icon_color=ft.Colors.WHITE,
                            on_click=self.filter_table,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                
                # Table container with scrollable content
                ft.Container(
                    content=ft.ListView(
                        [self.data_table],
                        height=275,
                        auto_scroll=True,
                    ),
                    border_radius=ft.border_radius.all(5),
                ),
            ],
            spacing=15,
        )
        
        # Style the container - responsive sizing
        self.bgcolor = ft.Colors.GREY_900
        self.padding = 20
        self.border_radius = 10
        self.expand = True
        
    def create_table_rows(self, data):
        rows = []
        for employee in data:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(employee.get('initials', 'N/A'), color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(employee.get('dept', 'N/A'), color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(employee.get('time_in', 'Not clocked in'), color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(employee.get('time_out', 'Not clocked out'), color=ft.Colors.WHITE)),
                    ]
                )
            )
        return rows
    
    def filter_table(self, e):
        search_term = self.search_field.value.lower()
        if search_term:
            filtered_data = [emp for emp in self.attendance_data 
                            if search_term in emp.get('name', '').lower() 
                            or search_term in emp.get('initials', '').lower()
                            or search_term in emp.get('dept', '').lower()]
        else:
            filtered_data = self.attendance_data
            
        self.data_table.rows = self.create_table_rows(filtered_data)
        # Don't call self.update() here as it may cause issues before component is added to page
    
    def update_attendance_data(self, new_data):
        """Update the attendance data with new records"""
        self.attendance_data = new_data
        self.data_table.rows = self.create_table_rows(self.attendance_data)
        # Don't call self.update() here as the component may not be added to page yet

# Example usage in a dashboard
def main(page: ft.Page):
    page.title = "Today's Attendance"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.GREY_300
    
    # Create the attendance component
    attendance_component = TodayAttendance()
    
    # In a real application, you would update this with data from your database
    # For demonstration, we'll simulate adding data later
    page.add(attendance_component)
    
    # Example of how to update the data later
    # This would be called when new attendance records are added to the database
    def simulate_data_update():
        # Simulated data that would come from your database
        new_data = [
            {'name': 'John Doe', 'initials': 'JD', 'dept': 'Engineering', 'time_in': '08:15 AM', 'time_out': ''},
            {'name': 'Jane Smith', 'initials': 'JS', 'dept': 'Marketing', 'time_in': '08:30 AM', 'time_out': ''},
        ]
        attendance_component.update_attendance_data(new_data)
    
    # Simulate data update after 2 seconds
    import threading
    import time
    def delayed_update():
        time.sleep(2)
        simulate_data_update()
        page.update()
    
    threading.Thread(target=delayed_update, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)