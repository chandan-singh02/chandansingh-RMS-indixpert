from app.auth.models.user import User
from app.utils.database_handler import get_users, save_users
from app.utils.otp_handler import generate_otp, verify_otp
from app.utils.id_generator import generate_id
from app.utils.validators import InputValidators
from app.utils.error_handler import ErrorHandler
from app.utils.log_handler import log_auth
from app.utils.app_error import AppError
import pwinput

from app.utils.colors import error, success, info, menu, user_input


class SignupService:

    @staticmethod    
    def signup():
        user_id = None

        try:
            info("\n==================================================")
            info("   USER SIGNUP                    ")
            info("==================================================\n")
           
            name = user_input("Full Name             : ")
            address = user_input("Address               : ")
            qualification = user_input("Qualification         : ")
            email = user_input("Email                 : ")
            password = pwinput.pwinput(prompt="Password                  :",mask="*")
            phone = user_input("Phone Number to Verify: ")

            InputValidators.validate_name(name)
            InputValidators.validate_name(address)
            InputValidators.validate_name(qualification) 
            InputValidators.validate_email(email)
            InputValidators.validate_password(password)
            InputValidators.validate_phone(phone)

            users = get_users()
            # print(users)

            for user in users:
                if user["email"] == email:
                    raise AppError("Email already exists! Please login","EMAIL_ALREADY_EXISTS")

                if user["phone"] == phone:
                    raise AppError("Phone number already exists! Please login","PHONE_NUMBER_ALREADY_EXISTS")
                
            info("\nSending OTP...")
            otp = generate_otp()
            info(f"OTP sent to {phone}: {otp}")

            if not verify_otp(otp):
                raise AppError("Invalid OTP","INVALID_OTP")

            new_user = User(generate_id("usr_"), name, email, password, phone)

            user_id = new_user.id

            save_users(new_user.convert_dict())

            success("\nYour account has been created successfully. Please log in.")

            log_auth("signup_success", user_id, "signup", "success")

        
        except Exception as e:
            log_auth("signup_failed", user_id, "signup", "failed")
            ErrorHandler.handle(e, user_id=None, module="auth", action="signup")