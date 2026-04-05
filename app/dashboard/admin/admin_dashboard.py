
from app.dashboard.admin.manageMenu.menu_service import MenuService
from app.dashboard.admin.manageStaff.staff_management import StaffManager
from app.menu.foodmenu_viewer import Menu
from app.utils.validators import InputValidators
from app.utils.colors import error, success, info, menu, user_input
from app.utils.error_handler import ErrorHandler
from app.utils.session import CURRENT_USER
from app.reports.reports_service import ReportService
from app.dashboard.admin.manageTables.tables_service import TableService
class AdminDashboard:

    @staticmethod
    def show_dashboard():
        try:
            
            while True:
                info("\n==================================================")
                info("   ADMIN DASHBOARD                    ")
                info("==================================================\n")
                menu("1. Manage Menu")
                menu("2. Manage Staff")
                menu("3. Manage Tables")
                menu("4. Reports")
                menu("5. Exit")

                choice = InputValidators.validate_number(input("Please select the option: "),"ADMIN DASHBOARD OPTIONS", 1) 

                if choice == 1:
                    AdminDashboard.manage_menu()

                elif choice == 2:
                    AdminDashboard.manage_staff() 


                elif choice == 3:
                    AdminDashboard.manage_tables()
       

                elif choice == 4:
                    ReportService.report_menu()

                elif choice == 5:
                    print("Logging out...")
                    break

                else:
                    print("Invalid option")
        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="show_dashboard")





    @staticmethod
    def manage_menu():
        try:
            service = MenuService()
            while True:
                info("\n========== MANAGE MENU ==========")
                menu("1. View Menu")
                menu("2. Add Item")
                menu("3. Update Item")
                menu("4. Delete Item")
                menu("5. Add New Category")
                menu("6. Delete Category")
                menu("7. Back")


                choice = InputValidators.validate_number(input("Please select the option: "),"MANAGE MENU OPTIONS", 1) 

                if choice == 1:
                    Menu.view_menu()

                elif choice == 2:
                    service.add_item()

                elif choice == 3:
                    service.update_item()
               

                elif choice == 4:
                    service.delete_item()

                elif choice == 5:
                    service.add_category()
            
                elif choice == 6:
                    service.delete_category()
            
                elif choice == 7:
                    break

                else:
                    menu("Invalid option")
        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="manage_menu")

    @staticmethod
    def manage_staff():
        try:
            service = StaffManager()
            while True:
                info("\n========== MANAGE Staff ==========")
                menu("1. View Staff")
                menu("2. Promote Staff to Admin")
                menu("3. Delete Staff")
                menu("4. Back")


                choice = InputValidators.validate_number(input("Please select the option: "),"MANAGE STAFF OPTIONS", 1) 

                if choice == 1:
                    service.load_users()
                    service.display_users()

                elif choice == 2:
                    service.update_role()

                elif choice == 3:
                    service.delete_staff()
                
                elif choice == 4:
                    break

                else:
                    menu("Invalid option")
        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="manage_staff")


    
  


    @staticmethod
    def manage_tables():
        table_service = TableService()

        while True:
            info("\n========== MANAGE Tables ==========")
            print("1. Add Table")
            print("2. Delete Table")
            print("3. Update Table")
            print("4. View Tables")
            print("5. Back")

            choice = InputValidators.validate_number(input("Please select the option: "),"MANAGE TABLE OPTIONS", 1) 

            try:
                if choice == 1:
                    table_service.add_table()

                elif choice == 2:
                    table_service.delete_table()

                elif choice == 3:
                    table_service.update_table()

                elif choice == 4:
                    table_service.view_tables()

                elif choice == 5:
                    break

                else:
                    print("Invalid choice")

            except AppError as e:
                ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="manage_tables")

    



    

    