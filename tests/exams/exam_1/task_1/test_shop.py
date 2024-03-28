import pytest

from src.exams.exam_1.task_1.shop import *

products = [
    Product("Shirt Tom Taylor", 59.9, 10, 2),
    Product("Jeans", 13.9, 2, 5),
    Product("NNN", 15.9, 9.5, 10),
]
SHOP = Shop()
SHOP.products = dict((product.name, product) for product in products)


@pytest.mark.parametrize(
    "val, expected",
    [
        (
            "price",
            [Product("Jeans", 13.9, 2, 5), Product("NNN", 15.9, 9.5, 10), Product("Shirt Tom Taylor", 59.9, 10, 2)],
        ),
        (
            "rating",
            [Product("Jeans", 13.9, 2, 5), Product("NNN", 15.9, 9.5, 10), Product("Shirt Tom Taylor", 59.9, 10, 2)],
        ),
    ],
)
def test_shop_sort_by(val, expected) -> None:
    assert SHOP._sort_by(val) == expected


def test_shop_get_cheapest() -> None:
    assert SHOP.get_cheapest() == Product("Jeans", 13.9, 2, 5)


def test_shop_get_costed() -> None:
    assert SHOP.get_costed() == Product("Shirt Tom Taylor", 59.9, 10, 2)


def test_shop_get_popular() -> None:
    assert SHOP.get_popular() == Product("Shirt Tom Taylor", 59.9, 10, 2)


def test_shop_get_unpopular() -> None:
    assert SHOP.get_unpopular() == Product("Jeans", 13.9, 2, 5)


@pytest.mark.parametrize("count, expected", [(4, 6), (5, 5), (10, 0)])
def test_product_buy_method(count, expected) -> None:
    product = Product("Shirt", 10, 9, 10)
    product.buy_product(count)
    assert product.count == expected


def test_product_buy_method_exception():
    product = Product("Shirt", 10, 9, 10)
    with pytest.raises(ValueError):
        product.buy_product(11)


@pytest.mark.parametrize("product, count", [(products[0], 3), (products[1], 2), (products[2], 10)])
def test_bucket_add_product(product, count) -> None:
    bucket = Bucket()
    bucket.add_product(product, count)
    assert bucket.products[product.name] == count
