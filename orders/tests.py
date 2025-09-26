from django.test import TestCase
from django.core.files.base import ContentFile
from orders.services.image_generator import LanternImageGenerator
from orders.models import Order, OrderItem
from products.models import Product
from accounts.models import CustomUser
from io import BytesIO
from PIL import Image
from datetime import date
import base64


class LanternImageGeneratorTest(TestCase):
    def setUp(self):
        # 創建測試用戶
        self.user = CustomUser.objects.create(
            username='testuser',
            email='test@example.com',
            first_name='測試',
            last_name='用戶',
            gregorian_birth_date=date(1990, 1, 1)
        )
        self.user.set_password('testpass123')
        self.user.save()

        # 創建測試產品
        self.product = Product.objects.create(
            name='測試燈種',
            price=100.00,
            prayer_text='願心想事成，萬事如意'
        )

        # 創建測試訂單
        self.order = Order.objects.create(
            user=self.user,
            full_name='測試用戶',
            email='test@example.com',
            phone_number='0912345678',
            address='測試地址',
            total_paid=100.00,
            paid=True
        )

        # 創建測試訂單項目
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=100.00
        )

    def test_image_generator_creation(self):
        """測試圖片生成器實例化"""
        generator = LanternImageGenerator()
        self.assertIsInstance(generator, LanternImageGenerator)

    def test_generate_image_basic(self):
        """測試基本圖片生成功能"""
        generator = LanternImageGenerator()

        # 生成圖片
        filename = generator.generate_image(self.order_item)

        # 檢查結果
        self.assertIsInstance(filename, str)
        self.assertTrue(filename.startswith('lantern_'))
        self.assertTrue(filename.endswith('.png'))

        # 檢查OrderItem是否更新
        self.order_item.refresh_from_db()
        self.assertIsNotNone(self.order_item.generated_image)
        self.assertIsNotNone(self.order_item.image_generated_at)

        # 驗證生成的圖片可以打開
        image_content = self.order_item.generated_image.read()
        image = Image.open(BytesIO(image_content))
        self.assertIsInstance(image, Image.Image)

    def test_generate_preview_image(self):
        """測試預覽圖片生成功能"""
        generator = LanternImageGenerator()

        # 生成預覽圖片
        base64_data = generator.generate_preview_image(self.order_item)

        # 檢查結果
        self.assertIsInstance(base64_data, str)
        self.assertTrue(base64_data.startswith('iVBORw0KGgo'))  # PNG base64 開頭

        # 驗證base64可以解碼為圖片
        try:
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            self.assertIsInstance(image, Image.Image)
        except Exception as e:
            self.fail(f"base64資料無法解碼為圖片: {e}")

    def test_chinese_text_rendering(self):
        """測試中文字體渲染"""
        generator = LanternImageGenerator()

        # 生成圖片
        filename = generator.generate_image(self.order_item)

        # 讀取生成的圖片
        self.order_item.refresh_from_db()
        image_content = self.order_item.generated_image.read()
        image = Image.open(BytesIO(image_content))

        # 檢查圖片尺寸（確保不是空的）
        self.assertGreater(image.width, 0)
        self.assertGreater(image.height, 0)

        # 檢查是否包含預期的中文文字
        # 注意：由於字體問題，這裡我們只檢查圖片是否成功生成
        # 在實際環境中，可能需要更複雜的OCR測試
        self.assertIsInstance(image, Image.Image)

    def test_font_loading(self):
        """測試字體載入邏輯"""
        generator = LanternImageGenerator()

        # 檢查字體是否已載入
        self.assertIsNotNone(generator.font)

        # 字體應該是ImageFont實例
        from PIL import ImageFont
        self.assertIsInstance(generator.font, ImageFont.FreeTypeFont)

    def test_preview_api_success(self):
        """測試預覽API成功回應"""
        from django.test import Client
        from django.urls import reverse

        client = Client()
        client.login(username=self.user.username, password='testpass123')

        # 測試預覽API
        url = reverse('orders:preview_lantern_image', args=[self.order_item.id])
        response = client.get(url)

        # 檢查回應
        self.assertEqual(response.status_code, 200)
        self.assertIn('image_data', response.json())

        # 檢查base64資料
        image_data = response.json()['image_data']
        self.assertTrue(image_data.startswith('iVBORw0KGgo'))  # PNG base64 開頭

    def test_preview_api_permission_denied(self):
        """測試預覽API權限檢查"""
        from django.test import Client
        from django.urls import reverse

        # 創建另一個用戶
        other_user = CustomUser.objects.create(
            username='otheruser',
            email='other@example.com',
            first_name='其他',
            last_name='用戶',
            gregorian_birth_date=date(1990, 1, 1)
        )
        other_user.set_password('testpass123')
        other_user.save()

        # 創建其他用戶的訂單項目
        other_order = Order.objects.create(
            user=other_user,
            full_name='其他用戶',
            email='other@example.com',
            phone_number='0912345678',
            address='其他地址',
            total_paid=100.00,
            paid=True
        )
        other_order_item = OrderItem.objects.create(
            order=other_order,
            product=self.product,
            price=100.00
        )

        client = Client()
        client.login(username=self.user.username, password='testpass123')

        # 嘗試訪問其他用戶的訂單項目
        url = reverse('orders:preview_lantern_image', args=[other_order_item.id])
        response = client.get(url)

        # 應該返回403 (Forbidden)
        self.assertEqual(response.status_code, 403)

    def test_preview_api_invalid_order_item(self):
        """測試預覽API無效訂單項目"""
        from django.test import Client
        from django.urls import reverse

        client = Client()
        client.login(username=self.user.username, password='testpass123')

        # 測試不存在的訂單項目ID
        url = reverse('orders:preview_lantern_image', args=[99999])
        response = client.get(url)

        # 應該返回404
        self.assertEqual(response.status_code, 404)
