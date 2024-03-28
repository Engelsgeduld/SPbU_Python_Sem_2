from dataclasses import dataclass
from typing import Iterator


@dataclass
class Product:
    name: str
    price: float
    rating: float
    count: int

    def buy_product(self, count: int = 1) -> None:
        if self.count < count:
            raise ValueError(f"You can bou only {self.count}")
        self.count -= count

    def __str__(self) -> str:
        return f"Name: {self.name} Rating: {self.rating} Price: {self.price} Count: {self.count}"


class Bucket:
    def __init__(self) -> None:
        self.products: dict[str, int] = {}
        self.size: int = 0
        self.cost: float = 0

    def add_product(self, product: Product, count: int = 1) -> None:
        print(product)
        self.products[product.name] = count
        self.size += count
        self.cost += product.price * count

    def remove_product(self, product: Product, count: int = 1) -> None:
        if count > self.products[product.name]:
            raise ValueError(f"Your bucket contain only {self.products[product.name]}")
        self.products[product.name] -= count
        self.size -= count
        self.cost -= product.price * count
        if self.products[product.name] == 0:
            self.products.pop(product.name)

    def __iter__(self) -> Iterator[tuple[str, int]]:
        return iter(self.products.items())

    def __delete__(self) -> None:
        del self.products
        self.size = 0
        self.cost = 0

    def get_cost(self) -> float:
        return self.cost


class Shop:
    def __init__(self) -> None:
        self.products: dict[str, Product] = {}

    def _sort_by(self, val: str) -> list[Product]:
        return sorted(self.products.values(), key=lambda product: getattr(product, val))

    def get_cheapest(self) -> Product:
        return self._sort_by("price")[0]

    def get_costed(self) -> Product:
        return self._sort_by("price")[-1]

    def get_popular(self) -> Product:
        return self._sort_by("rating")[-1]

    def get_unpopular(self) -> Product:
        return self._sort_by("rating")[0]

    def buy_bucket(self, bucket: Bucket) -> None:
        sold_out_products = [self.products[product] for product, cost in bucket if self.products[product].count < cost]
        if sold_out_products:
            raise ValueError(f"This products already sold out {list(sold_out_products)}")
        for product, count in bucket:
            self.products[product].buy_product(count)
        del bucket
