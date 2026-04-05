from app.utils.database_handler import get_food_menu
from app.utils.ui_helper import MenuViewer
from app.dashboard.models.menu_item import MenuItem
from app.utils.colors import error, success, info, menu, user_input,menus
from app.utils.app_error import AppError
from app.utils.error_handler import ErrorHandler
from app.utils.session import CURRENT_USER
class Menu:
    def __init__(self):
        data = get_food_menu()
        self.items = []
        
        self.restaurant = data.get("restaurant", {})
        menu_data = data.get("menu", [])

        for item in menu_data:
            menu_item = MenuItem.from_dict(item)
            self.items.append(menu_item)
            # print("\n item",items)


    def group_by_category(self):
        categories = {}
        # print("group by catgoru",categories)

        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []

            categories[item.category].append(item)

        return categories


    @staticmethod
    def view_menu():
        try:
            data = get_food_menu()

            if not data:
                print("Menu not loaded")
                return

            MenuViewer.display_header(data)

            menu = Menu()
            categories = menu.group_by_category()

            for category, items in categories.items():
                MenuViewer.print_box(category, items)

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="menu",action="view_menu")
           