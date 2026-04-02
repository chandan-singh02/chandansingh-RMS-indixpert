from app.booking.model.table import Table
from app.booking.model.booking import Booking
from app.utils.database_handler import get_bookings, save_bookings
from app.utils.app_error import AppError
from app.utils.id_generator import generate_id
import datetime
from app.utils.error_handler import ErrorHandler
from app.utils.colors import error, success, info, menu, user_input
from app.utils.session import CURRENT_USER
class BookingService:

    tables = []
    print("tables",tables)

    @staticmethod
    def init_tables():
        if len(BookingService.tables) > 0:
            print("booking service",BookingService.tables)
            print("tables",tables)
            return

        i = 1
        while i <= 30:
            BookingService.tables.append(Table(i, 50))
            i += 1
        print("after booking service",BookingService.tables)



    @staticmethod
    def validate_datetime(date_str, start_time, end_time):
        user_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.date.today()

        if user_date < today:
            raise AppError(" U cannot book past date","VALIDATION_ERROR")

        start_dt = datetime.datetime.strptime(start_time.upper(), "%I:%M %p")
        print("star time",start_dtf)
        end_dt = datetime.datetime.strptime(end_time.upper(), "%I:%M %p")

        if end_dt <= start_dt:
            raise AppError("End time must be after start time ","VALIDATION_ERROR")

        if user_date == today:
            now = datetime.datetime.now()
            full_start = datetime.datetime.combine(user_date, start_dt.time())

            if full_start <= now:
                raise AppError("start time already passed","VALIDATION_ERROR")

        duration = (end_dt - start_dt).seconds // 60
        return duration



    @staticmethod
    def is_active_booking(booking_date, end_time):
        today = datetime.date.today()
        now = datetime.datetime.now()

        booking_date = datetime.datetime.strptime(booking_date, "%Y-%m-%d").date()
        end_dt = datetime.datetime.strptime(end_time, "%I:%M %p")

        full_end = datetime.datetime.combine(booking_date, end_dt.time())

        #  booking already finished ignore this
        if full_end <= now:
            return False

        return True


  
    @staticmethod
    def get_available_tables(date, start_time, end_time):
        available = []

        raw = get_bookings()
        print("get booking ",raw)
        bookings = []

        for b in raw:
            bookings.append(Booking.from_dict(b))

        for table in BookingService.tables:
            used_seats = 0

            for b in bookings:
                if b.table_no == table.table_no:

                    if BookingService.is_active_booking(b.date, b.end_time):
                        used_seats += b.seats

            remaining = table.capacity - used_seats

            if remaining > 0:
                available.append({
                    "table_no": table.table_no,
                    "remaining_seats": remaining
                })

        return available



    @staticmethod
    def book_table():
        try:
            info("\n========== BOOK TABLE ==========")

            date = input("Enter date (YYYY-MM-DD): ")
            start_time = input("Start time (02:00 PM): ")
            end_time = input("End time (03:00 PM): ")

            duration = BookingService.validate_datetime(date, start_time, end_time)

            customer = input("Customer name: ")
            staff = input("Staff name: ")

            tables = BookingService.get_available_tables(date, start_time, end_time)

            if len(tables) == 0:
                raise AppError("no tables available","VALIDATION_ERROR")

            print("\nAvailable Tables:")
            for t in tables:
                print("Table", t["table_no"], ":", t["remaining_seats"],)

            table_no = int(input("Select table number: "))
            seats = int(input("Enter seats required: "))

            selected = None
            for t in tables:
                if t["table_no"] == table_no:
                    selected = t
                    # print("selected",selected)

            if selected is None:
                raise AppError("Invalid table selected","VALIDATION_ERROR")

            if seats > selected["remaining_seats"]:
                raise AppError("not enough seats available" ,"VALIDATION_ERROR")

            raw = get_bookings()
            bookings = []

            for b in raw:
                bookings.append(Booking.from_dict(b))

            new_booking = Booking(
                generate_id("tbl_"),
                table_no,
                date,
                start_time.upper(),
                end_time.upper(),
                customer,
                staff,
                seats,
                duration
            )

            bookings.append(new_booking)

            save_list = []
            for b in bookings:
                save_list.append(b.to_dict())

            save_bookings(save_list)

            print("Table booked successfully!")
            print("Booking ID:", new_booking.id)
            print("Duration:", duration, "minutes")

        except Exception as e:
            ErrorHandler.handle(e, user_id=None, module="booking", action="book_table")


    # ---------- VIEW BOOKINGS ----------
    @staticmethod
    def view_bookings():
        try:
            raw = get_bookings()

            if len(raw) == 0:
                print("No bookings")
                return

            print("\n--- BOOKINGS ---")

            for data in raw:
                b = Booking.from_dict(data)

                print("\n----------------")
                print("ID:", b.id)
                print("Table:", b.table_no)
                print("Date:", b.date)
                print("Time:", b.start_time, "-", b.end_time)
                print("Duration:", b.duration, "min")
                print("Customer:", b.customer)
                print("Staff:", b.staff)
                print("Seats:", b.seats)

        except:
            ErrorHandler.handle(e, user_id=None, module="booking", action="view_bookings")
     # ---------- CANCEL BOOKING ----------
    @staticmethod
    def cancel_booking():
        try:
            info("\n========== CANCEL BOOKING ==========")

            booking_id = input("Enter Booking ID: ")

            raw = get_bookings()

            if len(raw) == 0:
                raise AppError("No bookings found", "VALIDATION_ERROR")

            bookings = []
            for data in raw:
                bookings.append(Booking.from_dict(data))

            new_bookings = []
            found = False

            for b in bookings:
                if b.id == booking_id:
                    found = True
                else:
                    new_bookings.append(b)

            if not found:
                raise AppError(" Booking not found", "VALIDATION_ERROR")


            save_list = []
            for b in new_bookings:
                save_list.append(b.to_dict())

            save_bookings(save_list)

            success(" Booking cancelled successfully")

        except Exception as e:
            ErrorHandler.handle(e, user_id=None, module="booking", action="cancel_booking")
    


    