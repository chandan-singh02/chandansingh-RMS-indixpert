
from colorama import Fore, Style, init
init(autoreset=True)

def error(msg):
    print(Fore.RED + Style.BRIGHT + msg)

def success(msg):
    print(Fore.GREEN + Style.BRIGHT + msg)

def info(msg):
    print(Fore.CYAN + Style.BRIGHT + msg)

def menu(msg):
    print(Fore.YELLOW + Style.BRIGHT + msg)

def user_input(msg):
    return input(Fore.WHITE + msg)

