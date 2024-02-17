from sqlalchemy import create_engine, exc, text
from sqlalchemy.engine import Engine
from system.EnvLoader import EnvLoader

class SqlliteConnection:
    TASKS_DB = "TASKS"
    engines = {}

    @classmethod
    def get_engine(cls, db_name) -> Engine:
        if db_name not in cls.engines:
            database_path = EnvLoader.getenv(f'SQLITE_{db_name}_PATH')
            url = f"sqlite:///{database_path}"
            try:
                print(f"Try to connect SQLite DB: {db_name}", end='...')
                engine = create_engine(url)
                with engine.connect() as conn:
                     # 執行一個簡單的查詢來驗證連接
                    conn.execute(text("SELECT 1"))
                cls.engines[db_name] = engine
                print("OK!")

            except exc.SQLAlchemyError as e:
                print(f"SQLite Connection Error: {e}, Database Path: {database_path}")
                return None
        return cls.engines[db_name]

    @staticmethod
    def get_connection(db_name):
        return SqlliteConnection.get_engine(db_name)

    @staticmethod
    def close_connection():
        for engine in SqlliteConnection.engines.values():
            engine.dispose() 
        SqlliteConnection.engines = {}
