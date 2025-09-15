"""
EPD API 客戶端服務
"""
import requests
import logging
from typing import Optional, List, Dict, Any
from django.conf import settings

from ..exceptions import (
    EPDAPIException, EPDAuthenticationError, EPDConnectionError,
    EPDValidationError, EPDNotFoundError
)
from ..models import EPDPlayer, EPDDevice, EPDImage, AuthToken


logger = logging.getLogger(__name__)


class EPDAPIClient:
    """EPD API 客戶端"""
    
    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or getattr(settings, 'EPD_API_BASE_URL', 'http://43.213.2.34/api')
        self.token = token
        self.session = requests.Session()
        
        if self.token:
            self.session.headers.update({
                'Authorization': f'Token {self.token}',
                'Content-Type': 'application/json'
            })
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """處理 API 回應"""
        try:
            if response.status_code == 401:
                raise EPDAuthenticationError("認證失敗")
            elif response.status_code == 404:
                raise EPDNotFoundError("資源不存在")
            elif response.status_code == 400:
                raise EPDValidationError(f"資料驗證錯誤: {response.text}")
            elif not response.ok:
                raise EPDAPIException(f"API 錯誤 {response.status_code}: {response.text}")
            
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            raise EPDConnectionError(f"連線錯誤: {str(e)}")
    
    def authenticate(self, email: str, password: str) -> AuthToken:
        """使用者認證"""
        try:
            response = self.session.post(
                f"{self.base_url}/user/token/",
                data={'email': email, 'password': password}
            )
            data = self._handle_response(response)
            
            token = data.get('token')
            if not token:
                raise EPDAuthenticationError("認證回應中缺少 token")
            
            self.token = token
            self.session.headers.update({'Authorization': f'Token {token}'})
            
            return AuthToken(token=token)
        except Exception as e:
            logger.error(f"認證失敗: {str(e)}")
            raise
    
    # Player Management
    def create_player(self, serialnum: str) -> EPDPlayer:
        """建立播放器"""
        try:
            response = self.session.post(
                f"{self.base_url}/player/",
                json={'serialnum': serialnum}
            )
            data = self._handle_response(response)
            return EPDPlayer(**data)
        except Exception as e:
            logger.error(f"建立播放器失敗: {str(e)}")
            raise
    
    def get_player(self, player_id: int) -> EPDPlayer:
        """取得播放器資訊"""
        try:
            response = self.session.get(f"{self.base_url}/player/{player_id}/")
            data = self._handle_response(response)
            
            # 處理嵌套的 EPD 資料
            if 'epds' in data and data['epds']:
                epd_objects = []
                for epd_data in data['epds']:
                    # 處理嵌套的圖片資料
                    if 'images' in epd_data and epd_data['images']:
                        image_objects = [EPDImage(**img_data) for img_data in epd_data['images']]
                        epd_data['images'] = image_objects
                    epd_objects.append(EPDDevice(**epd_data))
                data['epds'] = epd_objects
            
            return EPDPlayer(**data)
        except Exception as e:
            logger.error(f"取得播放器失敗: {str(e)}")
            raise
    
    def list_players(self, serialnum: str = None) -> List[EPDPlayer]:
        """列出播放器"""
        try:
            params = {'serialnum': serialnum} if serialnum else {}
            response = self.session.get(f"{self.base_url}/player/players/", params=params)
            data = self._handle_response(response)
            return [EPDPlayer(**item) for item in data]
        except Exception as e:
            logger.error(f"列出播放器失敗: {str(e)}")
            raise
    
    # EPD Management
    def create_epd(self, player_id: int, order: int = 1) -> EPDDevice:
        """建立 EPD 設備"""
        try:
            response = self.session.post(
                f"{self.base_url}/player/{player_id}/epd/",
                json={'order': order}
            )
            data = self._handle_response(response)
            return EPDDevice(**data)
        except Exception as e:
            logger.error(f"建立 EPD 設備失敗: {str(e)}")
            raise
    
    def get_epd(self, epd_id: int) -> EPDDevice:
        """取得 EPD 設備資訊"""
        try:
            response = self.session.get(f"{self.base_url}/player/epd/{epd_id}/")
            data = self._handle_response(response)
            return EPDDevice(**data)
        except Exception as e:
            logger.error(f"取得 EPD 設備失敗: {str(e)}")
            raise
    
    def update_epd(self, epd_id: int, order: int = None, updated: bool = None) -> EPDDevice:
        """更新 EPD 設備"""
        try:
            update_data = {}
            if order is not None:
                update_data['order'] = order
            if updated is not None:
                update_data['updated'] = updated
            
            response = self.session.patch(
                f"{self.base_url}/player/epd/{epd_id}/",
                json=update_data
            )
            data = self._handle_response(response)
            return EPDDevice(**data)
        except Exception as e:
            logger.error(f"更新 EPD 設備失敗: {str(e)}")
            raise
    
    def list_epds(self, epd_id: str = None) -> List[EPDDevice]:
        """列出 EPD 設備"""
        try:
            params = {'epd_id': epd_id} if epd_id else {}
            response = self.session.get(f"{self.base_url}/player/epds/", params=params)
            data = self._handle_response(response)
            return [EPDDevice(**item) for item in data]
        except Exception as e:
            logger.error(f"列出 EPD 設備失敗: {str(e)}")
            raise
    
    # Image Management
    def upload_image(self, epd_id: int, image_file) -> EPDImage:
        """上傳圖片到 EPD"""
        try:
            files = {'upload_image': image_file}
            # 移除 Content-Type header 讓 requests 自動設定 multipart/form-data
            headers = {'Authorization': f'Token {self.token}'}
            
            response = requests.post(
                f"{self.base_url}/player/epd/{epd_id}/image/",
                files=files,
                headers=headers
            )
            data = self._handle_response(response)
            return EPDImage(**data)
        except Exception as e:
            logger.error(f"上傳圖片失敗: {str(e)}")
            raise
    
    def get_image(self, image_id: int) -> EPDImage:
        """取得圖片資訊"""
        try:
            response = self.session.get(f"{self.base_url}/player/image/{image_id}/")
            data = self._handle_response(response)
            return EPDImage(**data)
        except Exception as e:
            logger.error(f"取得圖片失敗: {str(e)}")
            raise
    
    def list_images(self, image_id: str = None) -> List[EPDImage]:
        """列出圖片"""
        try:
            params = {'id': image_id} if image_id else {}
            response = self.session.get(f"{self.base_url}/player/images/", params=params)
            data = self._handle_response(response)
            return [EPDImage(**item) for item in data]
        except Exception as e:
            logger.error(f"列出圖片失敗: {str(e)}")
            raise
    
    def delete_image(self, image_id: int) -> bool:
        """刪除圖片"""
        try:
            response = self.session.delete(f"{self.base_url}/player/image/{image_id}/")
            self._handle_response(response)
            return True
        except Exception as e:
            logger.error(f"刪除圖片失敗: {str(e)}")
            raise