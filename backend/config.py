import os


# Database configuration.
# Defaults to SQLite for local development.
DATABASE_URL = os.getenv(
    "SUPPLYPRESCRIPT_DATABASE_URL",
    "sqlite:///./supplyprescript.db",
)