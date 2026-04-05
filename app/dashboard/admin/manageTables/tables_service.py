from app.utils.app_error import AppError
from app.utils.database_handler import ( get_tables, save_tables,get_bookings)
from app.dashboard.models.tables import Table
from app.utils.error_handler import ErrorHandler
from app.utils.session import CURRENT_USER

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



class TableService:

    MAX = 10

    def __init__(self):
        self.repo = DataRepository()


    def add_table(self):
        try:
            self.repo.load_data()

            table_no = int(input("Table no: "))
            capacity = int(input("Capacity: "))

            if capacity <= 0 or capacity > self.MAX:
                raise AppError("Capacity must be 1 to 10", "VALIDATION")


            for t in self.repo.tables:
                table = Table.from_dict(t)
                if table.table_no == table_no:
                    raise AppError("Table already exists", "VALIDATION")

            new_table = Table(table_no, capacity)
            self.repo.tables.append(new_table.to_dict())

            self.repo.save_tables()
            success(f"Table {table_no} added")

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admin",action="add_table")


    def delete_table(self):
        try:
            self.repo.load_data()

            table_no = int(input("Table no: "))

           
            for b in self.repo.bookings:
                if b["table_no"] == table_no:
                    raise AppError("Bookings exist for this table", "VALIDATION")

            new_list = []
            found = False

            for t in self.repo.tables:
                table = Table.from_dict(t)

                if table.table_no == table_no:
                    found = True
                else:
                    new_list.append(t)

            if not found:
                raise AppError("Table not found", "VALIDATION")

            self.repo.tables = new_list
            self.repo.save_tables()

            success(f"Table {table_no} deleted")

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admin",action="delete_table")



    def update_table(self):
        try:
            self.repo.load_data()

            table_no = int(input("Table no: "))
            new_capacity = int(input("New capacity: "))

            if new_capacity <= 0 or new_capacity > self.MAX:
                raise AppError("Capacity must be 1 to 10", "VALIDATION")

       
            used = 0
            for b in self.repo.bookings:
                if b["table_no"] == table_no:
                    used = used + b["seats"]

            found = False

            for i in range(len(self.repo.tables)):
                table = Table.from_dict(self.repo.tables[i])

                if table.table_no == table_no:
                    found = True

                    if new_capacity < used:
                        raise AppError(
                            f"Already {used} seats booked",
                            "VALIDATION"
                        )

            
                    table.capacity = new_capacity
                    self.repo.tables[i] = table.to_dict()

            if not found:
                raise AppError("Table not found", "VALIDATION")

            self.repo.save_tables()
            success(f"Table {table_no} updated")

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admin",action="update_table")


    # -------- VIEW --------
    def view_tables(self):
        try:
            self.repo.load_data()

            if len(self.repo.tables) == 0:
                raise AppError("No tables found", "NOT_FOUND")
                return

            print("\n--- TABLES ---")

            for t in self.repo.tables:
                table = Table.from_dict(t)
                print("Table:", table.table_no, "| Capacity:", table.capacity)

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admin",action="view_table")
