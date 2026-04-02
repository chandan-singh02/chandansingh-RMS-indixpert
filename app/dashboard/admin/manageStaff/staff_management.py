from app.utils.database_handler import get_users, update_users
from app.auth.models.user import User
from app.utils.session import CURRENT_USER
from app.utils.app_error import AppError
from app.utils.error_handler import ErrorHandler
from app.utils.session import CURRENT_USER
from app.utils.colors import error, success, info, menu, user_input

class StaffManager:

    def __init__(self):
        self.users = []

    def load_users(self):
        try:
            data = get_users()
            self.users = []

            for u in data:
                user_obj = User.from_dict(u)
                self.users.append(user_obj)

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="load_users")


    def save_users(self):
        try:
            data = []

            for u in self.users:
                data.append(u.convert_dict())

            update_users(data)

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="save_users")


    # ===== DISPLAY USERS =====
    def display_users(self):
        info("\n========== DISPLAY USERS LIST ==========")
        for u in self.users:
            print(u.id + " - " + u.name + " (" + u.role + ")")

    # ===== UPDATE ROLE =====
    def update_role(self):
        try:
            if CURRENT_USER["role"] != "admin":
                raise AppError("Access denined","ACCESS_DENIED")
                return

            self.load_users()

            if not self.users:
                raise AppError("users not found","USER_NOT_fOUND")
                return

            self.display_users()

            user_id = input("\nEnter user id: ")

            for user in self.users:
                if user.id == user_id:

                    new_role = input("Enter new role (admin/staff): ")

                    if new_role not in ["admin", "staff"]:
                        raise AppError("Invalid role","INVALID_ROLE")
                        return

                    user.role = new_role
                    success("Role updated")
                    break
            else:
                raise AppError("user not found","USER_NOT_FOUND")
                return

            self.save_users()

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="update_users")

    # ===== DELETE USER =====
    def delete_user(self):
        try:
            if CURRENT_USER["role"] != "admin":
                raise AppError("Access denined","ACCESS_DENIED")
                return

            self.load_users()
            self.display_users()

            user_id = input("Enter user id to delete: ")

            new_users = []
            found = False

            for user in self.users:
                if user.id != user_id:
                    new_users.append(user)
                else:
                    found = True

            if not found:
                raise AppError("user not found","USER_NOT_FOUND")
                return

            self.users = new_users
            self.save_users()

            success("User deleted")

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="delete_users")