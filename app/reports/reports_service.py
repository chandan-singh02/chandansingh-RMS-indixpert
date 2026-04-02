from app.utils.database_handler import get_payments
from app.utils.app_error import AppError
from app.utils.error_handler import ErrorHandler
from app.reports.model.reports import Report
from app.utils.colors import error, success, info, menu, user_input


class ReportService:

    @staticmethod
    def report_menu():
        try:
            print("\n====== REPORT MENU ======")
            print("1. Total Revenue")
            print("2. Total Bookings")
            print("3. Most Ordered Dish")
            print("4. Back")
            print("=========================")

            choice = int(input("Enter choice: "))

            payments = get_payments()

            if not payments:
                raise AppError("no payment data found", "DataError")

            report = Report()

            for payment in payments:
                report.add_payment(payment)


            if choice == 1:
                print("\nTotal Revenue:", report.total_revenue)

            elif choice == 2:
                print("\nTotal Bookings")

            elif choice == 3:
            
                print("Ordered Times:")

            elif choice == 4:
                return

            else:
                print("Invalid choice")

        except Exception as e:
            ErrorHandler.handle(e, module="report", action="report_menu")