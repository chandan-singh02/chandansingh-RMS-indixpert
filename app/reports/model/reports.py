class Report:

    def __init__(self):
        self.total_revenue = 0
        self.total_bookings = 0
        self.dish_count = {}

    def add_payment(self, payment):
        self.total_revenue += payment.get("total_amount", 0)



