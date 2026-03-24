from app.utils.validators import InputValidators
from app.utils.database_handler import get_users
from app.utils.app_error import AppError
from app.utils.database_handler import get_users, save_users
from app.utils.otp_handler import generate_otp, verify_otp
from app.utils.log_handler import log_auth
from app.dashboard.staff.staff_dashboard import StaffDashboard
from app.dashboard.admin.admin_dashboard import AdminDashboard
from app.utils.app_error import AppError
from app.utils.session import CURRENT_USER
import pwinput

from app.utils.colors import error, success, info, menu, user_input


class SigninService:
    
    @staticmethod
    def signin():
        while True:
            info("\n==================================================")
            info("   USER LOGIN                    ")
            info("==================================================\n")
            
            menu("Choose Login Options")
            menu("1. Continue with Email")
            menu("2. Continue with Phone")
            menu("3. Back")

            choice = InputValidators.validate_number( user_input("Please select the option: "),"Login Option", 1)

            if choice == 1:
                SigninService.login_with_email()
            
            elif choice == 2:
                SigninService.login_with_phone()
            
            elif choice == 3:
                break
            
            else:
                error("Invalid option")
    
    @staticmethod
    def login_with_email():
        user_id = None  

        try:
            info("\n========== LOGIN WITH Email ==========")
            email = user_input("Enter your email: ")
            password = pwinput.pwinput(prompt="Enter your password: ",mask="*")

            InputValidators.validate_email(email)
            InputValidators.validate_password(password)

            users = get_users()

            for user in users:

                if user["email"] == email:
                    user_id = user["id"]   

                    if user["password"] != password:
                        raise AppError("Invalid password","INVALID_PASSWORD")

                    success(f"\nLogin successful! Welcome {user['name']}")

                    CURRENT_USER["id"] =user["id"]
                    CURRENT_USER["name"]=user["name"]
                    CURRENT_USER["role"] =user["role"]

                    log_auth("login_success", user_id,"login","success")

                    if user["role"] == "staff":
                         StaffDashboard.show_dashboard()
                    else:
                        AdminDashboard.show_dashboard()

                    return
           
            raise AppError("User not found Please signup first","USER_NOT_FOUND")
            

        except Exception as e:   
            log_auth("login_failed", user_id,"login","failed")
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="auth",action="login_with_email")

        
        
    @staticmethod
    def login_with_phone():
        user_id = None

        try:
            info("\n========== LOGIN WITH PHONE ==========")
            phone = user_input("Enter your phone number: ")

            InputValidators.validate_phone(phone)
            
            users = get_users()
            print("phone user",users)

            for user in users:
                if user["phone"] == phone:
                    user_id = user["id"]

                    info("\nSending OTP...")
                    otp = generate_otp()
                    info(f"OTP sent to {phone}: {otp}")

                    if not verify_otp(otp):
                        raise AppError("Invalid OTP","INVALID_OTP")
                    
                    success(f"\nLogin successful! Welcome {user['name']}")
                       
                    CURRENT_USER["id"] =user["id"]
                    CURRENT_USER["name"]=user["name"]
                    CURRENT_USER["role"] =user["role"]

                    log_auth("login_success",user_id,"login","success")

                    if user["role"] == "staff":
                        StaffDashboard.show_dashboard()
                        
                    elif user["role"] == "admin":
                        AdminDashboard.show_dashboard()
                    return
                         
        
            raise AppError("Phone number not found,Please signup first","USER_NOT_FOUND")
                   
        
        except Exception as e:
            log_auth("login_failed", user_id,"login","failed")
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="auth",action="login_with_phone")