# SQLAlchemy 20.
### 1. **Installation**
Make sure to install the necessary packages first:

```bash
pip install sqlalchemy==2.0 fastapi uvicorn psycopg2
```

- `SQLAlchemy 2.0` is the ORM for working with databases.
- `FastAPI` is the web framework.
- `psycopg2` is the PostgreSQL adapter.

### 2. **Setting up SQLAlchemy**

We'll start by setting up SQLAlchemy and defining our models. SQLAlchemy 2.0 introduces `async` support, so we can integrate it easily with FastAPI.

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.future import select

# Database URL (use your PostgreSQL credentials)
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/mydatabase"

# Creating the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker using AsyncSession
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

```

### 3. **Defining Models**

We'll define two simple models, `User` and `Item`, where a user can have multiple items (a one-to-many relationship).

```python
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    
    # One-to-many relationship with Item
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Many-to-one relationship with User
    owner = relationship("User", back_populates="items")
```

### 4. **Creating the Database Tables**

Before running FastAPI, we need to create the tables in our PostgreSQL database.

```python
import asyncio

async def init_db():
    async with engine.begin() as conn:
        # Drop all tables and recreate them (useful during development)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# To create tables, run the init_db function
asyncio.run(init_db())
```

### 5. **Integrating SQLAlchemy with FastAPI**

Now, we'll integrate SQLAlchemy into FastAPI by using a dependency to get the database session.

#### `app.py`

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

app = FastAPI()

# Dependency to get DB session
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### 6. **Creating Endpoints**

#### Add a new User

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

@app.post("/users/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
```

#### Query Users

```python
@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users
```

#### Query a User by ID and include their items

```python
@app.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 7. **Creating Items for a User**

```python
class ItemCreate(BaseModel):
    title: str
    description: str

@app.post("/users/{user_id}/items/")
async def create_item_for_user(user_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_item = Item(title=item.title, description=item.description, owner_id=user_id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item
```

### 8. **Running FastAPI**

Start the FastAPI app using `uvicorn`.

```bash
uvicorn app:app --reload
```

Now, you can interact with your API at `http://127.0.0.1:8000/docs`.

### 9. **Different Queries in SQLAlchemy 2.0**

#### Query Users with Items

```python
@app.get("/users/{user_id}/items/")
async def read_user_items(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.owner_id == user_id))
    items = result.scalars().all()
    return items
```

#### Filtering Users

```python
@app.get("/users/")
async def read_filtered_users(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    users = result.scalars().all()
    return users
```
