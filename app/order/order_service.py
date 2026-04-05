from app.utils.database_handler import get_orders, save_orders, get_food_menu, get_bookings
from app.utils.id_generator import generate_id
from app.utils.session import CURRENT_USER
from app.utils.app_error import AppError
from app.utils.error_handler import ErrorHandler

from app.order.model.order import Order

import datetime
from app.utils.colors import error, success, info, menu, user_input
from app.utils.ui_helper import OrderViewer
class OrderService:

   
    @staticmethod
    def take_order():
        try:
            info("\n========== TAKE ORDER ==========")

            booking_id = input("Enter Booking ID: ")

            bookings = get_bookings()

            booking_found = None
            for b in bookings:
                if b["id"] == booking_id:
                    booking_found = b

            if booking_found is None:
                raise AppError("booking not found","VALIDATION_ERROR")

            today = datetime.date.today()
            now = datetime.datetime.now()

            booking_date = datetime.datetime.strptime(booking_found["date"], "%Y-%m-%d" ).date()

            end_time = datetime.datetime.strptime( booking_found["end_time"], "%I:%M %p"  )

            full_end = datetime.datetime.combine(booking_date, end_time.time())

            if full_end <= now:
                raise AppError("Booking time already finished","VALIDATION_ERROR")


            customer_name = booking_found["customer"]
            print("Customer name:", customer_name)

            items_list = []
            price_list = []

            menu_data = get_food_menu()

            while True:

                categories = menu_data.get("categories", [])

                info("\nselect Category:")
                i = 1
                for c in categories:
                    menu(str(i) + ". " + c)
                    i += 1

                choice = int(input("\nEnter category choice: "))

                if choice < 1 or choice > len(categories):
                    raise AppError("Invalid category selected","VALIDATION_ERROR")

                selected_category = categories[choice - 1]

                all_items = menu_data.get("menu", [])
                filtered_items = []

                info("\nItems:")
                i = 1
                for item in all_items:
                    if item["category"].lower() == selected_category.lower():
                        filtered_items.append(item)
                        menu(str(i) + ". " + item["name"])
                        i += 1

                if len(filtered_items) == 0:
                    raise AppError("No items found","VALIDATION_ERROR")

                item_choice = int(input("\nSelect item: "))

                if item_choice < 1 or item_choice > len(filtered_items):
                    raise AppError("Invalid item","VALIDATION_ERROR")

                selected_item = filtered_items[item_choice - 1]

                price_data = selected_item["price"]

                if "half" in price_data and "full" in price_data:
                    qty = input("Choose (half/full): ").lower()

                    if qty not in ["half", "full"]:
                        raise AppError("Invalid quantity","VALIDATION_ERROR")

                    price = price_data[qty]

                else:
                    qty = "single"
                    price = price_data["single"]

                items_list.append({selected_item["name"]: qty})
                price_list.append({selected_item["name"]: price})

                cont = input("add more items? (y/n): ").lower()
                if cont == "n":
                    break

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")

            order = Order(
                generate_id("ord_"),
                booking_id,
                customer_name,
                items_list,
                price_list,
                CURRENT_USER["name"],
                current_time
            )

            raw = get_orders()

            orders = []
            for d in raw:
                orders.append(Order.from_dict(d))

            orders.append(order)

            save_list = []
            for o in orders:
                save_list.append(o.to_dict())

            save_orders(save_list)

            success("\nOrder placed successfully!")
            success("Order ID:", order.id)

        except Exception as e:
            ErrorHandler.handle(e, CURRENT_USER["id"], "order", "take_order")


   
    @staticmethod
    def my_orders():
        try:
            info("\n========== MY ORDERS ==========")

            raw = get_orders()

            orders = []
            for d in raw:
                orders.append(Order.from_dict(d))

            found = False

            for o in orders:
                if o.staff == CURRENT_USER["name"]:
                    found = True
                    
                    OrderViewer.print_order_box(o)
                

            if not found:
                raise AppError("Order not found","VALIDATION_ERROR")

        except Exception as e:
            ErrorHandler.handle(e, CURRENT_USER["id"], "order", "my_order")


    @staticmethod
    def cancel_order():
        try:
            info("\n========== CANCEL ORDER ==========")

            order_id = input("Enter Order ID: ")

            raw = get_orders()

            orders = []
            for d in raw:
                orders.append(Order.from_dict(d))

            new_orders = []
            found = False

            for o in orders:
                if o.id == order_id:
                    found = True
                else:
                    new_orders.append(o)

            if not found:
                raise AppError("Order not found","VALIDATION_ERROR")

            save_list = []
            for o in new_orders:
                save_list.append(o.to_dict())

            save_orders(save_list)

            success("\nOrder cancelled successfully")

        except Exception as e:
            ErrorHandler.handle(e, CURRENT_USER["id"], "order", "cancel_order")