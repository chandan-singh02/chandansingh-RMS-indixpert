class Order:

    def __init__(self, id, booking_id, customer_name, items, prices, staff, date):
        self.id = id
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.items = items
        self.prices = prices
        self.staff = staff
        self.date = date

    def to_dict(self):
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "customer_name": self.customer_name,
            "items": self.items,
            "prices": self.prices,
            "staff": self.staff,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Order(
            data["id"],
            data["booking_id"],
            data["customer_name"],
            data["items"],
            data["prices"],
            data["staff"],
            data["date"]
        )