"""AWS Lambda entrypoint for the FastAPI BudgetBot app."""
from mangum import Mangum

from src.app import app


handler = Mangum(app)
