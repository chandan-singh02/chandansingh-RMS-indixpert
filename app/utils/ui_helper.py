

def print_line():
    print("+" + "-" * UIHelper.WIDTH + "+")
class UIHelper:

    WIDTH = 87

    @staticmethod
    def print_line():
         print("+" + "-" * UIHelper.WIDTH + "+")

    @staticmethod
    def print_center(text):
        print("|" + text.center(UIHelper.WIDTH) + "|")

    @staticmethod
    def display_header(data):
        res = data.get("restaurant", {})

        print("\n+" + "-" * UIHelper.WIDTH + "+")
        print("|" + res.get("name", "").upper().center(UIHelper.WIDTH) + "|")
        print("|" + res.get("location", "").center(UIHelper.WIDTH) + "|")
        print("|" + res.get("contact", "").center(UIHelper.WIDTH) + "|")
        print("+" + "-" * UIHelper.WIDTH + "+")