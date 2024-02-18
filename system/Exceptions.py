# 當驗證失敗時，會引發此異常
class ValidationError(Exception):
    pass

# 當沒有權限存取此資源時，會引發此異常
class UnauthorizedError(Exception):
    pass