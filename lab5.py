import datetime
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import PlainTextResponse
from typing import List, Dict, Any

app = FastAPI()



#1
class User:
    def __init__(self, user_id, name, email):
        self._id = int(user_id)
        self._name = name.strip().title()

        email_clean = email.strip().lower()
        if "@" not in email_clean:
            raise ValueError
        self._email = email_clean

    def __str__(self):
        return f"User(id={self._id}, name='{self._name}', email='{self._email}')"

    def __del__(self):
        print(f"User {self._name} deleted")


@app.get('/a')
def index_a():
    u = User(1, " john doe ", "John@Example.COM")
    print(u)



#2
class UserExtended(User):
    @classmethod
    def from_string(cls, data: str):
        parts = [p.strip() for p in data.split(',')]
        return cls(parts[0], parts[1], parts[2])


@app.get('/b')
def index_b():
    u = UserExtended.from_string("2, Alice Wonderland , alice@wonder.com")
    print(u)



#3
class Product:
    def __init__(self, product_id: int, name: str, price: float, category: str):
        self.id = product_id
        self.name = name
        self.price = float(price)
        self.category = category

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'category': self.category}

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, category='{self.category}')"


@app.get('/product')
def show_product():
    p1 = Product(1, 'Laptop', 1200.0, 'Electronics')
    p2 = Product(1, 'Laptop', 1200.0, 'Electronics')

    products_set = {p1, p2}

    return {
        "string_format": str(p1),
        "dict_format": p1.to_dict(),
        "set_count": len(products_set)
    }



#4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Set

class Product(BaseModel):
    id: int
    name: str
    price: float

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.id == other.id

class Inventory:
    def __init__(self):
        self._products: Dict[int, Product] = {}

    def add_product(self, product: Product):
        if product.id not in self._products:
            self._products[product.id] = product

    def remove_product(self, product_id: int):
        self._products.pop(product_id, None)

    def get_product(self, product_id: int) -> Product:
        return self._products.get(product_id)

    def get_all_products(self) -> List[Product]:
        return list(self._products.values())

    def unique_products(self) -> Set[Product]:
        return set(self._products.values())

    def to_dict(self) -> Dict[int, Product]:
        return self._products.copy()

app = FastAPI()
inventory = Inventory()

@app.post("/products/", status_code=201)
async def add_product(product: Product):
    if inventory.get_product(product.id):
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    inventory.add_product(product)
    return {"status": "success", "added": product}

@app.get("/products/", response_model=List[Product])
async def list_products():
    return inventory.get_all_products()

@app.get("/products/unique")
async def list_unique_products():
    return inventory.unique_products()

@app.get("/products/{product_id}", response_model=Product)
async def get_one_product(product_id: int):
    product = inventory.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    if not inventory.get_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    inventory.remove_product(product_id)
    return {"status": "deleted", "id": product_id}

@app.get("/inventory/raw")
async def get_raw_dict():
    return inventory.to_dict()







#5
from pydantic import BaseModel
from typing import List, Dict


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


class Inventory:
    def __init__(self):
        self._products: Dict[int, Product] = {}

    def add_product(self, product: Product):
        if product.id not in self._products:
            self._products[product.id] = product

    def filter_by_price(self, min_price: float) -> List[Product]:
        check = lambda p: p.price >= min_price

        return [p for p in self._products.values() if check(p)]


if __name__ == "__main__":
    inv = Inventory()
    inv.add_product(Product(id=1, name="Laptop", price=1200.0, category="Electronics"))
    inv.add_product(Product(id=2, name="Mouse", price=25.0, category="Electronics"))

    expensive = inv.filter_by_price(100.0)
    print([p.name for p in expensive])


@app.get("/products/filter")
async def filter_products(min_price: float = 0.0):
    return inventory.filter_by_price(min_price)





#6
class Logger:
    @staticmethod
    def log_action(user_id, action, product_id, filename="actions.log"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp};{user_id};{action};{product_id}\n"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_entry)

    @staticmethod
    def read_logs(filename="actions.log"):
        logs = []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(';')
                        logs.append({'time': parts[0], 'user': parts[1], 'act': parts[2]})
        except FileNotFoundError:
            return []
        return logs


@app.get('/logs')
def test_logs():
    Logger.log_action(1, "view", 101)
    return Logger.read_logs()



#7
class Order:
    def __init__(self, order_id: int, user_name: str):
        self.id = order_id
        self.user_name = user_name
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def total_price(self):
        return sum(p.price for p in self.products)

    def __str__(self):
        names = [p.name for p in self.products]
        return f"Order {self.id}, User: {self.user_name}, Products: {names}, Total: {self.total_price()}"


@app.get('/order')
def test_order():
    my_order = Order(500, "John Doe")
    my_order.add_product(Product(101, "Laptop", 1200.0, "IT"))
    return {
        "order_id": my_order.id,
        "total": my_order.total_price(),
        "user": my_order.user_name,
        "info": str(my_order)
    }



#8
class AnalyticsOrder(Order):
    def most_expensive_products(self, n: int) -> list[Product]:
        sorted_p = sorted(self.products, key=lambda p: p.price, reverse=True)
        return sorted_p[:n]


@app.get('/analytics')
def analytics():
    order = AnalyticsOrder(1, "Admin")
    order.add_product(Product(1, "Mouse", 25.0, "Acc"))
    order.add_product(Product(2, "Laptop", 1200.0, "IT"))
    order.add_product(Product(3, "Monitor", 300.0, "IT"))

    top = order.most_expensive_products(2)
    return {"top_products": [p.to_dict() for p in top]}



#9
class OrderWithGenerator(Order):
    def price_stream(self):
        for product in self.products:
            yield product.price


@app.get('/stream_prices')
def stream_prices():
    p_list = [
        Product(1, "Laptop", 1200.0, "IT"),
        Product(2, "Mouse", 25.0, "Acc"),
        Product(3, "Monitor", 300.0, "IT")
    ]

    order = OrderWithGenerator(p_list)

    collected_prices = []
    for price in order.price_stream():
        collected_prices.append(price)

    return {"prices": collected_prices}

#10
class SimpleOrder:
    def __init__(self, id, count):
        self.id = id
        self.count = count

    def __str__(self):
        return f"Заказ #{self.id}: {self.count} товаров"


class OrderIterator:
    def __init__(self, orders):
        self.orders = orders
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.orders):
            res = str(self.orders[self.index])
            self.index += 1
            return res + "\n"
        raise StopIteration


@app.get('/orders', response_class=PlainTextResponse)
async def get_all_orders():
    data = [SimpleOrder(101, 2), SimpleOrder(102, 5)]
    iterator = OrderIterator(data)
    return "".join(list(iterator))


#11
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


@app.post("/prices")
async def get_prices_array(products: List[Product]):
    prices = [p.price for p in products]
    np_prices = np.array(prices, dtype=float)

    return {"prices": np_prices.tolist()}


#12
import numpy as np
from fastapi import FastAPI
from typing import List, Tuple

app = FastAPI()


@app.post("/analytics")
async def get_price_stats(prices: List[float]):
    np_prices = np.array(prices)

    mean_price = np.mean(np_prices)
    median_price = np.median(np_prices)

    return mean_price, median_price


#13
import numpy as np
from fastapi import FastAPI
from typing import List

app = FastAPI()


@app.post("/normalize")
async def normalize_prices(prices: List[float]):
    np_prices = np.array(prices)

    min_val = np.min(np_prices)
    max_val = np.max(np_prices)

    if max_val == min_val:
        return np.zeros_like(np_prices).tolist()

    normalized = (np_prices - min_val) / (max_val - min_val)

    return normalized.tolist()


#14
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


@app.post("/categories")
async def get_categories_array(products: List[Product]):
    categories = [p.category for p in products]
    np_categories = np.array(categories)

    return np_categories.tolist()



#15
import numpy as np
from fastapi import FastAPI
from typing import List

app = FastAPI()


@app.post("/unique-categories-count")
async def count_unique_categories(categories: List[str]):
    np_categories = np.array(categories)

    unique_categories = np.unique(np_categories)
    count = len(unique_categories)

    return count


#16
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


@app.post("/expensive-products")
async def get_expensive_products(products: List[Product]):
    prices = np.array([p.price for p in products])

    mean_price = np.mean(prices)

    result = [p for p in products if p.price > mean_price]

    return result


#17
import numpy as np
from fastapi import FastAPI
from typing import List

app = FastAPI()


@app.post("/apply-discount")
async def apply_discount(prices: List[float]):
    np_prices = np.array(prices)

    discounted_prices = np_prices * 0.9

    return discounted_prices.tolist()



#18
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


class User(BaseModel):
    id: int
    name: str


class Order(BaseModel):
    id: int
    user: User
    products: List[Product]


@app.post("/user-orders-matrix")
async def get_orders_matrix(orders: List[Order]):
    totals = [[sum(p.price for p in order.products)] for order in orders]

    matrix = np.array(totals, dtype=float)

    return matrix.tolist()


#19
import numpy as np
from fastapi import FastAPI
from typing import List

app = FastAPI()


@app.post("/average-order")
async def calculate_average_order(order_sums: List[float]):
    order_array = np.array(order_sums)

    average_sum = np.mean(order_array)

    return float(average_sum)



#20
import numpy as np
from fastapi import FastAPI
from typing import List

app = FastAPI()


@app.post("/high-value-indices")
async def get_high_value_indices(order_sums: List[float]):
    np_orders = np.array(order_sums)

    indices = np.where(np_orders > 1000)[0]

    return indices.tolist()




#21
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from typing import List

app = FastAPI()

class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email
        self.registration_date = date.today().isoformat()

users_list = [
    User(1, "John Doe", "john@example.com"),
    User(2, "Alice", "alice@example.com"),
]


@app.get("/users/dataframe")
def get_users_table():
    data = [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "registration_date": u.registration_date
        }
        for u in users_list
    ]


    df = pd.DataFrame(data)

    return df.to_dict(orient="records")


#22
class Product:
    def __init__(self, id: int, name: str, category: str, price: float):
        self.id = id
        self.name = name
        self.category = category
        self.price = price


    def products_to_dataframe(products):
        return pd.DataFrame([
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price
            }
            for p in products
        ])

products = [
        Product(1, "Laptop", "Electronics", 1200.0),
        Product(2, "T-Shirt", "Clothing", 20.0)
    ]




@app.get("/products")
def get_products_df():
    df = products_to_dataframe(products)
    return df.to_dict(orient="records")




#23
class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
class Order:
    def __init__(self, order_id: int, user_id: int, total: float):
        self.order_id = order_id
        self.user_id = user_id
        self.total = total


def merge_orders(users, orders):
    users_df = pd.DataFrame([
        {"id": u.id, "name": u.name} for u in users
    ])

    orders_df = pd.DataFrame([
        {"order_id": o.order_id, "user_id": o.user_id, "total": o.total}
        for o in orders
    ])

    merged = pd.merge(
        orders_df,
        users_df,
        left_on="user_id",
        right_on="id",
        how="left"
    )

    return merged[["order_id", "name", "total"]].rename(columns={"name": "user_name"})


users = [
    User(1, "John"),
    User(2, "Alice")
]

orders = [
    Order(101, 1, 1200),
    Order(102, 2, 25)
]


@app.get("/orders")
def get_merged_orders():
    df = merge_orders(users, orders)
    return df.to_dict(orient="records")


#24
df = pd.DataFrame([
    {"order_id": 101, "user_name": "John", "total": 1200},
    {"order_id": 102, "user_name": "Alice", "total": 25},
])

def filter_orders(value: float):
    return df[df["total"] > value]

@app.get("/orders/filter")
def get_orders(value: float):
    result = filter_orders(value)
    return result.to_dict(orient="records")


#25
df = pd.DataFrame([
    {"order_id": 101, "user_name": "John", "total": 1200},
    {"order_id": 103, "user_name": "John", "total": 500},
    {"order_id": 102, "user_name": "Alice", "total": 25},
])

def group_orders():
    result = df.groupby("user_name", as_index=False)["total"].sum()
    result = result.rename(columns={"total": "total_sum"})
    return result

@app.get("/orders/grouped")
def get_grouped_orders():
    result = group_orders()
    return result.to_dict(orient="records")


#26
df = pd.DataFrame([
    {"order_id": 101, "user_name": "John", "total": 1200},
    {"order_id": 103, "user_name": "John", "total": 500},
    {"order_id": 102, "user_name": "Alice", "total": 25},
])

def group_orders_mean():
    result = df.groupby("user_name", as_index=False)["total"].mean()
    result = result.rename(columns={"total": "mean_total"})
    return result

@app.get("/orders/mean")
def get_mean_orders():
    result = group_orders_mean()
    return result.to_dict(orient="records")


#27
df = pd.DataFrame([
    {"order_id": 101, "user_name": "John", "total": 1200},
    {"order_id": 103, "user_name": "John", "total": 500},
    {"order_id": 102, "user_name": "Alice", "total": 25},
])

def group_orders_count():
    result = df.groupby("user_name", as_index=False)["order_id"].count()
    result = result.rename(columns={"order_id": "orders_count"})
    return result

@app.get("/orders/count")
def get_orders_count():
    result = group_orders_count()
    return result.to_dict(orient="records")


#28
df = pd.DataFrame([
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 1200},
    {"id": 2, "name": "Mouse", "category": "Electronics", "price": 25},
    {"id": 3, "name": "Shirt", "category": "Clothing", "price": 20},
])

def mean_price_by_category():
    result = df.groupby("category", as_index=False)["price"].mean()
    result = result.rename(columns={"price": "mean_price"})
    return result

@app.get("/products/mean-price")
def get_mean_price():
    result = mean_price_by_category()
    return result.to_dict(orient="records")


#29
df = pd.DataFrame([
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Mouse", "price": 25},
])

def add_discount_column():
    df["discounted_price"] = df["price"] * 0.9
    return df

@app.get("/products/discount")
def get_discounted_products():
    result = add_discount_column()
    return result.to_dict(orient="records")


#30
df = pd.DataFrame([
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Mouse", "price": 25},
    {"id": 3, "name": "Monitor", "price": 450},
])

def sort_by_price_desc():
    result = df.sort_values(by="price", ascending=False)
    return result

@app.get("/products/sorted")
def get_sorted_products():
    result = sort_by_price_desc()
    return result.to_dict(orient="records")


#31
df = pd.DataFrame([
    {"order_id": 101, "product_name": "Laptop", "price": 1200},
    {"order_id": 102, "product_name": "Mouse", "price": 25},
])

def add_quantity():
    df["quantity"] = 1
    return df

@app.get("/orders/quantity")
def get_orders_with_quantity():
    result = add_quantity()
    return result.to_dict(orient="records")


#32
df = pd.DataFrame([
    {"order_id": 101, "product_name": "Laptop", "price": 1200, "quantity": 1},
    {"order_id": 102, "product_name": "Mouse", "price": 25, "quantity": 2},
])

def add_total_price():
    df["total_price"] = df["price"] * df["quantity"]
    return df

@app.get("/orders/total")
def get_orders_total():
    result = add_total_price()
    return result.to_dict(orient="records")


#33
df = pd.DataFrame([
    {"product_name": "Laptop", "category": "Electronics", "price": 1200},
    {"product_name": "T-Shirt", "category": "Clothing", "price": 20},
])

def get_electronics():
    return df[df["category"] == "Electronics"]

@app.get("/products/electronics")
def electronics_products():
    result = get_electronics()
    return result.to_dict(orient="records")


#34
df = pd.DataFrame([
    {"product_name": "Laptop", "category": "Electronics"},
    {"product_name": "Mouse", "category": "Electronics"},
    {"product_name": "Shirt", "category": "Clothing"},
])

def count_products_by_category():
    result = df.groupby("category", as_index=False)["product_name"].count()
    result = result.rename(columns={"product_name": "count"})
    return result

@app.get("/products/count-by-category")
def get_count_by_category():
    result = count_products_by_category()
    return result.to_dict(orient="records")


#35
df = pd.DataFrame([
    {"product_name": "Laptop", "category": "Electronics", "price": 1200},
    {"product_name": "Mouse", "category": "Electronics", "price": 25},
    {"product_name": "Shirt", "category": "Clothing", "price": 20},
])

def mean_price_by_category():
    result = df.groupby("category", as_index=False)["price"].mean()
    result = result.rename(columns={"price": "mean_price"})
    return result

@app.get("/products/mean-price")
def get_mean_price():
    result = mean_price_by_category()
    return result.to_dict(orient="records")


#36
df = pd.DataFrame([
    {"order_id": 101, "total_price": 1200},
    {"order_id": 102, "total_price": 50},
])

def sort_orders():
    result = df.sort_values(by="total_price", ascending=False)
    return result

@app.get("/orders/sorted")
def get_sorted_orders():
    result = sort_orders()
    return result.to_dict(orient="records")


#37
df = pd.DataFrame([
    {"order_id": 101, "total_price": 1200},
    {"order_id": 102, "total_price": 50},
    {"order_id": 103, "total_price": 500},
    {"order_id": 104, "total_price": 1500},
])

def top_3_orders():
    result = df.sort_values(by="total_price", ascending=False).head(3)
    return result

@app.get("/orders/top3")
def get_top_3():
    result = top_3_orders()
    return result.to_dict(orient="records")


#38
users_df = pd.DataFrame([
    {"user_id": 1, "user_name": "John"},
    {"user_id": 2, "user_name": "Alice"},
])

orders_df = pd.DataFrame([
    {"order_id": 101, "user_id": 1, "total_price": 1200},
    {"order_id": 102, "user_id": 2, "total_price": 50},
])

def merge_users_orders():
    result = pd.merge(
        orders_df,
        users_df,
        on="user_id",
        how="left"
    )

    return result[["order_id", "user_name", "total_price"]]

@app.get("/orders/with-users")
def get_orders_with_users():
    result = merge_users_orders()
    return result.to_dict(orient="records")


#39
df = pd.DataFrame([
    {"user_name": "John", "total_price": 1200},
    {"user_name": "John", "total_price": 500},
    {"user_name": "Alice", "total_price": 50},
])

def mean_order_by_user():
    result = df.groupby("user_name", as_index=False)["total_price"].mean()
    result = result.rename(columns={"total_price": "mean_total"})
    return result

@app.get("/orders/mean-by-user")
def get_mean_by_user():
    result = mean_order_by_user()
    return result.to_dict(orient="records")


#40
df = pd.DataFrame([
    {"user_name": "John", "order_id": 101},
    {"user_name": "John", "order_id": 103},
    {"user_name": "Alice", "order_id": 102},
])

def count_orders_by_user():
    result = df.groupby("user_name", as_index=False)["order_id"].count()
    result = result.rename(columns={"order_id": "orders_count"})
    return result

@app.get("/orders/count-by-user")
def get_count_by_user():
    result = count_orders_by_user()
    return result.to_dict(orient="records")


#41
df = pd.DataFrame([
    {"user_name": "John", "total_price": 1200},
    {"user_name": "John", "total_price": 500},
    {"user_name": "Alice", "total_price": 50},
])

def max_order_by_user():
    result = df.groupby("user_name", as_index=False)["total_price"].max()
    result = result.rename(columns={"total_price": "max_order"})
    return result

@app.get("/orders/max-by-user")
def get_max_by_user():
    result = max_order_by_user()
    return result.to_dict(orient="records")


#42
df = pd.DataFrame([
    {"user_name": "John", "category": "Electronics"},
    {"user_name": "John", "category": "Electronics"},
    {"user_name": "John", "category": "Clothing"},
    {"user_name": "Alice", "category": "Clothing"},
])

def unique_categories_by_user():
    result = df.groupby("user_name", as_index=False)["category"].nunique()
    result = result.rename(columns={"category": "unique_categories"})
    return result

@app.get("/users/unique-categories")
def get_unique_categories():
    result = unique_categories_by_user()
    return result.to_dict(orient="records")


#43
df = pd.DataFrame([
    {"user_name": "John", "total_sum": 1700},
    {"user_name": "Alice", "total_sum": 25},
])

def add_vip_column():
    df["VIP"] = df["total_sum"] > 1000
    return df

@app.get("/users/vip")
def get_vip_users():
    result = add_vip_column()
    return result.to_dict(orient="records")


#44
df = pd.DataFrame([
    {"user_name": "John", "total_sum": 1700, "mean_total": 850},
    {"user_name": "Alice", "total_sum": 25, "mean_total": 25},
    {"user_name": "Bob", "total_sum": 1700, "mean_total": 600},
])

def sort_users():
    result = df.sort_values(
        by=["total_sum", "mean_total"],
        ascending=[False, True]
    )
    return result

@app.get("/users/sorted")
def get_sorted_users():
    result = sort_users()
    return result.to_dict(orient="records")


#45
df = pd.DataFrame([
    {"user_name": "John", "order_id": 101, "total_price": 1200, "category": "Electronics"},
    {"user_name": "John", "order_id": 103, "total_price": 500, "category": "Clothing"},
    {"user_name": "Alice", "order_id": 102, "total_price": 25, "category": "Clothing"},
])

def build_user_stats():
    grouped = df.groupby("user_name")

    result = pd.DataFrame({
        "user_name": grouped["order_id"].count().index,
        "total_orders": grouped["order_id"].count().values,
        "total_sum": grouped["total_price"].sum().values,
        "mean_total": grouped["total_price"].mean().values,
        "max_order": grouped["total_price"].max().values,
        "unique_categories": grouped["category"].nunique().values,
    })

    result["VIP"] = result["total_sum"] > 1000

    return result

@app.get("/users/stats")
def get_user_stats():
    result = build_user_stats()
    return result.to_dict(orient="records")







