from dataclasses import dataclass

@dataclass
class Product:
    weight: int = None
    price: int = None

apple = Product()
apple.price = 10
print(apple)
print(apple.price)