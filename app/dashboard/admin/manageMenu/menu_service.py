from app.dashboard.models.menu_item import MenuItem
from app.utils.database_handler import get_food_menu, save_food_menu
from app.utils.validators import InputValidators
from app.utils.app_error import AppError
from app.utils.error_handler import ErrorHandler
from app.utils.colors import error, success, info, menu, user_input
from app.utils.session import CURRENT_USER
from app.utils.id_generator import generate_id

class MenuService:
    def __init__(self):
        self.data = get_food_menu()
        self.categories = self.data.get("categories", [])

        # convert dict → object
        self.menu = [] 
        menu_data = self.data.get("menu", [])

        for item in menu_data:
            menu_item = MenuItem.from_dict(item)
            self.menu.append(menu_item)
    def save(self):
        new_menu = []

        # convert object → dict
        for item in self.menu:
            new_menu.append(item.to_dict())

        self.data["menu"] = new_menu
        save_food_menu(self.data)


    def add_item(self):
        try:
            info("\n========== ADD FOOD ITEM ==========")
            category = input("Enter category name: ").title()
            name = input("Enter food name:  ")
            food_type = input("Enter food type veg/nonveg: ").lower()
            tags = input("Enter tags(optional): ").strip()

            InputValidators.validate_name(name,"Name")
            InputValidators.validate_name(category,"Category")
            InputValidators.validate_name(food_type,"Food type")

            if food_type not in ["veg","nonveg"]:
                raise AppError("Invalid food type","INVALID_TYPE")

           
            print("Please select the your price")
            menu("1. Single Price")
            menu("2. Half / Full Price")
            choice = InputValidators.validate_number(input("Please select the option: "),"PRICE OPTIONS", 1) 
         
            price = {}


            if choice == 1:
                single_price = input("Enter price: ")

                InputValidators.validate_price(single_price)
                price["single"] = single_price
                
            elif choice == 2:
                half_price = input("Enter half price: ")
                full_price = input("Enter full price: ")

                InputValidators.validate_price(half_price)
                InputValidators.validate_price(full_price)
                InputValidators.validate_price_relation(half_price,full_price)

                price["half"] = half_price
                price["full"] = full_price
            else:
                print("Invalid error")

            exists = False
            for item in self.categories:
                if item.lower() == category.lower():
                    exists = True
                    break

            if not exists:
                raise AppError("Category not found","INVALID_CATEGORY")

            

            new_item = MenuItem(
                id=generate_id("f"),
                name=name,
                category=category,
                food_type=food_type,
                price=price
            )

            self.menu.append(new_item)
            self.save()

            success(f"{name} item added successfully!")

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="add_item")

  
    def delete_item(self):
        try:
            name = input("Enter item name to delete: ")
            InputValidators.validate_name(name,"Name")

            found = False

            for item in self.menu:
                if item.name.lower() == name.lower():
                    self.menu.remove(item)
                    found = True
                    break

            if not found:
                raise AppError("Item not found","ITEM_NOT_FOUND")
                return

            self.save()
            success(f"{name} item deleted successfully!")
        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="delete_item")


  
    def update_item(self):
        try:
            item_name = input("Enter item name to update: ")
            InputValidators.validate_name(item_name,"Name")

            found = False

            for item in self.menu:
                if item.name.lower() == item_name.lower():
                    found = True

                    name = input(f"New name ({item.name}) : ").strip()

                    if name:
                        item.name = name

                    menu("Change price?")
                    menu("1. Single")
                    menu("2. Half/Full")
                    menu("3. Skip")

                    choice = input("Enter choice: ")

                    if choice == "1":
                        new_price = int(input("Enter new price: "))
                        item.price = {"single": new_price}

                    elif choice == "2":
                        half = int(input("Enter half price: "))
                        full = int(input("Enter full price: "))
                        item.price = {"half": half, "full": full}

                    self.save()
                    success(f"{name} item updated successfully!")
                    return

            if not found:
                raise AppError("Item  not found","INVALID_ITEM")

        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="delete_item")


  

 
    def add_category(self):

        try:
                        
            category = input("Enter new category: ").strip().title()

            exists = False
            for c in self.categories:
                if c.lower() == category.lower():
                    exists = True
                    break

            if exists:
                raise AppError("Category already exists", "DUPLICATE_CATEGORY")

            self.categories.append(category)
            self.data["categories"] = self.categories

            # save_food_menu(self.data)
            self.save()

            success(f"Category '{category}' added successfully")
        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="add_category")



 
    def delete_category(self):

        try:
            category = input("Enter category to delete: ").strip().lower()

            found = False

            for c in self.categories:
                if c.lower() == category.lower():
                    self.categories.remove(c)
                    found=True
                    break

            if not found:
                raise AppError("Category not found","CATEGORY_NOT_FOUND")
                return

            self.data["categories"] = self.categories
            self.save()
            success(f"Category {category} deleted successfully!")
        except Exception as e:
            ErrorHandler.handle(e,user_id=CURRENT_USER["id"],module="admindashboard",action="delete_category")


