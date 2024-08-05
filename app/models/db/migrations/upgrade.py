from alembic import command, config
from app.models.db import db


def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


def run_downgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    command.downgrade(cfg, "-1")


async def run_async_upgrade():
    async with db.engine.begin() as conn:
        await conn.run_sync(run_upgrade, config.Config("alembic.ini"))


async def run_async_downgrade():
    async with db.engine.begin() as conn:
        await conn.run_sync(run_downgrade, config.Config("alembic.ini"))
