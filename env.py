import os
import logging
from sqlalchemy import engine_from_config, pool
from alembic import context
from database.models import Base

# Alembic Config object provides access to values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
logging.basicConfig()
logger = logging.getLogger('alembic.env')

# Retrieve the database URL from environment variable
DATABASE_URL_ENV = "DATABASE_URL"
DATABASE_URL = os.environ.get(DATABASE_URL_ENV)

if not DATABASE_URL:
    raise RuntimeError(f"Environment variable {DATABASE_URL_ENV} is not set.")

# Add the database URL to the Alembic configuration
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Set up metadata for Alembic migrations
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()