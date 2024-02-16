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
