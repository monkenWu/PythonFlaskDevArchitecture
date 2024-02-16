import os
import importlib
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def import_all_orm_model():
    current_dir = os.path.dirname(__file__)

    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            importlib.import_module('.' + module_name, package='model.orm')
