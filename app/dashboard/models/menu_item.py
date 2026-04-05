class MenuItem:
    def __init__(self, id, name, category, food_type, price, tags="", available=True):
        self.id = id
        self.name = name
        self.category = category
        self.food_type = food_type
        self.price = price 
        self.tags = tags
        self.available = available


    def get_single(self):
        return self.price.get("single", "-")

    def get_half(self):
        return self.price.get("half", "-")

    def get_full(self):
        return self.price.get("full", "-")


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "type": self.food_type,
            "price": self.price,
            "tags": self.tags,
            "available": self.available
        }

    @staticmethod
    def from_dict(data):
        return MenuItem(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            food_type=data["type"],
            price=data.get("price", {}),
            tags=data.get("tags", ""),
            available=data.get("available", True)
        )
