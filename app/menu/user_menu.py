from app.auth.services.signup_service import SignupService
from app.auth.services.signin_service import SigninService
from app.utils.validators import InputValidators
from app.utils.log_handler import log_app
from app.utils.error_handler import ErrorHandler

from app.utils.colors import error, success, info, menu, user_input


class UserMenu:
    
    @staticmethod
    def show_user_menu():

        log_app("main_menu_opened","menu") 

        while True:
            info("\n+==========================================================+")
            info("|                     QUICKSERVE RMS                      |")
            info("|             Seamless Service in Every Order             |")
            info("+==========================================================+\n")

            menu("1. Signup")
            menu("2. Login")
            menu("3. Exit")

            try:
                choice = InputValidators.validate_number( user_input("Please select the option: "),"Menu Choice",1)

                if choice == 1:
                    SignupService.signup()
            
                elif choice == 2:
                    SigninService.signin() 
            
                elif choice == 3:
                    error("\nExiting...")
                    info("See you soon")
                    log_app("application_exit","menu") 
                    break
            
                else:
                    error("Invalid choice")
            
            except Exception as e:
                ErrorHandler.handle(e, user_id=None, module="menu", action="show_menu")