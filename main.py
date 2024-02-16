import os
import importlib
from dotenv import load_dotenv
from flask import Flask
load_dotenv()

app = Flask(__name__)

## auto require all controller
controller_dir = os.path.join(os.path.dirname(__file__), 'controllers')
for filename in os.listdir(controller_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        module = importlib.import_module('controllers.' + module_name)
        app.register_blueprint(module.defi)

if __name__ == '__main__':
    env = os.getenv('APP_ENV')
    
    debug = False
    if env == 'development':
        debug = True
    
    host = os.getenv('FLASK_HOST')
    port = os.getenv('FLASK_PORT')

    app.run(debug=debug, port=port, host=host)
    