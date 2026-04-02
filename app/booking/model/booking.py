class Booking:
    def __init__(self, id, table_no, date, start_time, end_time, customer, staff, seats, duration):
        self.id = id
        self.table_no = table_no
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.customer = customer
        self.staff = staff
        self.seats = seats
        self.duration = duration

    def to_dict(self):
        return {
            "id": self.id,
            "table_no": self.table_no,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "customer": self.customer,
            "staff": self.staff,
            "seats": self.seats,
            "duration": self.duration
        }

    @staticmethod
    def from_dict(data):
        return Booking(
            data.get("id"),
            data.get("table_no"),
            data.get("date"),
            data.get("start_time"),
            data.get("end_time"),
            data.get("customer"),
            data.get("staff"),
            data.get("seats"),
            data.get("duration", 0)
        )