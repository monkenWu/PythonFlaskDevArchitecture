import os
import traceback
import importlib
from flask import Flask
from flask import jsonify
from flask_jwt_extended import JWTManager
from system.EnvLoader import EnvLoader
from system.LogManager import LogManager

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

# 設定全域錯誤處理
# 直接初始化基本的系統 log
app_error_log = LogManager.get_logger(LogManager.APP_ERROR_LOG, LogManager.LOG_ERROR)
@app.errorhandler(Exception)
def handle_error(e):
    env = EnvLoader.getenv('APP_ENV')
    if env == 'development' or env == 'testing':
        detail_list = ''.join(traceback.format_exception(None, e, e.__traceback__)).splitlines()
        response = {
            'message' : str(e),
            'details' : detail_list
        }
    else:
        response = {
            'message' : 'Internal server error'
        }
    
    # 寫入錯誤 log
    app_error_log.write(
        str(e) + '\n' + '\n'.join(traceback.format_exception(None, e, e.__traceback__)),
        LogManager.LOG_ERROR
    )
    return jsonify(response), 500

if __name__ == '__main__':
    env = EnvLoader.getenv('APP_ENV')
    
    debug = False
    if env == 'development':
        debug = True
    
    host = EnvLoader.getenv('FLASK_HOST')
    port = EnvLoader.getenv('FLASK_PORT')

    app.run(debug=debug, port=port, host=host)
    