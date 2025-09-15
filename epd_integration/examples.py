"""
EPD API 使用範例
"""
from django.conf import settings
from .services.api_client import EPDAPIClient
from .exceptions import EPDAPIException


def example_basic_usage():
    """基本使用範例"""
    try:
        # 建立 API 客戶端
        client = EPDAPIClient()
        
        # 認證
        email = settings.EPD_API_EMAIL
        password = settings.EPD_API_PASSWORD
        auth_token = client.authenticate(email, password)
        print(f"認證成功，Token: {auth_token.token}")
        
        # 列出所有播放器
        players = client.list_players()
        print(f"找到 {len(players)} 個播放器")
        
        # 列出所有 EPD 設備
        epds = client.list_epds()
        print(f"找到 {len(epds)} 個 EPD 設備")
        
        return True
        
    except EPDAPIException as e:
        print(f"EPD API 錯誤: {e}")
        return False


def example_create_player_and_epd():
    """建立播放器和 EPD 設備範例"""
    try:
        client = EPDAPIClient()
        
        # 認證
        auth_token = client.authenticate(
            settings.EPD_API_EMAIL,
            settings.EPD_API_PASSWORD
        )
        
        # 建立新播放器
        player = client.create_player("TEMPLE_001")
        print(f"建立播放器成功，ID: {player.id}")
        
        # 為播放器建立 EPD 設備
        epd = client.create_epd(player.id, order=1)
        print(f"建立 EPD 設備成功，ID: {epd.id}")
        
        return player, epd
        
    except EPDAPIException as e:
        print(f"建立失敗: {e}")
        return None, None


def example_upload_image():
    """上傳圖片範例"""
    try:
        client = EPDAPIClient()
        
        # 認證
        client.authenticate(
            settings.EPD_API_EMAIL,
            settings.EPD_API_PASSWORD
        )
        
        # 取得第一個 EPD 設備
        epds = client.list_epds()
        if not epds:
            print("沒有可用的 EPD 設備")
            return None
        
        epd = epds[0]
        
        # 上傳圖片（需要實際的圖片檔案）
        # with open('path/to/image.jpg', 'rb') as image_file:
        #     image = client.upload_image(epd.id, image_file)
        #     print(f"上傳圖片成功，ID: {image.id}")
        #     return image
        
        print("請提供實際的圖片檔案路徑來測試上傳功能")
        return None
        
    except EPDAPIException as e:
        print(f"上傳圖片失敗: {e}")
        return None


def example_update_epd_content():
    """更新 EPD 內容範例（點燈流程整合用）"""
    try:
        client = EPDAPIClient()
        
        # 認證
        client.authenticate(
            settings.EPD_API_EMAIL,
            settings.EPD_API_PASSWORD
        )
        
        # 取得 EPD 設備
        epds = client.list_epds()
        if not epds:
            print("沒有可用的 EPD 設備")
            return False
        
        epd = epds[0]
        
        # 標記 EPD 需要更新
        updated_epd = client.update_epd(epd.id, updated=True)
        print(f"EPD {updated_epd.id} 已標記為需要更新")
        
        return True
        
    except EPDAPIException as e:
        print(f"更新 EPD 失敗: {e}")
        return False


# 點燈流程整合範例
def integrate_with_lantern_lighting(order_id, customer_name, prayer_text):
    """
    與點燈流程整合的範例
    
    Args:
        order_id: 訂單 ID
        customer_name: 客戶姓名
        prayer_text: 祈福文字
    """
    try:
        client = EPDAPIClient()
        
        # 認證
        client.authenticate(
            settings.EPD_API_EMAIL,
            settings.EPD_API_PASSWORD
        )
        
        # 這裡可以根據訂單資訊選擇適當的 EPD 設備
        # 例如：根據點燈類型、位置等選擇對應的電子紙
        epds = client.list_epds()
        if not epds:
            raise EPDAPIException("沒有可用的 EPD 設備")
        
        # 選擇第一個可用的 EPD（實際應用中需要更複雜的邏輯）
        target_epd = epds[0]
        
        # 生成點燈內容圖片（這部分需要在後續任務中實作）
        # image_content = generate_lantern_image(customer_name, prayer_text)
        
        # 上傳圖片到 EPD
        # with open(image_content, 'rb') as image_file:
        #     image = client.upload_image(target_epd.id, image_file)
        
        # 標記 EPD 需要更新
        client.update_epd(target_epd.id, updated=True)
        
        print(f"點燈內容已更新到 EPD {target_epd.id}")
        return True
        
    except EPDAPIException as e:
        print(f"點燈流程整合失敗: {e}")
        return False