import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field


DATABASE_URL = "sqlite:///my_database.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("pasword", sqlalchemy.String(100))
)

products = sqlalchemy.Table(
    'products',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("prise", sqlalchemy.Integer),
)

orders = sqlalchemy.Table(
    'orders',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String, nullable=False)
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


app = FastAPI()



class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=50)
    email: str = Field(max_length=128)
    pasword: str = Field(max_length=100)
    
class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    surname: str = Field(max_length=50)
    email: str = Field(max_length=128)
    pasword: str = Field(max_length=100)
    
    
class ProductIn(BaseModel):
    name: str = Field(max_length=50)
    description: str
    prise: int
    
class Product(BaseModel):
    id: int
    name: str = Field(max_length=50)
    description: str
    prise: int
    
    
class OrderIn(BaseModel):
    name_id: int
    product_id: int
    status: str
    
class Order(BaseModel):
    id: int
    name_id: int
    product_id: int
    status: str
    



@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=list[User])
async def read_user():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.fetch_one(query)
    return {"massage": "User delete"}




@app.post("/products/", response_model=Product)
async def create_products(product: ProductIn):
    query = products.insert().values(**product.dict())
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


@app.get("/products/", response_model=list[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product)
async def read_products(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.put("/products/{product_id}", response_model=Product)
async def update_products(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}


@app.delete("/products/{product_id}")
async def delete_products(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.fetch_one(query)
    return {"massage": "Product delete"}




@app.post("/orders/", response_model=Order)
async def create_orders(order: OrderIn):
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.get("/orders/", response_model=list[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_orders(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_orders(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_orders(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.fetch_one(query)
    return {"massage": "Order delete"}