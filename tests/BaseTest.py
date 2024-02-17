import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alembic import command
from alembic.config import Config
from system.EnvLoader import EnvLoader

EnvLoader.is_testing = True

def initialize_database():
    alembic_cfg = Config("alembic.testing.ini")
    alembic_cfg.print_stdout = False
    command.upgrade(alembic_cfg, "head")

def clear_database():
    alembic_cfg = Config("alembic.testing.ini")
    alembic_cfg.print_stdout = False
    command.downgrade(alembic_cfg, "base")