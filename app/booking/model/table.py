class Table:
    def __init__(self, table_no, capacity):
        self.table_no = table_no
        self.capacity = capacity

    def to_dict(self):
        return {
            "table_no": self.table_no,
            "capacity": self.capacity
        }

    @staticmethod
    def from_dict(data):
        return Table(
            data.get("table_no"),
            data.get("capacity", 50)
        )