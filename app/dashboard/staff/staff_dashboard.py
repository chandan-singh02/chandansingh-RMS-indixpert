from app.utils.log_handler import log_app
from app.utils.colors import error, success, info, menu, user_input
from app.utils.database_handler import get_food_menu
from app.utils.session import CURRENT_USER
from app.menu.foodmenu_viewer import Menu
from app.booking.booking_service import BookingService
from app.order.order_service import OrderService
from app.billing.payment_service import PaymentService
class StaffDashboard:

    @staticmethod
    def show_dashboard():

        log_app("staff_dashboard_opened","dashboard") 
        BookingService.init_tables()

        while True:
            info("\n==================================================")
            info("   STAFF DASHBOARD                    ")
            info("==================================================\n")
            menu("1. View Menu")
            menu("2. Book Table")
            menu("3. View Booking")
            menu("4. Cancel Booking")
            menu("5. Take Order")
            menu("6. My Orders")
            menu("7. Cancel Order")
            menu("8. Take payment")
            menu("9. View Invoice")
            menu("10.Logout")

            choice = user_input("Select option: ")

            if choice == "1":
                Menu.view_menu()

            elif choice == "2":
                BookingService.book_table()

            elif choice == "3":
                BookingService.view_bookings()

            elif choice == "4":
                OrderService.cancel_booking()

            elif choice == "5":
                OrderService.take_order()

            elif choice == "6":
                OrderService.my_orders()
            
            elif choice == "7":
                OrderService.cancel_order()
            
            elif choice == "8":
                PaymentService.make_payment()
            
            elif choice == "9":
                PaymentService.show_invoice()
            

            elif choice == "10":
                info("Logging out...")

                CURRENT_USER["id"] =None
                CURRENT_USER["name"]=None
                CURRENT_USER["role"] =None

                log_app("staff_dashboard_closed")
                break

            else:
                error("Invalid option")
