from app.utils.database_handler import get_food_menu
from app.utils.ui_helper import UIHelper


class MenuViewer:

    # ================= BOX =================
    @staticmethod
    def print_box(title, items):
        if not items:
            return

        width = UIHelper.WIDTH

        # detect pricing type
        has_half_full = any(
            "half" in item.get("price", {}) or "full" in item.get("price", {})
            for item in items
        )

        # column widths
        name_w = 26
        type_w = 18
        tag_w = 37

        if has_half_full:
            half_w = 8
            full_w = 8
        else:
            price_w = 10

        def format_col(text, w):
            return str(text)[:w].ljust(w)

        # ===== TITLE =====
        UIHelper.print_center(title.upper())
        UIHelper.print_line()

        # ===== HEADER =====
        if has_half_full:
            header = (
                format_col("DISH", name_w) +
                format_col("TYPE", type_w) +
                format_col("HALF", half_w) +
                format_col("FULL", full_w) +
                format_col("TAGS", tag_w)
            )
        else:
            header = (
                format_col("DISH", name_w) +
                format_col("TYPE", type_w) +
                format_col("PRICE", price_w) +
                format_col("TAGS", tag_w)
            )

        header = header[:width]
        print("|" + header.ljust(width) + "|")
        UIHelper.print_line()

        # ===== DATA =====
        for item in items:
            name = item.get("name", "")
            food_type = item.get("type", "")
            tags = " ".join(item.get("tags", []))

            price = item.get("price", {})
            half = price.get("half", "")
            full = price.get("full", "")
            single = price.get("single", "")

            if has_half_full:
                row = (
                    format_col(name, name_w) +
                    format_col(food_type, type_w) +
                    format_col(half, half_w) +
                    format_col(full, full_w) +
                    format_col(tags, tag_w)
                )
            else:
                row = (
                    format_col(name, name_w) +
                    format_col(food_type, type_w) +
                    format_col(single, price_w) +
                    format_col(tags, tag_w)
                )

            row = row[:width]
            print("|" + row.ljust(width) + "|")

        UIHelper.print_line()


    @staticmethod
    def view_menu():
        try:
            data = get_food_menu()

            if not data:
                print(" Menu not loaded")
                return

            UIHelper.display_header(data)

            menu = data.get("menu", [])

      
            appetizers = []
            breakfast = []
            lunch_dinner = {}

            international = []
            street = []
            soups = []
            drinks = []
            desserts = []


            for item in menu:
                category = item.get("category", "").lower()
                meals = item.get("meal", [])

                if category == "appetizers":
                    appetizers.append(item)

                elif "breakfast" in meals:
                    breakfast.append(item)

                elif "lunch" in meals or "dinner" in meals:
                    if category not in lunch_dinner:
                        lunch_dinner[category] = []
                    lunch_dinner[category].append(item)

                elif category == "international":
                    international.append(item)

                elif "street" in category:
                    street.append(item)

                elif "soup" in category:
                    soups.append(item)

                elif "drink" in category:
                    drinks.append(item)

                elif "dessert" in category:
                    desserts.append(item)

        
            MenuViewer.print_box("Appetizers", appetizers)
            MenuViewer.print_box("Breakfast", breakfast)

            UIHelper.print_line()
            UIHelper.print_center("LUNCH / DINNER")
            UIHelper.print_line()

            for subcat, items in lunch_dinner.items():
                MenuViewer.print_box(subcat, items)

            MenuViewer.print_box("International", international)
            MenuViewer.print_box("Street Food", street)
            MenuViewer.print_box("Soups", soups)
            MenuViewer.print_box("Drinks", drinks)
            MenuViewer.print_box("Desserts", desserts)

        except Exception as e:
            print("Error while displaying menu:", e)