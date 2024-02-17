from sqlalchemy.orm import Session
from db.SqlliteConnection import SqlliteConnection
from model.orm.User import User

class UserDAO:
    def __init__(self):
        self.engine = SqlliteConnection.get_connection(SqlliteConnection.TASKS_DB)
        
    def create_user(self, username, hashed_password) -> User:
        with Session(self.engine) as session:
            user = User(username=username, password=hashed_password)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def find_by_username(self, username) -> User:
        with Session(self.engine) as session:
            user = session.query(User).filter_by(username=username).first()
            return user

    def find_by_id(self, id) -> User:
        with Session(self.engine) as session:
            user = session.query(User).filter_by(id=id).first()
            return user