"""Alembic ?˜ê²½ ?¤ì •."""
import os
# Alembic ?¤í–‰ ì¤‘ìž„??ê°€??ë¨¼ì? ?œì‹œ (?¤ë¥¸ import ?„ì— ?¤ì •)
os.environ["ALEMBIC_CONTEXT"] = "1"

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection

from alembic import context

# labzang.core ?¤ì • import
from labzang.core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_url():
    """?°ì´?°ë² ?´ìŠ¤ URL ë°˜í™˜."""
    database_url = settings.database_url
    # Alembic?€ asyncpgë¥??¬ìš©?˜ì? ?Šìœ¼ë¯€ë¡?postgresql://ë¡?ë³€??    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return database_url


# ëª¨ë¸?¤ì´ ?¬ìš©?˜ëŠ” Baseë¥?import (ëª¨ë¸ê³??™ì¼??Base ?¬ìš©)
# ëª¨ë¸?¤ì´ Base.metadata???±ë¡?˜ë„ë¡?import ?„ìˆ˜
from labzang.shared.bases import Base
from labzang.apps.soccer.models.bases.players import Player
from labzang.apps.soccer.models.bases.teams import Team
from labzang.apps.soccer.models.bases.schedules import Schedule
from labzang.apps.soccer.models.bases.stadiums import Stadium
from labzang.apps.soccer.models.bases.player_embeddings import PlayerEmbedding
from labzang.apps.soccer.models.bases.schedule_embeddings import ScheduleEmbedding
from labzang.apps.soccer.models.bases.stadium_embeddings import StadiumEmbedding
from labzang.apps.soccer.models.bases.team__embeddings import TeamEmbedding

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
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

