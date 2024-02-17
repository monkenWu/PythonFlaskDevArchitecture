import os
import importlib
from flask import Flask
from flask_jwt_extended import JWTManager
from system.EnvLoader import EnvLoader

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] =  EnvLoader.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# auto require all controller
versions = ['v1', 'v2']
for version in versions:
    controller_dir = os.path.join(os.path.dirname(__file__), 'controllers', version)
    files = os.listdir(controller_dir)
    for filename in files:
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            importName = 'controllers.' + version + '.' + module_name
            module = importlib.import_module(importName)
            app.register_blueprint(module.defi, url_prefix='/api/' + version)
            
if __name__ == '__main__':
    env = EnvLoader.getenv('APP_ENV')
    
    debug = False
    if env == 'development':
        debug = True
    
    host = EnvLoader.getenv('FLASK_HOST')
    port = EnvLoader.getenv('FLASK_PORT')

    app.run(debug=debug, port=port, host=host)
    