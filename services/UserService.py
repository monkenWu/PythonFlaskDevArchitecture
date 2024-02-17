from model.UserDAO import UserDAO
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from system.EnvLoader import EnvLoader

class UserService:

    def __init__(self):
        self.user_dao = UserDAO()

    @staticmethod
    def get_current_user_id():
        try:
            current_user = get_jwt_identity()
            return current_user['id']
        except Exception as e:
            # 驗證失敗
            return {"error": str(e)}
    
    @staticmethod
    def get_current_user_name():
        try:
            current_user = get_jwt_identity()
            return current_user['username']
        except Exception as e:
            # 驗證失敗
            return {"error": str(e)}

    # 註冊使用者，成功回傳使用者物件，若使用者已存在則回傳None
    def register(self, username, password):
        existing_user = self.user_dao.find_by_username(username)
        if existing_user:
            return None
        hashed_password = generate_password_hash(password)
        user = self.user_dao.create_user(username, hashed_password)
        return user

    # 登入，成功回傳JWT令牌，失敗回傳None
    def login(self, username, password):
        user = self.user_dao.find_by_username(username)
        if user and check_password_hash(user.password, password):
            access_token_expires = float(EnvLoader.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
            access_token = create_access_token(
                identity={
                    "id": user.id,
                    "username": user.username
                },
                expires_delta=timedelta(seconds=access_token_expires)
            )
            return access_token
        return None

    # 取得使用者資訊
    def get_user_info(self, username):
        user = self.user_dao.find_by_username(username)
        if user:
            return {
                "id": user.id,
                "username": user.username,
            }
        return None
