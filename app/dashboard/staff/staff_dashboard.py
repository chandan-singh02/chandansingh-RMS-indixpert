from app.utils.log_handler import log_app
from app.utils.colors import error, success, info, menu, user_input
from app.utils.database_handler import get_food_menu
from app.utils.session import CURRENT_USER
from app.menu.foodmenu_viewer import MenuViewer
class StaffDashboard:

    @staticmethod
    def show_dashboard():

        log_app("staff_dashboard_opened","dashboard") 

        while True:
            info("\n==================================================")
            info("   STAFF DASHBOARD                    ")
            info("==================================================\n")
            menu("1. View Menu")
            menu("2. Take Order")
            menu("3. My Orders")
            menu("4. Cancel Order")
            menu("5. View Invoice")
            menu("6. View Profile")
            menu("7. Logout")

            choice = user_input("Select option: ")

            if choice == "1":
                MenuViewer.view_menu()

            elif choice == "2":
                StaffDashboard.take_order()

            elif choice == "3":
                StaffDashboard.my_orders()

            elif choice == "4":
                StaffDashboard.cancel_order()

            elif choice == "5":
                StaffDashboard.view_invoice()

            elif choice == "6":
                StaffDashboard.view_profile()

            elif choice == "7":
                info("Logging out...")

                CURRENT_USER["id"] =None
                CURRENT_USER["name"]=None
                CURRENT_USER["role"] =None

                log_app("staff_dashboard_closed")
                break

            else:
                error("Invalid option")


 
        
       




    @staticmethod
    def take_order():
        info("Taking Order")

    @staticmethod
    def my_orders():
        info("Showing My Orders")

    @staticmethod
    def cancel_order():
        info("Cancel Order")

    @staticmethod
    def view_invoice():
        info("View Invoice")

    @staticmethod
    def view_profile():
        info("View Profile")