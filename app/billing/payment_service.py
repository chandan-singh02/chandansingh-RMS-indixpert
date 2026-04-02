from app.utils.database_handler import (
    get_orders, get_bookings,
    get_payments, save_payments
)
from app.utils.app_error import AppError
from app.utils.error_handler import ErrorHandler
from app.utils.id_generator import generate_id
from app.billing.model.payment import Payment

import datetime
from app.utils.colors import error, success, info, menu, user_input

class PaymentService:
    @staticmethod
    def make_payment():
        try:
            info("\n========== MAKE PAYMENT ==========")

            order_id = input("Enter Order ID: ")

            orders = get_orders()
            order = None

            for o in orders:
                if o["id"] == order_id:
                    order = o

            if order is None:
                raise AppError("Order not found","NOT FOUND")


            payments = get_payments()
            for p in payments:
                if p["order_id"] == order_id:
                    raise AppError("Payment already done for this order","PAYMENT_DONE")

            total_amount = 0
            for item in order["prices"]:
                for key in item:
                    total_amount += int(item[key])


            bookings = get_bookings()
            booking = None

            for b in bookings:
                if b["id"] == order["booking_id"]:
                    booking = b

            if booking is None:
                raise AppError("Booking not found","NOT_FOUND")

            seats = booking["seats"]
            duration = booking["duration"]

            seat_charge = seats * 50
        

            final_total = total_amount + seat_charge

            payment_method = input("Enter payment method (UPI/Cash): ")

            payment = Payment(
                generate_id("pay"),
                order_id,
                order["customer_name"],
                order["prices"],
                final_total,
                payment_method,
                duration,
                seats,
                seat_charge,
                str(datetime.datetime.now())
            )

            payments.append(payment.to_dict())
            save_payments(payments)

            print("\nPayment Successful!")
            print("Payment ID:", payment.payment_id)

        except Exception as e:
            ErrorHandler.handle(e, module="payment", action="make_payment")



    @staticmethod
    def show_invoice():
        try:
            info("\n========== INVOICE ==========")

            payment_id = input("Enter Payment ID: ")

            payments = get_payments()
            payment = None

            for p in payments:
                if p["payment_id"] == payment_id:
                    payment = Payment.from_dict(p)

            if payment is None:
                raise AppError("Payment not found", "VALIDATION_ERROR")

            print("\n===================================")
            print("      Quick Serve Restaurant")
            print("===================================")

            print("Payment Date:", payment.date)
            print("-----------------------------------")

            print("\nITEMS:")
            dish_total = 0

            for item in payment.ordered_items:
                for name in item:
                    price =item[name]
                    dish_total += price
                    print(f"{name}---> Rs {price}")
            print("\n-----------------------------------")
            print("Dish Total:", dish_total)

            print("Seat Charge:", payment.seat_charge)

            time_charge = payment.booking_duration * 2
            print("Time Charge:", time_charge)

            sub_total = dish_total + payment.seat_charge + time_charge

            
            gst = sub_total * 0.025

            
            print("GST:", round(cgst, 2))

            total = sub_total + sgst + gst

            print("\nTOTAL:", round(total, 2))
            print("===================================")

        
        except Exception as e:
            ErrorHandler.handle(e, module="payment", action="show_invoice")


