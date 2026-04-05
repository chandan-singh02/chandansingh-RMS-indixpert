from app.dashboard.models.tables import Table
from app.booking.model.booking import Booking
from app.utils.app_error import AppError
from app.utils.database_handler import ( get_tables, save_tables,get_bookings, save_bookings)
import datetime
from app.utils.error_handler import ErrorHandler
from app.utils.session import CURRENT_USER

from app.utils.colors import error, success, info, menu, user_input
from app.utils.id_generator import generate_id
from app.utils.validators import InputValidators


class DataRepository:

    def __init__(self):
        self.tables = []
        self.bookings = []
        self.load_data()

    def load_data(self):
        self.tables = get_tables()
        self.bookings = get_bookings()

    def save_tables(self):
        save_tables(self.tables)

    def save_bookings(self):
        save_bookings(self.bookings)



class BookingService:

    def __init__(self):
        self.repo = DataRepository()

  
    def validate_datetime(self, date_str, start_time, end_time):
      
        user_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.date.today()

        if user_date < today:
            raise AppError("Past date not allowed", "VALIDATION_ERROR")

        start_dt = datetime.datetime.strptime(start_time.upper(), "%I:%M %p")
        end_dt = datetime.datetime.strptime(end_time.upper(), "%I:%M %p")

        if end_dt <= start_dt:
            raise AppError("End must be after start time ", "VALIDATION_ERROR")


            
        if user_date == today:
            now = datetime.datetime.now()
            full_start = datetime.datetime.combine(user_date, start_dt.time())

            if full_start <= now:
                raise AppError("start time is already passed","VALIDATION_ERROR")

        duration = (end_dt - start_dt).seconds // 60
        return duration


    def is_active_booking(self, booking_date, end_time):
        now = datetime.datetime.now()

        b_date = datetime.datetime.strptime(booking_date, "%Y-%m-%d").date()
        end_dt = datetime.datetime.strptime(end_time.upper(), "%I:%M %p")

        full_end = datetime.datetime.combine(b_date, end_dt.time())

        if full_end > now:
            return True

        return False

 
    def get_available_tables(self):

        available = []

        for t in self.repo.tables:
            table = Table.from_dict(t)

            used_seats = 0

            for b in self.repo.bookings:
                booking = Booking.from_dict(b)

                if booking.table_no == table.table_no:
                    if self.is_active_booking(booking.date, booking.end_time):
                        used_seats = used_seats + booking.seats

            remaining = table.capacity - used_seats

            if remaining > 0:
                available.append({
                    "table_no": table.table_no,
                    "remaining_seats": remaining
                })

        return available


    def book_table(self):
        try:
            info("\n========== BOOK TABLE ==========")

            date =  input("Date (YYYY-MM-DD): ")
            start = input("Start time (02:00 PM): ")
            end =   input("End time (03:00 PM): ")

            duration = self.validate_datetime(date, start, end)

            customer = input("Customer name: ")
            staff = CURRENT_USER["name"]
            print("Staff name who booked:",staff)

            available = self.get_available_tables()

            if len(available) == 0:
                raise AppError("No tables available", "VALIDATION")

            menu("\nAvailable Tables:")
            for t in available:
                print("Table:", t["table_no"], "Seats:", t["remaining_seats"])
            
            table_no = InputValidators.validate_number(input("Select table no : "),"Table")
            seats = InputValidators.validate_number(input("Select seats u want: "),"Seats")

            selected = None

            for t in available:
                if t["table_no"] == table_no:
                    selected = t

            if selected is None:
                raise AppError("Invalid table", "VALIDATION")

            if seats > selected["remaining_seats"]:
                raise AppError("Not enough seats", "VALIDATION")

            new_booking = Booking(
                generate_id("tbl_"),
                table_no,
                date,
                start.upper(),
                end.upper(),
                customer,
                staff,
                seats,
                duration
            )

            self.repo.bookings.append(new_booking.to_dict())
            self.repo.save_bookings()

            success("\nBooking successfully done!")

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="booking",action="book_table")


    def view_bookings(self):
        try:
            if len(self.repo.bookings) == 0:
                print("No bookings")
                return

            info("\n========== VIEW BOOKINGS ==========")

            for data in self.repo.bookings:
                b = Booking.from_dict(data)

                menu("------------------------------")
                print("Booking ID   :", b.id)
                menu("------------------------------")
                print("Customer name:",b.customer)
                print("Table no.    :",b.table_no)
                print("Seats booked :",b.seats)
                print("Date         :",b.date)
                print("Start time   :",b.start_time)
                print("End time:    :",b.end_time)
                print("Duration     :",b.duration)


        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="booking",action="view_bookings")

 
    def cancel_booking(self):
        try:
            booking_id = input("Enter booking id: ")

            new_list = []
            found = False

            for b in self.repo.bookings:
                if b["id"] == booking_id:
                    found = True
                else:
                    new_list.append(b)

            if not found:
                raise AppError("Booking not found", "VALIDATION")

            self.repo.bookings = new_list
            self.repo.save_bookings()

            success("Booking cancelled")

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="booking",action="cancel_booking")