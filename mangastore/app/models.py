# Optional - mostly use Pydantic schemas in schemas.py

class User:
    def __init__(self, email, full_name, role, password_hash):
        self.email = email
        self.full_name = full_name
        self.role = role
        self.password_hash = password_hash

class Manga:
    def __init__(self, title, author, genre, price, stock, rating=0):
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.stock = stock
        self.rating = rating

class Order:
    def __init__(self, user_id, manga_ids, total_price, status="pending"):
        self.user_id = user_id
        self.manga_ids = manga_ids
        self.total_price = total_price
        self.status = status
