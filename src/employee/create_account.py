import flet as ft
from database import db
from models.employee import Employee
from models.department import Department
import uuid
from qr_manager import generate_qr_code

class CreateAccountView(ft.View):
    """
    The create account view for new employees.
    Allows users to enter their details and create an account.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/create_account"

        # Form fields
        self.first_name_field = ft.TextField(label="First Name", icon=ft.Icons.PERSON)
        self.middle_name_field = ft.TextField(label="Middle Name", icon=ft.Icons.PERSON)
        self.last_name_field = ft.TextField(label="Last Name", icon=ft.Icons.PERSON)

        # Department dropdown with predefined options
        self.department_options = [
            ft.dropdown.Option(key="Information Technology", text="Information Technology"),
            ft.dropdown.Option(key="Sales", text="Sales"),
            ft.dropdown.Option(key="Human Resource", text="Human Resource"),
            ft.dropdown.Option(key="Marketing", text="Marketing"),
            ft.dropdown.Option(key="Production", text="Production"),
            ft.dropdown.Option(key="Engineering", text="Engineering"),
            ft.dropdown.Option(key="Automation", text="Automation"),
            ft.dropdown.Option(key="Admin", text="Admin"),
            ft.dropdown.Option(key="Others", text="Others")
        ]

        self.department_dropdown = ft.Dropdown(
            label="Department",
            options=self.department_options,
            on_change=self.handle_department_change
        )

        self.custom_department_field = ft.TextField(
            label="Specify Department",
            icon=ft.Icons.EDIT,
            visible=False
        )

        self.create_button = ft.ElevatedButton(
            text="Create Account",
            on_click=self.handle_create_account,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15)),
                bgcolor=ft.Colors.DEEP_PURPLE_ACCENT_400,
                color="white"
            )
        )

        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Image(
                                        src="images/LOGO.png",
                                        width=300,
                                        height=300,
                                        fit=ft.ImageFit.CONTAIN
                                    ),
                                    ft.Text(
                                        "INNOVATIVE CONTROLS, INC.",
                                        size=30,
                                        color=ft.Colors.BLACK,
                                        text_align=ft.TextAlign.CENTER,
                                        weight=ft.FontWeight.BOLD
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True
                            ),
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                self.first_name_field,
                                                self.middle_name_field,
                                                self.last_name_field,
                                                self.department_dropdown,
                                                self.custom_department_field,
                                                self.create_button,
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=20
                                        ),
                                        padding=ft.padding.all(30),
                                        border_radius=ft.border_radius.all(20),
                                        gradient=ft.LinearGradient(
                                            begin=ft.Alignment(0, -1),  # top
                                            end=ft.Alignment(0, 1),    # bottom
                                            colors=["#EF3334", "#613636"]
                                        ),
                                        alignment=ft.alignment.center,
                                        width="70%",
                                        height="80%"
                                    ),
                                    ft.TextButton("Back to Login", on_click=lambda _: self.page.go("/"))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True
                            ),
                            margin=ft.margin.only(right=50),
                            width="75%",
                            height="90%"
                        )
                    ],
                    expand=True
                ),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1, 1),  # bottom-left
                    end=ft.Alignment(1, -1),    # top-right
                    colors=["#7B2727", "#DB7929", "#D9D9D9"]
                ),
                expand=True
            )
        ]

    def handle_department_change(self, e):
        if self.department_dropdown.value == "Others":
            self.custom_department_field.visible = True
        else:
            self.custom_department_field.visible = False
            self.custom_department_field.value = ""
        self.page.update()

    def handle_create_account(self, e):
        first_name = self.first_name_field.value
        middle_name = self.middle_name_field.value
        last_name = self.last_name_field.value
        selected_dept = self.department_dropdown.value

        if not first_name or not last_name or not selected_dept:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please fill in all required fields."), open=True)
            self.page.update()
            return

        if selected_dept == "Others":
            dept_name = self.custom_department_field.value
            if not dept_name:
                self.page.snack_bar = ft.SnackBar(ft.Text("Please specify the department."), open=True)
                self.page.update()
                return
        else:
            dept_name = selected_dept

        db.connect()
        try:
            # Get or create department
            department, created = Department.get_or_create(
                name=dept_name,
                defaults={'initials': dept_name[:3].upper(), 'description': f"{dept_name} department"}
            )
            employee_id = str(uuid.uuid4())[:8]  # Generate short unique ID
            qr_code = str(uuid.uuid4())  # Generate QR code

            employee = Employee.create(
                employee_id=employee_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                department=department,
                qr_code=qr_code
            )
            print(f"Employee created: {employee.employee_id} - {employee.first_name} {employee.last_name}")

            # Generate QR code image
            qr_filename = f"{employee_id}_qr.png"
            generate_qr_code(qr_code, qr_filename)
            qr_image_path = f"assets/qr_codes/{qr_filename}"

            # Navigate to QR display page
            self.page.employee = employee
            self.page.qr_image_path = qr_image_path
            self.page.qr_filename = qr_filename
            self.page.go("/qr_display")
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error creating account: {str(ex)}"), open=True)
            self.page.update()
        finally:
            db.close()
