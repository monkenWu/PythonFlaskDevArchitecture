# PythonTasks

## Environment

### 初次部署

#### 透過 docker-compose.yml 部署開發環境

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

### 路由規則

所有 Controller 底下 `v{version}` 的路由都會以 `/api/{version}` 開頭。舉個例子：
* 置於 `{project_root}/controllers/v2/IndexController.py` 的以下路由

    ```python
    @defi.route('/', methods=['GET'])
    def index_page():
        return jsonify(status=200, msg={
            "message": "Server is running, This is version 2 API."
    })
    ```
    將會被註冊成 `/api/v2/` 。
