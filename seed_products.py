from app.database import SessionLocal
from app.models import Product

db = SessionLocal()

db.add_all([
    Product(title="Laptop", price=999.99, count=10),
    Product(title="Mouse", price=29.99, count=50)
])

db.commit()
db.close()
print("Добавлено 2 продукта")