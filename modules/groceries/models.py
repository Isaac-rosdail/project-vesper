# Handles DB setup/functionality & grocery related DB functions
from core.database import get_session, engine
from sqlalchemy.orm import declarative_base

# Making a model for Product (use base classes later but stick with this for now)
## Metadata needed to register the table properly? Investigate later
from sqlalchemy import Table, Column, Integer, String, DECIMAL, Float

Base = declarative_base()

class Product(Base):
	__tablename__ = "product"

	product_id = Column(Integer, primary_key=True)
	product_name = Column(String(100), nullable=False)
	price = Column(DECIMAL(10,2), nullable=False)
	net_weight = Column(Float, nullable=False)

Base.metadata.create_all(engine) # Replaces our old Core style setup_schema function for database setup

# ORM style:
def get_all_products():
	session = get_session()
	products = session.query(Product).all()
	session.close()
	return products

def add_product(barcode):
	session = get_session()
	new_product = Product(product_id=barcode, product_name="Jam", price=1.29, net_weight=20)
	session.add(new_product)
	session.commit()
	session.close()