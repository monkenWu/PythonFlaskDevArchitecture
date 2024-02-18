# Python Flask Dev Architecture

這是一個基於 Flask 的 API 伺服器開發架構示範。

在這個示範中整合了一些常用的開發工具，並且提供了一個基本的開發環境。包含以下特性：

* 使用 `docker-compose` 部署開發環境
* 使用 `sqllib` 進行資料庫操作
* 使用 `alembic` 進行資料庫 Migration
* 使用 `SQLAlchemy` 作為 ORM，並且提供基本的 Model 設計
* 使用 `unittest` 進行單元測試，提供基本的測試行為與獨立的測試環境組態設定
* 使用 `flask` 進行 API 開發，並且進行 API 版本控制
* 使用 `logging` 進行日誌記錄，提供統一的日誌管理介面
* 使用 `flask` 內建的錯誤處理機制，並且提供統一的錯誤處理介面
* 建立 Controller-Service-DAO 的開發架構

## Feature

在專案內已包含了一些 APIs 與相關的測試，你可以透過在啟動開發環境後進行基本的測試。你可以在專案根目錄中找到 `APIs.postman_collection.json` 檔案，這是一個 Postman Collection 檔案，你可以透過 Postman 進行 API 測試，這些 API 在設計上依循 RESTful API 的設計原則。

在專案內提供以下的功能模組：
* 使用者
    * 註冊
    * 登入 - 取得 Access Token
    * 取得使用者資訊
* 任務
    * 新增任務
    * 取得任務列表
    * 取得任務資訊
    * 更新任務 - 完整更新
    * 更新任務 - 部分更新
    * 刪除任務

## Environment

本專案將透過 docker-compose.yml 部署開發環境

### 初次部署

* 建構環境
    ```bash
    docker-compose build
    ```
    > 如果需要重頭建構 image 可以同時在指令後面使用 `--no-cache` 選項
* 執行容器
    ```bash
    docker-compose up
    ```
    > 如果需要背景執行可以使用 `-d` 選項
* 進入容器
    ```bash
    docker-compose exec app bash
    ```
    > 你也可以透過 VSCode 的 Remote - Containers 擴充套件進入容器開發

* 將 `env.example` 複製成 `.env` 並調整組態設定使其符合需求
* 初始化資料庫
    ```bash
    alembic upgrade head
    ```
* 執行開發伺服器
    ```bash
    python main.py
    ```

### 更新 pip 依賴

當你在專案中新增了新的依賴，你需要更新 `requirements.txt` 檔案。

```bash
pip freeze > requirements.txt
```

再次建構環境

```bash
docker-compose build
```

## Database Migration

資料庫 Migration 使用 `alembic`，並且使用 `SQLAlchemy` 作為 ORM。 
`alembic` 會自動掃描 `models.orm` Package 下的所有 Model 並且生成對應的 Migration。

### 更新 Migration Versiom

若對於資料庫的 Schema 進行了修改，則需要更新 Migration Version。

```bash
alembic revision --autogenerate -m "message"
```

### 執行 Migration

```bash
alembic upgrade head
```

## Controller and API Version Control

所有 `controllers` 底下的資料夾都會被自動地掃描並且註冊成 API 路由。

API 將透過 `controllers` 底下的資料夾進行版本控制，每個資料夾代表一個版本的 API。

### 新增 API 版本

* 新增一個資料夾，並且命名為 `v{version}`，例如 `v1`
* 在 main.py 中調整以下程式
    ```python
    ## auto require all controller
    versions = ['v1', 'v2', 'v{version}']
    ```
* 在新的 `v{version}` 資料夾中開始新增新的 Controller

### 新增 Controller

在 `v{version}` 資料夾中新增一個新的 Controller，例如 `IndexController.py`

```python
from flask import Blueprint, jsonify
from system.LogManager import LogManager

defi = Blueprint('v1_index_api', __name__)

@defi.route('/', methods=['GET'])
def index_page():
    access_log = LogManager.get_logger('access_log', LogManager.LOG_INFO)
    access_log.write('Access index page', LogManager.LOG_INFO)
    return jsonify(status=200, msg={
        "message": "Server is running. This is version 1 API."
    })
```

defi 是一個 Flask Blueprint 實體，他將會被註冊成一個 API 路由。你一定得透過 defi 作為 Blueprint('v1_index_api', __name__) 的 Blueprint 名稱，這樣才能被 `main.py` 正確地自動註冊。

### 路由規則

所有 Controller `v{version}` 底下的路由都會以 `/api/{version}` 開頭。舉個例子：

置於 `{project_root}/controllers/v2/IndexController.py` 的以下路由

```python
@defi.route('/', methods=['GET'])
def index_page():
    return jsonify(status=200, msg={
        "message": "Server is running, This is version 2 API."
})
```

將會被註冊成 `/api/v2/` 。

## 執行單元測試

專案使用 `unittest` 作為單元測試框架，所有的單元測試都會置於 `tests` 資料夾底下。在執行單元測試前，請確保根目錄下的 `.testing.env` 與 `alembic.testing.ini` 檔案已經設定好。

### 執行測試

* 執行單個測試
    ```bash
    python -m unittest tests/v1/TestUserCase.py
    ```
* 執行全部測試
    ```bash
    python -m unittest discover -s ./tests/v1 -p 'Test*.py'
    ```

### 建立新的測試

一個測試檔案應該繼承 `unittest.TestCase` 並且在 `setUp` 方法中初始化測試環境，並且在 `tearDown` 方法中清理測試環境。

請於合適的地方建立一個以 `Test` 開頭的測試檔案，並讓他看起來像是以下的程式碼：

```python
from tests.BaseTest import initialize_database, clear_database
import unittest
from main import app

class TestUserCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        initialize_database()
        
    def tearDown(self):
        self.ctx.pop()
        clear_database()

```

上述程式碼中的 `initialize_database` 與 `clear_database` 是用來初始化與清理測試資料庫的方法，這個測試用資料庫將會依賴 `.testing.env` 與 `alembic.testing.ini` 檔案中的相關設定。

## 錯誤處理

專案使用 `flask` 內建的錯誤處理機制，並且透過 `logging` 模組進行日誌的記錄。

### 錯誤處理

錯誤處理的程式碼位於 `main.py` 中，並且透過 `@app.errorhandler` 裝飾器進行註冊。若在程式中出現無法處理的錯誤，那麼將會統一拋出 HTTP 500 錯誤。

當 `.env` 中的 `APP_ENV` 設定為 `development` 時，錯誤處理將會回傳詳細的錯誤訊息，否則將會回傳一個簡單的錯誤訊息。

舉個例子：

* development 環境響應的錯誤資訊
    ```json
    {
        "details": [
            "Traceback (most recent call last):",
            "  File \"/usr/local/lib/python3.9/site-packages/flask/app.py\", line 870, in full_dispatch_request",
            "    rv = self.dispatch_request()",
            "  File \"/usr/local/lib/python3.9/site-packages/flask/app.py\", line 855, in dispatch_request",
            "    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]",
            "  File \"/app/controllers/v1/UserController.py\", line 10, in register",
            "    sdfds",
            "NameError: name 'sdfds' is not defined"
        ],
        "message": "name 'sdfds' is not defined"
    }
    ```
* production 環境響應的錯誤資訊
    ```json
    {
        "message": "Internal Server Error"
    }
    ```

### 拋出錯誤

你可以透過 `system.Exceptions` 底下的類別在你的 Controller 或是 Service 中拋出錯誤。框架會自動地將這些錯誤訊息轉換成 HTTP 響應。

舉了一個例子：

```python
from system.Exceptions import ValidationError

def create_task(self, user_id, name):
    task = self.task_dao.find_by_name(user_id, name)
    if task:
        raise ValidationError(f'Task {name} already exists')
```

此時，當 `create_task` 方法被呼叫時，若 `task` 已經存在，則會拋出一個 HTTP 400 錯誤，並且響應以下的訊息：

```json
{
    "message": "Task {name} already exists"
}
```

## 日誌

專案內的日誌統一由 `system.LogManager` 進行管理，他是一個 Singleton 類別，並且透過 `logging` 模組進行日誌的記錄。所有的 Log 將統一被寫入到 `writable/logs` 資料夾底下，相同的日誌最多留存 3 天。

### 系統預設錯誤日誌

系統錯誤將會被記錄在 `writable/logs/app_error.log`。當無法預期的錯誤發生時，將會被記錄在這個日誌中。就像這樣：

```log
2024-02-18 01:00:38,773 - ERROR - name 'sdfds' is not defined
Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 870, in full_dispatch_request
    rv = self.dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 855, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]

  File "/app/controllers/v1/UserController.py", line 10, in register
    sdfds

NameError: name 'sdfds' is not defined
```

### 建立你自己的日誌

你可以透過 `system.LogManager` 類別建立你自己的日誌，使用 `get_logger` 方法取得 Logger 實體。舉個例子：

```python
from flask import Blueprint, jsonify
from system.LogManager import LogManager

defi = Blueprint('v1_index_api', __name__)

@defi.route('/', methods=['GET'])
def index_page():
    access_log = LogManager.get_logger('access_log', LogManager.LOG_INFO)
    access_log.write('Access index page', LogManager.LOG_INFO)
    return jsonify(status=200, msg={
        "message": "Server is running. This is version 1 API."
    })
```

上述程式碼中的 `access_log` 將會記錄在 `writable/logs/access_log.log` 中。
