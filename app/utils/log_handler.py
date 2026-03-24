import json
import os
from datetime import datetime
from app.utils.id_generator import generate_id
from app.utils.app_error import AppError

APP_LOG_FILE = "app/logs/app.json"
AUTH_LOG_FILE = "app/logs/auth.json"
ERROR_LOG_FILE = "app/logs/error.json"


def store_log(file_path, record):

    if not os.path.exists(file_path):
        data = []
    else:
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except:
                data = []

    data.append(record)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)




#app log operations
def log_app(event,module):
    store_log(APP_LOG_FILE,{
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event":event,
        "module":module
    })
    

def log_auth(event,user_id=None,action=None,status="success"):
    store_log(AUTH_LOG_FILE,{
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event":event,
        "user_id":user_id,
        "module":"auth",
        "action":action,
        "status":status
    })


def log_error(user_id,error,module,action):
    
    if isinstance(error,AppError):
        message = error.message
        error_type = error.error_type
    else:
        message =str(error)
        error_type = type(error).__name__ 

    store_log(ERROR_LOG_FILE,{
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "error_id":generate_id("err"),
        "user_id":user_id,
        "message":message,
        "error_type":error_type,
        "module":module,       
        "action":action,
        "status":"failed",        
        "execution_time_ms":"110",
        "environment":"development",
        "version":"v2.4.0"
    })

 
