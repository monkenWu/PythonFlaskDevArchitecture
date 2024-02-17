import os
import importlib
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# auto require all controller
versions = ['v1', 'v2']
for version in versions:
    controller_dir = os.path.join(os.path.dirname(__file__), 'controllers', version)
    for filename in os.listdir(controller_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module('controllers.' + version + '.' + module_name)
            app.register_blueprint(module.defi, url_prefix='/api/' + version)

if __name__ == '__main__':
    env = os.getenv('APP_ENV')
    
    debug = False
    if env == 'development':
        debug = True
    
    host = os.getenv('FLASK_HOST')
    port = os.getenv('FLASK_PORT')

    app.run(debug=debug, port=port, host=host)
    