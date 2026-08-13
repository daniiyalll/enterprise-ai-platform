from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys
import os

# Make the "app" package importable when running alembic from backend/
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import settings
from app.database.base import Base

# Import every model so Base.metadata knows about all tables
from app.models import user        # noqa: F401
from app.models import workflow    # noqa: F401
from app.models import decision    # noqa: F401
from app.models import audit_log   # noqa: F401
from app.models import project     # noqa: F401
from app.models import dataset     # noqa: F401
from app.models import ai_model    # noqa: F401

# this is the Alembic Config object, which provides access to values
# within the .ini file in use.
config = context.config

# Override the sqlalchemy.url from alembic.ini with the real DATABASE_URL
# from backend/.env, so there's only one place the DB connection is configured.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
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


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
