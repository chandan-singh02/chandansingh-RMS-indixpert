from app.utils.database_handler import get_pricing, save_pricing

class Pricing:

    @staticmethod
    def update_seat_price():
        pricing = get_pricing()

        price = int(input("Enter new seat price: "))
        pricing["seat_price"] = price

        save_pricing(pricing)
        print("Seat price updated")

    @staticmethod
    def update_gst():
        pricing = get_pricing()

        gst = int(input("Enter GST %: "))
        pricing["gst_percent"] = gst

        save_pricing(pricing)
        print("GST updated")