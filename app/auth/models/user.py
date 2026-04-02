class User:
    def __init__(self, user_id, name, email, password, phone, role="staff"):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.role = role

    def convert_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "role": self.role
        }

    @staticmethod
    def from_dict(data):
        return User(
            data["id"],
            data["name"],
            data["email"],
            data["password"],
            data["phone"],
            data["role"]
        )