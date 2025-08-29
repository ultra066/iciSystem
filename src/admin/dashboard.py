import flet as ft
from datetime import datetime
from database import db
from models.employee import Employee
from models.attendance import Attendance
from components.admin_layout import AdminLayout
from components.header import AdminHeader
from components.pie_graph import EmployeeStatusPieChart, fetch_employee_status_data  # Importing the function and class
from components.monthly_summary import MonthlySummary
from components.time_in_time_out import TodayAttendance
from components.cards import InfoCard
from peewee import fn

def fetch_monthly_summary_data():
    """Fetch monthly attendance summary data for the current month"""
    try:
        db.connect()
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Get total employees
        total_employees = Employee.select().count()
        
        # Get first and last day of current month
        first_day = datetime(current_year, current_month, 1).date()
        if current_month == 12:
            last_day = datetime(current_year + 1, 1, 1).date()
        else:
            last_day = datetime(current_year, current_month + 1, 1).date()
        
        # Get attendance data for current month using date range
        present_count = (Attendance
                        .select()
                        .where(
                            (Attendance.date >= first_day) &
                            (Attendance.date < last_day) &
                            (Attendance.status == 'Present')
                        )
                        .count())
        
        absent_count = (Attendance
                       .select()
                       .where(
                           (Attendance.date >= first_day) &
                           (Attendance.date < last_day) &
                           (Attendance.status == 'Absent')
                       )
                       .count())
        
        # Calculate percentages
        total_records = present_count + absent_count
        if total_records > 0:
            active_percent = round((present_count / total_records) * 100)
            absent_percent = round((absent_count / total_records) * 100)
        else:
            active_percent = 0
            absent_percent = 0
            
        # For demo purposes, using placeholder values for changes
        active_change = 5  # 5% increase from last month
        absent_change = -3  # 3% decrease from last month
        
    finally:
        db.close()
    
    return {
        'month': datetime.now().strftime('%B'),
        'year': current_year,
        'active_percent': active_percent,
        'absent_percent': absent_percent,
        'active_change': active_change,
        'absent_change': absent_change
    }

def fetch_today_attendance_data():
    """Fetch today's attendance data for the time-in/time-out component"""
    try:
        db.connect()
        today_date = datetime.now().date()
        
        # Get all employees with their attendance for today
        attendance_data = []
        employees = Employee.select()
        
        for employee in employees:
            # Get today's attendance record for this employee
            attendance_record = (Attendance
                               .select()
                               .where(
                                   (Attendance.employee_id == employee.id) &
                                   (Attendance.date == today_date)
                               )
                               .first())
            
            if attendance_record:
                time_in = attendance_record.time_in.strftime('%I:%M %p') if attendance_record.time_in else 'Not clocked in'
                time_out = attendance_record.time_out.strftime('%I:%M %p') if attendance_record.time_out else 'Not clocked out'
            else:
                time_in = 'Not clocked in'
                time_out = 'Not clocked out'
            
            attendance_data.append({
                'name': employee.name,
                'initials': employee.initials if employee.initials else employee.name[:2].upper(),
                'dept': employee.department.name if employee.department else 'N/A',
                'time_in': time_in,
                'time_out': time_out
            })
            
    finally:
        db.close()
    
    return attendance_data

class AdminDashboardView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/dashboard"
        self.page.bgcolor = "#F0F2F5"  # A light, modern background color
        
        self.page.appbar = ft.AppBar(
            title=ft.Text("Dashboard", size=24, weight="bold"),
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
        )

        # Fetch data for components
        monthly_data = fetch_monthly_summary_data()
        status_data = fetch_employee_status_data()
        attendance_data = fetch_today_attendance_data()

        # Create the TodayAttendance component and populate it with data
        today_attendance = TodayAttendance()
        # Set the data directly instead of calling update_attendance_data which tries to update before component is added
        today_attendance.attendance_data = attendance_data
        today_attendance.data_table.rows = today_attendance.create_table_rows(attendance_data)

        self.controls = [
            AdminLayout(
                page=self.page,
                main_content=ft.Column(
                    [
                        AdminHeader("DASHBOARD"),
                        ft.Divider(height=20),
                        ft.Row(
                            [
                                # Left column with pie chart on top of monthly summary
                                ft.Column(
                                    [
                                        EmployeeStatusPieChart(*status_data),
                                        ft.Divider(height=20),
                                        MonthlySummary(
                                            month=monthly_data['month'],
                                            year=monthly_data['year'],
                                            active_percent=monthly_data['active_percent'],
                                            absent_percent=monthly_data['absent_percent'],
                                            active_change=monthly_data['active_change'],
                                            absent_change=monthly_data['absent_change']
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                ),
                                # Right column with time-in/time-out component - now expands to fill space
                                ft.Column(
                                    [
                                        today_attendance
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                    expand=True
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=40,
                            expand=True
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        ]

    def create_info_cards(self):
        try:
            db.connect()
            # Calculate stats
            total_employees = Employee.select().count()
            today_date = datetime.now().date()
            present_employees = Attendance.select().where(Attendance.date == today_date).count()
        finally:
            db.close()
        
        return ft.Row(
            [
                InfoCard("Total Employees", str(total_employees), ft.Icons.PEOPLE, "#007BFF"),
                InfoCard("Present Today", str(present_employees), ft.Icons.CHECK_CIRCLE, "#28A745"),
                InfoCard("Absent Today", str(total_employees - present_employees), ft.Icons.CANCEL, "#DC3545"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )

    def create_attendance_table_container(self):
        return ft.Container(
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(10),
            content=ft.Column(
                [
                    ft.Text("Today's Attendance", size=20, weight="bold"),
                    ft.Divider(height=10),
                    self.create_attendance_table()
                ]
            )
        )
    
    def create_attendance_table(self):
        # We'll populate this table dynamically
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Department")),
                ft.DataColumn(ft.Text("Time-in")),
                ft.DataColumn(ft.Text("Time-out")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[]
        )

    def did_mount(self):
        # No need to load attendance data since table is removed
        pass

    def load_daily_attendance_data(self):
        # This method is no longer needed since table is removed
        pass
