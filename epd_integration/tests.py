"""
EPD API 整合測試
"""
import os
import tempfile
from unittest.mock import Mock, patch
from django.test import TestCase
from django.conf import settings

from .services.api_client import EPDAPIClient
from .exceptions import EPDAuthenticationError, EPDConnectionError
from .models import EPDPlayer, EPDDevice, EPDImage, AuthToken


class EPDAPIClientTest(TestCase):
    """EPD API 客戶端測試"""
    
    def setUp(self):
        self.client = EPDAPIClient()
        self.test_token = "test_token_123"
    
    def test_init_with_token(self):
        """測試使用 token 初始化"""
        client = EPDAPIClient(token=self.test_token)
        self.assertEqual(client.token, self.test_token)
        self.assertIn('Authorization', client.session.headers)
    
    @patch('requests.Session.post')
    def test_authenticate_success(self, mock_post):
        """測試成功認證"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {'token': self.test_token}
        mock_post.return_value = mock_response
        
        result = self.client.authenticate('test@example.com', 'password')
        
        self.assertIsInstance(result, AuthToken)
        self.assertEqual(result.token, self.test_token)
        self.assertEqual(self.client.token, self.test_token)
    
    @patch('requests.Session.post')
    def test_authenticate_failure(self, mock_post):
        """測試認證失敗"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.text = "Invalid credentials"
        mock_post.return_value = mock_response
        
        with self.assertRaises(EPDAuthenticationError):
            self.client.authenticate('test@example.com', 'wrong_password')
    
    @patch('requests.Session.post')
    def test_create_player_success(self, mock_post):
        """測試成功建立播放器"""
        self.client.token = self.test_token
        
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'id': 1,
            'serialnum': 'TEST001',
            'created_time': '2024-01-01T00:00:00Z',
            'update_time': '2024-01-01T00:00:00Z'
        }
        mock_post.return_value = mock_response
        
        result = self.client.create_player('TEST001')
        
        self.assertIsInstance(result, EPDPlayer)
        self.assertEqual(result.serialnum, 'TEST001')
    
    @patch('requests.Session.get')
    def test_list_players_success(self, mock_get):
        """測試成功列出播放器"""
        self.client.token = self.test_token
        
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 1,
                'serialnum': 'TEST001',
                'created_time': '2024-01-01T00:00:00Z',
                'update_time': '2024-01-01T00:00:00Z'
            }
        ]
        mock_get.return_value = mock_response
        
        result = self.client.list_players()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], EPDPlayer)
    
    def test_upload_image_file_handling(self):
        """測試圖片檔案處理"""
        # 建立臨時圖片檔案
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            tmp_file.write(b'fake image data')
            tmp_file_path = tmp_file.name
        
        try:
            # 測試檔案是否可以正確開啟
            with open(tmp_file_path, 'rb') as image_file:
                self.assertIsNotNone(image_file.read())
        finally:
            # 清理臨時檔案
            os.unlink(tmp_file_path)


class EPDModelsTest(TestCase):
    """EPD 模型測試"""
    
    def test_epd_player_creation(self):
        """測試 EPD 播放器模型建立"""
        player = EPDPlayer(id=1, serialnum='TEST001')
        self.assertEqual(player.id, 1)
        self.assertEqual(player.serialnum, 'TEST001')
    
    def test_epd_device_creation(self):
        """測試 EPD 設備模型建立"""
        device = EPDDevice(id=1, order=1)
        self.assertEqual(device.id, 1)
        self.assertEqual(device.order, 1)
        self.assertIsInstance(device.images, list)
        self.assertEqual(len(device.images), 0)
    
    def test_epd_image_creation(self):
        """測試 EPD 圖片模型建立"""
        image = EPDImage(id=1, upload_image='test.jpg')
        self.assertEqual(image.id, 1)
        self.assertEqual(image.upload_image, 'test.jpg')
    
    def test_auth_token_creation(self):
        """測試認證 Token 模型建立"""
        token = AuthToken(token='test_token')
        self.assertEqual(token.token, 'test_token')
        self.assertIsNone(token.user)