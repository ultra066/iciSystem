import flet as ft
from database import db
from models.admin import Admin
from auth import check_admin_credentials, initialize_admin
from components.navigation import AdminNavigation
import bcrypt
import time

class AdminProfileView(ft.View):
    """
    The profile view for the admin.
    Displays credentials and allows for changing username and password.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/admin/profile"
        self.page.bgcolor = "#F0F2F5"
        self.admin_user = self.get_admin_user()

        self.name_value = ft.Text(self.admin_user.username, size=18)
        self.password_value = ft.Text("***********", size=18)
        
        self.username_field = ft.TextField(label="New Username", value=self.admin_user.username)
        self.password_field = ft.TextField(label="New Password", password=True, can_reveal_password=True)
        self.confirm_password_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True)

        self.change_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Change Credentials"),
            content=ft.Column(
                [
                    self.username_field,
                    self.password_field,
                    self.confirm_password_field
                ]
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_modal),
                ft.TextButton("Save", on_click=self.save_changes),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Create a large centered profile icon
        profile_icon = ft.CircleAvatar(
            content=ft.Icon(name=ft.Icons.PERSON, size=40, color="white"),
            radius=60,
            bgcolor=ft.Colors.DEEP_PURPLE_ACCENT_400
        )

        self.controls = [
            ft.Row(
                [
                    # Sidebar navigation
                    AdminNavigation(page=self.page),
                    # Main content area
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Admin Profile", size=36, weight="bold"),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            # Large centered profile icon
                                            ft.Container(
                                                content=profile_icon,
                                                alignment=ft.alignment.center,
                                                padding=ft.padding.only(bottom=20)
                                            ),
                                            
                                            # Name field
                                            ft.Row(
                                                [
                                                    ft.Text("Name:", size=18, weight="bold", width=100),
                                                    ft.Text("Admin 0", size=18),
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            ft.Divider(height=10, color="transparent"),
                                            
                                            # Initials field
                                            ft.Row(
                                                [
                                                    ft.Text("Initials:", size=18, weight="bold", width=100),
                                                    ft.Text("AAC", size=18),
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            ft.Divider(height=10, color="transparent"),
                                            
                                            # Username field
                                            ft.Row(
                                                [
                                                    ft.Text("Username:", size=18, weight="bold", width=100),
                                                    self.name_value
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            ft.Divider(height=10, color="transparent"),
                                            
                                            # Password field
                                            ft.Row(
                                                [
                                                    ft.Text("Password:", size=18, weight="bold", width=100),
                                                    self.password_value
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            ft.Divider(height=20, color="transparent"),
                                            
                                            # Change button
                                            ft.ElevatedButton(
                                                text="Change Credentials",
                                                on_click=self.open_modal,
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15)),
                                                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                                                )
                                            )
                                        ],
                                        alignment=ft.CrossAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    padding=ft.padding.all(40),
                                    border_radius=ft.border_radius.all(20),
                                    bgcolor=ft.Colors.TRANSPARENT,
                                    alignment=ft.alignment.center
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True
                        ),
                        padding=ft.padding.all(30),
                        expand=True
                    )
                ],
                expand=True
            )
        ]
    
    def get_admin_user(self):
        db.connect()
        try:
            return Admin.get(Admin.id == 1) # Assuming a single admin with ID 1
        except Admin.DoesNotExist:
            initialize_admin()
            return Admin.get(Admin.id == 1)
        finally:
            db.close()

    def open_modal(self, e):
        self.page.dialog = self.change_modal
        self.change_modal.open = True
        self.page.update()

    def close_modal(self, e):
        self.change_modal.open = False
        self.page.update()

    def save_changes(self, e):
        new_username = self.username_field.value
        new_password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        if new_password != confirm_password:
            self.page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match."), open=True)
            self.page.update()
            return

        db.connect()
        try:
            admin_record = Admin.get(Admin.id == 1)
            admin_record.username = new_username
            admin_record.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin_record.save()
            self.admin_user = self.get_admin_user() # Refresh user data
            self.name_value.value = self.admin_user.username
            self.page.snack_bar = ft.SnackBar(ft.Text("Credentials updated successfully!"), open=True)
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error saving changes: {ex}"), open=True)
        finally:
            db.close()
            self.close_modal(e)
