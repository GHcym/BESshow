"""
EPD API 例外處理類別
"""


class EPDAPIException(Exception):
    """EPD API 基礎例外"""
    pass


class EPDAuthenticationError(EPDAPIException):
    """認證失敗例外"""
    pass


class EPDConnectionError(EPDAPIException):
    """連線錯誤例外"""
    pass


class EPDValidationError(EPDAPIException):
    """資料驗證錯誤例外"""
    pass


class EPDNotFoundError(EPDAPIException):
    """資源不存在例外"""
    pass