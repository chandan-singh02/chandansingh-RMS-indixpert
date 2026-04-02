import json
import os

USERS_DB_PATH = "app/database/users.json"
FOOD_MENU_PATH = "app/database/food_menu.json"
BOOKED_TABLE_PATH ="app/database/booked_table.json"
CUSTOMER_ORDER_PATH = "app/database/customer_order.json"
PAYMENT_PATH = "app/database/payment.json"


def load_data(file_path):

    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return []

    with open(file_path, "r",encoding="utf-8") as file:

        try:
            return json.load(file)
        except Exception as e:
            print("JSON ERROR:", e)
            return []

def save_data(file_path, data):
    print("Save data function start")

    with open(file_path, "w",encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        print("Save data function inside")
    print("save data function ending")


def append_data(file_path, record):

    data = load_data(file_path)

    data.append(record)

    save_data(file_path, data)


#USER DATABASE OPERATIONS

def get_users():
    return load_data(USERS_DB_PATH)

def save_users(user_record):
    append_data(USERS_DB_PATH,user_record)

def update_users(users): #for updating
    save_data(USERS_DB_PATH,users)

#FOOD MENU OPERATIONS
def get_food_menu():
    return load_data(FOOD_MENU_PATH)


def save_food_menu(food_menu_record):
    print("save food menu database handler")
    save_data(FOOD_MENU_PATH,food_menu_record)


#booking operations
def get_bookings():
    return load_data(BOOKED_TABLE_PATH)


def save_bookings(bookings):
    save_data(BOOKED_TABLE_PATH, bookings)


#order operations
def get_orders():
    return load_data(CUSTOMER_ORDER_PATH)


def save_orders(orders):
    save_data(CUSTOMER_ORDER_PATH, orders)

#payment operations

def get_payments():
    return load_data(PAYMENT_PATH)

def save_payments(payments):
    save_data(PAYMENT_PATH, payments)



