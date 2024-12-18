import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, TIMESTAMP, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session maker
Session = sessionmaker(bind=engine)

# Create the table in the database
Base = declarative_base()

class Product(Base):
    __tablename__ = 'Product'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    URL = Column(String(2083), nullable=False)
    domain = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price_before_tax = Column(Float, nullable=False)
    price_after_tax = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    image_url = Column(String(2083), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


def create_product(URL, domain, name, description, price_before_tax, price_after_tax, tax, currency, image_url):
    """
    Creates a new product record in the database.

    Args:
        URL (str): The URL of the product.
        domain (str): The domain of the product.
        name (str): The name of the product.
        description (str): A detailed description of the product.
        price_before_tax (float): The price of the product before tax.
        price_after_tax (float): The price of the product after tax.
        tax (float): The tax applied to the product.
        currency (str): The currency of the product.
        image_url (str): The URL of the product's image.

    Returns:
        int: The ID of the created product.
    """

    # Create a session and add the product
    try:
        session = Session()
        new_product = Product(
            URL=URL,
            domain=domain,
            name=name,
            description=description,
            price_before_tax=price_before_tax,
            price_after_tax=price_after_tax,
            tax=tax,
            currency=currency,
            image_url=image_url
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)  # Refresh to get the updated object with id
        session.close()
        
        print(f"Created record for {URL}. New ID: {new_product.id}")
        
        return new_product.id  # Return the created product's ID
    except Exception as e:
        print(e)
        return -1


def read_product_by_url(URL:str):
    """
    Reads a product record from the database by its URL.

    Args:
        URL (str): The URL of the product.

    Returns:
        Optional[Product]: The product object if found, None otherwise.
    """
    print(f"Input URL: {URL}")
   
    # Create session and query the database
    session = Session()
    product = session.query(Product).filter(Product.URL == URL).order_by(desc(Product.id)).first()
    session.close()
    
    print(f"Found {product.name} for {URL}")
    
    return str(product.__dict__)  # Returns the product object or None if not found

def read_all_products():
    """
    Reads all product records from the database.

    Returns:
        List[Product]: A list of product objects.
    """
    
    session = Session()
    products = session.query(Product).all()
    session.close()
    
    return products  # Returns a list of product objects


# if __name__ == "__main__":
#     # Create a new product
#     # product_id = create_product(
#     #     'https://example.com/product1', 'example.com', 'Wireless Headphones',
#     #     'High-quality wireless headphones with noise cancellation.', 150.00, 177.00, 27.00, 'USD',
#     #     'https://example.com/images/headphones.jpg'
#     # )
#     # print(f"Created product with ID: {product_id}")

#     # Read a product by URL
#     product = read_product_by_url('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
#     print(f"Product: {product}")

#     # Read all products
#     # all_products = read_all_products()
#     # for p in all_products:
#     #     print(f"Product: {p.name}, {p.description}, {p.image_url}, {p.URL}, {p.created_at}, {p.domain}, {p.currency}, {p.price_before_tax}, {p.price_after_tax}, {p.tax}")
