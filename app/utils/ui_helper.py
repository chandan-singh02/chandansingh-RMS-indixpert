from app.utils.colors import error, success, info, menu, user_input,menus,restaurant_color,sub_headings
class MenuViewer:

    WIDTH = 84

    @classmethod
    def print_line(cls):
       print(menus("+" + "-" * cls.WIDTH + "+"))

    @classmethod
    def print_center(cls,text):
        print(menus("|" + text.center(cls.WIDTH) + "|"))

    @classmethod
    def display_header(cls,data):
        res = data.get("restaurant", {})

        print("\n+" + "-" * cls.WIDTH + "+")
        print("|" + restaurant_color(res.get("name", "").upper().center(cls.WIDTH)) + "|")
        print("|" + sub_headings(res.get("location", "").center(cls.WIDTH)) + "|")
        print("|" + sub_headings(res.get("contact", "").center(cls.WIDTH)) + "|")
        print("+" + "-" * cls.WIDTH + "+")


    @classmethod
    def print_box(cls,title, items):
        if not items:
            return

        width = cls.WIDTH

        cls.print_center(title.upper())
        cls.print_line()

        # column sizes
        name_w = 24
        type_w = 15
        half_w = 8
        full_w = 8
        price_w = 10
        tag_w = 5

        header = (
         menus(f"{'DISH':<{name_w}}")+
         menus(f"{'TYPE':<{type_w}}")+
         menus(f"{'HALF':<{half_w}}")+
         menus(f"{'FULL':<{full_w}}")+
         menus(f"{'PRICE':<{price_w}}")+
         menus(f"{'TAGS':<{tag_w}}")
        )

        print("|" + header.ljust(width) + "")
        cls.print_line()

        # ===== ROWS =====
        for item in items:
            tags =  item.tags or ""

            row = (
                f"{item.name:<{name_w}}"
                f"{item.food_type:<{type_w}}"
                f"{str(item.get_half()):<{half_w}}"
                f"{str(item.get_full()):<{full_w}}"
                f"{str(item.get_single()):<{price_w}}"
                f"{tags:<{tag_w}}"
            )

            print("|" + row.ljust(width) + "|")

        cls.print_line()
    

class OrderViewer(MenuViewer):

    WIDTH = 50
    @classmethod
    def print_order_box(cls,order):
        # WIDTH = MenuViewer.WIDTH
    

        print("\n")
        cls.print_line()
        cls.print_center("ORDER DETAILS")
        cls.print_line()

       
        print(f"| Order ID : {order.id}".ljust(cls.WIDTH) + "|")
        print(f"| Customer : {order.customer_name}".ljust(cls.WIDTH) + "|")
        print(f"| Date     : {order.date}".ljust(cls.WIDTH) + "|")
 
        cls.print_line()

      
        print("| Items:".ljust(cls.WIDTH) + "|")

        count = 1
        for item in order.items:
            for name, size in item.items():
                line = f"{count}. {name} ({size.capitalize()})"
                print(f"| {line}".ljust(cls.WIDTH) + "|")
                count += 1

        cls.print_line()


class InvoiceViewer(MenuViewer):
    WIDTH = 60   

    @classmethod
    def print_invoice(cls, payment):
        print("\n")

        cls.print_line()
        cls.print_center("Quick Serve Restaurant")
        cls.print_center("PAYMENT INVOICE")
        cls.print_line()

        print(f"| Payment ID : {payment.payment_id}".ljust(cls.WIDTH) + "|")
        print(f"| Customer   : {payment.customer_name}".ljust(cls.WIDTH) + "|")
        print(f"| Date       : {payment.date}".ljust(cls.WIDTH) + "|")

        cls.print_line()

        info("| Items:".ljust(cls.WIDTH) + "|")

        dish_total = 0

        for item in payment.ordered_items:
            for name in item:
                price = item[name]
                dish_total += price
                line = f"{name}    : ₹{price}"
                print(f"| {line}".ljust(cls.WIDTH) + "|")

        cls.print_line()

     
        print(f"| Dish Total  : ₹{dish_total}".ljust(cls.WIDTH) + "|")
        print(f"| Seat Charge : ₹{payment.seat_charge}".ljust(cls.WIDTH) + "|")

        sub_total = dish_total + payment.seat_charge
        gst = round(sub_total * 0.05, 2)
        total = sub_total + gst

        print(f"| GST         : ₹{gst}".ljust(cls.WIDTH) + "|")
        print(f"| TOTAL       : ₹{round(total, 2)}".ljust(cls.WIDTH) + "|")

        cls.print_line()