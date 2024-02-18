from sqlalchemy.orm import Session
from db.SqlliteConnection import SqlliteConnection
from model.orm.Task import Task
from datetime import datetime

class TaskDAO:
    
    def __init__(self):
        self.engine = SqlliteConnection.get_connection(SqlliteConnection.TASKS_DB)
        
    def create_task(self, user_id, name) -> Task:
        with Session(self.engine) as session:
            task = Task(user_id=user_id, name=name)
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        
    def find_by_id(self, user_id, id) -> Task:
        with Session(self.engine) as session:
            task = session.query(Task).filter_by(user_id=user_id, id=id, deleted_at=None).first()
            return task
    
    def find_by_name(self, user_id, name) -> Task:
        with Session(self.engine) as session:
            task = session.query(Task).filter_by(user_id=user_id, name=name, deleted_at=None).first()
            return task

    def get_all_tasks_for_user(self, user_id) -> list[Task]:
        with Session(self.engine) as session:
            tasks = session.query(Task).filter_by(user_id=user_id, deleted_at=None).all()
            return tasks
    
    def update_task(self, user_id, id, **kwargs) -> Task:
        with Session(self.engine) as session:
            task = session.query(Task).filter_by(id=id, user_id=user_id, deleted_at=None).first()
            if task is None:
                return None
            for key, value in kwargs.items():
                setattr(task, key, value)
            session.commit()
            session.refresh(task)
            return task
    
    def delete_task(self, user_id, id) -> Task:
        with Session(self.engine) as session:
            task = session.query(Task).filter_by(id=id, user_id=user_id, deleted_at=None).first()
            if task is None:
                return None
            task.deleted_at = datetime.now()
            session.commit()
            session.refresh(task)
            return task