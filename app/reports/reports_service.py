
from app.utils.colors import error, success, info, menu, user_input

from app.utils.database_handler import get_payments
from app.utils.app_error import AppError
from app.utils.error_handler import ErrorHandler
from app.reports.model.reports import Report


class ReportService:

    @staticmethod
    def report_menu():
        try:
            info("\n====== REPORT MENU ======")
            menu("1. Total Revenue")
            menu("2. Total Bookings")
            menu("3. Most Ordered Dish")
            menu("4. Back")

            choice = int(input("Enter choice: "))

            payments = get_payments()

            if not payments:
                raise AppError("No payment data found", "DataError")

            report = Report()

            for payment in payments:
                report.add_payment(payment)

            if choice == 1:
                print("\nTotal Revenue:", report.total_revenue)

            elif choice == 2:
                print("\nTotal Bookings:", report.total_bookings)

            elif choice == 3:
                dish, count = report.get_most_ordered()
                print("\nMost Ordered Dish:", dish)
                print("Ordered Times      :", count)

            elif choice == 4:
                return

            else:
                print("Invalid choice")

        except Exception as e:
            ErrorHandler.handle(e, module="report", action="report_menu")