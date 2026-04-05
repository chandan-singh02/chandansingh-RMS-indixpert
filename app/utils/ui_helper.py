from app.utils.colors import error, success, info, menu, user_input,menus,restaurant_color,sub_headings
class MenuViewer:

    WIDTH = 84

    @staticmethod
    def print_line():
       print(menus("+" + "-" * MenuViewer.WIDTH + "+"))

    @staticmethod
    def print_center(text):
        print(menus("|" + text.center(MenuViewer.WIDTH) + "|"))

    @staticmethod
    def display_header(data):
        res = data.get("restaurant", {})

        print("\n+" + "-" * MenuViewer.WIDTH + "+")
        print("|" + restaurant_color(res.get("name", "").upper().center(MenuViewer.WIDTH)) + "|")
        print("|" + sub_headings(res.get("location", "").center(MenuViewer.WIDTH)) + "|")
        print("|" + sub_headings(res.get("contact", "").center(MenuViewer.WIDTH)) + "|")
        print("+" + "-" * MenuViewer.WIDTH + "+")


    @staticmethod
    def print_box(title, items):
        if not items:
            return

        width = MenuViewer.WIDTH

        MenuViewer.print_center(title.upper())
        MenuViewer.print_line()

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
        MenuViewer.print_line()

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

        MenuViewer.print_line()
    
    @staticmethod
    def print_order_box(order):
        width = MenuViewer.WIDTH

        print("\n")
        MenuViewer.print_line()
        MenuViewer.print_center("ORDER DETAILS")
        MenuViewer.print_line()

        # Basic Info
       print(menus(f"| Order ID : {order.id}".ljust(width)) + "|")
       print(menus(f"| Customer : {order.customer_name}".ljust(width)) + "|")
       print(menus(f"| Date     : {order.date}".ljust(width)) + "|")

       MenuViewer.print_line()

       # Items Header
       print(menus("| Items:".ljust(width)) + "|")

        # Items List
        for i, item in enumerate(order.items, start=1):
            for name, size in item.items():
                line = f"{i}. {name} ({size.capitalize()})"
                print(menus(f"| {line}".ljust(width)) + "|")

        MenuViewer.print_line()