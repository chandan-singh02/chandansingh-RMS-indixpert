import re
from app.utils.app_error import AppError

class InputValidators:

    @staticmethod
    def validate_required(value,field):
        value = value.strip()
        
        if not value:
            raise AppError(f"{field} field cannot be empty","VALIDATION_ERROR")

        if len(value) < 3:
            raise AppError(f"{field} must be atleast four characters","VALIDATION_ERROR")
        
        if re.search(r"(.)\1{3,}",value):
            raise AppError(f"{field} cannot contain the same character repeated 4 times","VALIDATION_ERROR")

    
    @staticmethod
    def validate_number(value,field,length=None):
        value = value.strip()

        if not value:
            raise AppError(f"{field} field cannot be empty","VALIDATION_ERROR")
        
        if not value.isdigit():
            raise AppError(f"{field} only contain numbers ","VALIDATION_ERROR")
        
        if length and len(value)!=length:
            raise AppError(f"{field} must be {length} digits","VALIDATION_ERROR")
        
        if re.search(r"(.)\1{3,}",value):
            raise AppError(f"{field}cannot contain the same  digit repeated 4 times","VALIDATION_ERROR")
        
        return int(value)


    @staticmethod
    def validate_name(name):
        if not name.replace(" ","").isalpha():
            raise AppError("Name must contain only characters","VALIDATION_ERROR")

        InputValidators.validate_required(name,"Name")
    
    @staticmethod
    def validate_email(email):
        InputValidators.validate_required(email,"E-mail")

        if "@" not in email or "." not in email:
            raise AppError("Invalid email format","VALIDATION_ERROR")
    
    @staticmethod
    def validate_phone(phone):
        InputValidators.validate_number(phone,"PhoneNumber",10)

    
    @staticmethod
    def validate_password(password):
        InputValidators.validate_required(password,"Password")



        




        
        



        
