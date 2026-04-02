class Payment:

    def __init__(self, payment_id, order_id, customer_name,
                 ordered_items, total_amount, payment_method,
                 booking_duration, seats, seat_charge, date):

        self.payment_id = payment_id
        self.order_id = order_id
        self.customer_name = customer_name
        self.ordered_items = ordered_items
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.booking_duration = booking_duration
        self.seats = seats
        self.seat_charge = seat_charge
        self.date = date

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "ordered_items": self.ordered_items,
            "total_amount": self.total_amount,
            "payment_method": self.payment_method,
            "booking_duration": self.booking_duration,
            "seats": self.seats,
            "seat_charge": self.seat_charge,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Payment(
            data["payment_id"],
            data["order_id"],
            data["customer_name"],
            data["ordered_items"],
            data["total_amount"],
            data["payment_method"],
            data["booking_duration"],
            data["seats"],
            data["seat_charge"],
            data["date"]
        )