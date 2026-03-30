import asyncio
from sqlalchemy import text
from app.core.database import engine, Base, AsyncSessionLocal
from app.models.product import Product
from app.models.message import Message

async def seed_database():
    print("Connecting to the database...")
    
    async with engine.begin() as conn:
        # 1. Force drop the products table and anything attached to it
        await conn.execute(text("DROP TABLE IF EXISTS products CASCADE"))
        
        # 2. Create the fresh table
        await conn.run_sync(Base.metadata.create_all) 
        print("Created 'products' table!")

    # 3. Add some test products
    async with AsyncSessionLocal() as session:
        products = [
            Product(name="Nike Air Max", description="Comfortable running shoes", price=120.00),
            Product(name="Leather Wallet", description="Genuine brown leather wallet", price=45.00),
            Product(name="Wireless Earbuds", description="Noise-canceling bluetooth earbuds", price=89.99),
            Product(name="Cotton T-Shirt", description="Soft blue cotton t-shirt", price=19.50)
        ]
        
        session.add_all(products)
        await session.commit()
        print(f"Successfully added {len(products)} products to the database!")

if __name__ == "__main__":
    asyncio.run(seed_database())