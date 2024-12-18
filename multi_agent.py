import os
import json
from io import StringIO
from pydantic import BaseModel, Field
from datetime import datetime
from dotenv import load_dotenv
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool
from markdownify import markdownify as md

from tools.scraper import scrape_url
from tools.database_ops import create_product, read_product_by_url
from tools.mail import send_email

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

import warnings
warnings.filterwarnings('ignore')


class ProductDetails(BaseModel):
    URL: str = Field(..., description="The product page URL that was given as input")
    name: str = Field(..., description="The name of the product")
    description: str = Field(..., description="A detailed description of the product, including content highlights.")
    price_before_tax: float = Field(description='Price before Tax')
    price_after_tax: float = Field(description='Price after Tax')
    tax: float = Field(description='Tax')
    currency: str = Field(description='Curreny')
    image_url: str = Field(...,description='Image URL of the product')

class MonitoringAgentResponse(BaseModel):
    message: str = Field(..., description="This field will have information whether there was change in price along with details of price scraped and price in the database")    


scraper_agent = Agent(
    'openai:gpt-4o-mini',
    result_type=ProductDetails,
    system_prompt = (
        "You are a Scraper Agent. Your tasks are as follows:\n"
        "1. Receive the URL of a product.\n"
        "2. Extract the product and pricing information from the given URL."
    ),
    tools=[Tool(scrape_url, takes_ctx=False)]
)


monitoring_agent = Agent(
    'openai:gpt-4o-mini',
    result_type=MonitoringAgentResponse,
    deps_type=ProductDetails,    
    system_prompt = (
        "You are a Price Monitoring Agent. Your tasks are as follows:\n"
        "1. You will receive the URL of a product along with its product and pricing information from the scraper_agent.\n"
        "2. Check the database for the same product and thoroughly review the response.\n"
        "3. Compare the price information from the scraper_agent with the database.\n"
        "   - If there is a price difference, send an email highlighting the difference and the URL of the product.\n"
        "   - If there is no price difference, do not send any email.\n"
        "4. Store the product and pricing data received from the scraper_agent into the database."
    ),
    tools=[Tool(read_product_by_url, takes_ctx=False), Tool(create_product, takes_ctx=False), Tool(send_email, takes_ctx=False)]
)


@monitoring_agent.system_prompt
async def add_customer_name(ctx: RunContext[ProductDetails]) -> str:
    return f"Customer details: {str(ctx.deps)}"


product_url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

result = scraper_agent.run_sync(product_url)
product = result.data

# product = ProductDetails(name="Test", description="test desc",price_before_tax=100.0, price_after_tax=100.0, currency="usd",tax=0, image_url='someurl')
print(f"URL: {product.URL}")
print()
print(f"Name: {product.name}")
print()
print(f"Description: {product.description}")
print()
print(f"Price Before Tax: {product.price_before_tax}")
print()
print(f"Price After Tax: {product.price_after_tax}")
print()
print(f"Tax: {product.tax}")
print()
print(f"Currency: {product.currency}")
print()
print(f"Image: {product.image_url}")


final_result = monitoring_agent.run_sync(user_prompt='Use product details to monitor price change',deps=product)
response = final_result.data

print(f"Message: {response.message}")

