import re
from app.utils.app_error import AppError

class InputValidators:

    @staticmethod
    def validate_required(value=None,field=None):
        value = value.strip()
        
        if not value:
            raise AppError(f"{field} field cannot be empty","VALIDATION_ERROR")

        # if len(value) < 4:
        #     raise AppError(f"{field} must be atleast three characters","VALIDATION_ERROR")
        
        if re.search(r"(.)\1{3,}",value):
            raise AppError(f"{field} cannot contain the same character repeated 4 times","VALIDATION_ERROR")

    
    @staticmethod
    def validate_number(value=None,field=None,length=None):
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
    def validate_name(name,field="Name"):
        InputValidators.validate_required(name,field)
        if not name.replace(" ","").isalpha():
            raise AppError(f"{field} must contain only characters","VALIDATION_ERROR")

        
    
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


    


    @staticmethod
    def validate_price(value,field="Price"):
        value = value.strip()

        if not value:
            raise AppError(f"{field} can't be empty","VALIDATION_ERROR")
        
        if not value.isdigit():
            raise AppError(f"{field} must be numbers")
        
        price = int(value)
        
        if price <= 0:
            raise AppError(f"{field} must be greater than 0","VALIDATION_ERROR") 

        return price
    
    @staticmethod
    def validate_price_relation(half,full):
        if full <= half:
            raise AppError("Full price must be greater than half price","VALIDATION_ERROR")





        




        
        



        
