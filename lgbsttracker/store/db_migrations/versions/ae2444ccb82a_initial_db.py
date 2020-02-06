"""initial db

Revision ID: ae2444ccb82a
Revises: 
Create Date: 2020-01-28 10:51:41.173284

"""
import datetime
import logging

from alembic import op
from sqlalchemy import CheckConstraint, Column, DateTime, Float, Index, Integer, PrimaryKeyConstraint, String, orm

from lgbsttracker.entities.experiment import ExperimentAction, ExperimentState

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

# revision identifiers, used by Alembic.
revision = "ae2444ccb82a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    _logger.info("Initial database creation.")

    # Experiment table
    op.create_table(
        "experiment",
        Column("id", Integer, autoincrement=True),
        Column("experiment_uuid", String(32), nullable=False),
        Column("ts", DateTime, default=str(datetime.datetime.now())),
        Column("action", String(32), default=ExperimentAction.NONE),
        Column("vision_sensor", Float, nullable=True),
        Column("speed", Float, nullable=True),
        Column("state", String(32), default=ExperimentState.STOPPED),
        # Primary Key
        PrimaryKeyConstraint("id", name="experiment_pk"),
        # Check Constraint
        CheckConstraint("action IN ('none', 'forward', 'backward', 'left', 'right')", name="experiment_checkaction",),
        CheckConstraint("state IN ('stopped', 'failed', 'running', 'finished')", name="experiment_checkstate",),
        # Index creation
        Index("experiment_index1", "experiment_uuid"),
    )

    session.commit()

    _logger.info("Database creation completed.")


def downgrade():
    pass
