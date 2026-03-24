from app.utils.log_handler import log_error
from app.utils.app_error import AppError


from colorama import Fore,Style, init
init(autoreset=True)

class ErrorHandler:
    @staticmethod
    def handle(error,user_id=None,module="unknown",action="unknown"):

        log_error(user_id,error,module,action)

        if isinstance(error,AppError):
            print(Style.BRIGHT + Fore.RED + f"\n{str(error.message)}")
        else:
            print(Style.BRIGHT + Fore.RED + "\nSomething went wrong.Please try again later")

