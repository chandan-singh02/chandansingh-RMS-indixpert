class Report:

    def __init__(self):
        self.total_revenue = 0
        self.total_bookings = 0
        self.dish_count = {}

    def add_payment(self, payment):
        self.total_revenue += payment.get("total_amount", 0)
        self.total_bookings += 1

        items = payment.get("ordered_items", [])

        for item in items:
            for dish in item:
                self.dish_count[dish] = self.dish_count.get(dish, 0) + 1

    def get_most_ordered(self):
        max_count = 0
        dish_name = None

        for dish in self.dish_count:
            if self.dish_count[dish] > max_count:
                max_count = self.dish_count[dish]
                dish_name = dish

        return dish_name, max_count