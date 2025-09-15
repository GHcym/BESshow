"""
EPD API 資料模型
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class EPDPlayer:
    """EPD 播放器模型"""
    id: Optional[int] = None
    serialnum: str = ""
    version: Optional[str] = None
    indicator: Optional[str] = None
    location: Optional[str] = None
    ip: Optional[str] = None
    mac: Optional[str] = None
    heartbeat_interval: Optional[int] = None
    created_time: Optional[datetime] = None
    last_sync: Optional[datetime] = None
    online_status: Optional[bool] = None
    enabled: Optional[bool] = None
    update_time: Optional[datetime] = None
    epds: List['EPDDevice'] = None

    def __post_init__(self):
        if self.epds is None:
            self.epds = []


@dataclass
class EPDDevice:
    """EPD 設備模型"""
    id: Optional[int] = None
    order: int = 1
    updated: bool = False
    created_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    images: List['EPDImage'] = None

    def __post_init__(self):
        if self.images is None:
            self.images = []


@dataclass
class EPDImage:
    """EPD 圖片模型"""
    id: Optional[int] = None
    upload_image: Optional[str] = None
    four_color_image: Optional[str] = None
    converted_image: Optional[str] = None
    created_time: Optional[datetime] = None
    update_time: Optional[datetime] = None


@dataclass
class EPDUser:
    """EPD 使用者模型"""
    email: str
    name: str
    password: Optional[str] = None


@dataclass
class AuthToken:
    """認證 Token 模型"""
    token: str
    user: Optional[EPDUser] = None