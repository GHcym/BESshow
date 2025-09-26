from PIL import Image, ImageDraw, ImageFont
import os
import logging
import platform
import base64
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from orders.models import OrderItem

logger = logging.getLogger(__name__)


class LanternImageGenerator:
    """
    燈種圖片生成器
    使用Pillow生成個人化燈種圖片
    """

    def _find_font(self):
        """
        查找可用的中文字體路徑
        按優先順序檢查多個字體路徑
        """
        system = platform.system()

        # 定義不同系統的字體路徑
        font_paths = {
            'Linux': [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            ],
            'Darwin': [  # macOS
                '/System/Library/Fonts/STHeiti Light.ttc',
                '/System/Library/Fonts/PingFang.ttc',
                '/System/Library/Fonts/Arial Unicode.ttf',
            ],
            'Windows': [
                'C:\\Windows\\Fonts\\msyh.ttc',  # 微軟雅黑
                'C:\\Windows\\Fonts\\simsun.ttc',  # 新宋體
                'C:\\Windows\\Fonts\\simhei.ttf',  # 黑體
                'C:\\Windows\\Fonts\\arial.ttf',
            ]
        }

        # 獲取當前系統的字體路徑列表
        system_fonts = font_paths.get(system, [])

        # 首先檢查自訂字體
        custom_font = getattr(settings, 'LANTERN_FONT_PATH', None)
        if custom_font and os.path.exists(custom_font):
            logger.info(f"使用自訂字體: {custom_font}")
            return custom_font

        # 檢查系統字體
        for font_path in system_fonts:
            if os.path.exists(font_path):
                logger.info(f"使用系統字體: {font_path}")
                return font_path

        # 如果都失敗，返回 None
        logger.warning("未找到合適的中文字體")
        return None

    def _create_default_base_image(self):
        """
        創建預設的底圖
        包含燈籠主題的設計
        """
        # 創建背景
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color=(255, 248, 220))  # 淺米色背景
        draw = ImageDraw.Draw(image)

        # 繪製燈籠輪廓
        lantern_color = (139, 69, 19)  # 褐色
        # 燈籠主體
        draw.rectangle([200, 100, 600, 500], fill=lantern_color, outline=(0, 0, 0), width=3)
        # 燈籠頂部
        draw.polygon([(350, 50), (450, 50), (425, 100), (375, 100)], fill=lantern_color, outline=(0, 0, 0), width=2)
        # 燈籠底部
        draw.polygon([(375, 500), (425, 500), (450, 550), (350, 550)], fill=lantern_color, outline=(0, 0, 0), width=2)

        # 添加裝飾文字
        try:
            title_font = ImageFont.truetype(self.font.path, 24) if hasattr(self.font, 'path') else self.font
        except:
            title_font = self.font

        # 標題
        title = "祈福燈籠"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        draw.text(((width - title_width) // 2, 30), title, fill=(139, 69, 19), font=title_font)

        logger.info("創建預設燈籠底圖")
        return image

    def __init__(self):
        # 初始化字體路徑
        self.font_path = self._find_font()
        self.font = ImageFont.truetype(self.font_path, 40) if self.font_path else ImageFont.load_default()

        # 設定底圖路徑
        self.base_image_path = getattr(settings, 'LANTERN_BASE_IMAGE_PATH', 'static/images/lantern_base.png')
        logger.info(f"底圖路徑設定為: {self.base_image_path}")

    def _get_font(self, size):
        """獲取指定大小的字體"""
        if self.font_path:
            return ImageFont.truetype(self.font_path, size), size
        return ImageFont.load_default(), 40

    def _get_fitting_font(self, text, max_width):
        """根據文字長度動態調整字型大小，使其適合最大寬度"""
        if not self.font_path:
            return ImageFont.load_default(), 40

        size = 40
        while size > 10:
            font, _ = self._get_font(size)
            bbox = font.getbbox(text)
            width = bbox[2] - bbox[0]
            if width <= max_width:
                return font, size
            size -= 2
        return self._get_font(10)

    def _generate_image_content(self, order_item: OrderItem) -> Image.Image:
        """
        生成圖片內容的共用邏輯

        Args:
            order_item: OrderItem實例

        Returns:
            PIL Image物件
        """
        # 優先使用產品圖片作為底圖
        if order_item.product.image and order_item.product.image.path:
            try:
                base_image = Image.open(order_item.product.image.path)
                logger.info(f"成功載入產品底圖: {order_item.product.image.path}")
            except Exception as e:
                logger.error(f"載入產品底圖失敗 {order_item.product.image.path}: {e}")
                # 回退到靜態底圖
                if os.path.exists(self.base_image_path):
                    try:
                        base_image = Image.open(self.base_image_path)
                        logger.info(f"成功載入靜態底圖: {self.base_image_path}")
                    except Exception as e2:
                        logger.error(f"載入靜態底圖失敗 {self.base_image_path}: {e2}")
                        base_image = self._create_default_base_image()
                else:
                    logger.warning(f"靜態底圖不存在，使用預設底圖: {self.base_image_path}")
                    base_image = self._create_default_base_image()
        else:
            logger.warning(f"產品沒有圖片，使用靜態底圖")
            # 使用靜態底圖
            if os.path.exists(self.base_image_path):
                try:
                    base_image = Image.open(self.base_image_path)
                    logger.info(f"成功載入靜態底圖: {self.base_image_path}")
                except Exception as e:
                    logger.error(f"載入靜態底圖失敗 {self.base_image_path}: {e}")
                    base_image = self._create_default_base_image()
            else:
                logger.warning(f"靜態底圖不存在，使用預設底圖: {self.base_image_path}")
                base_image = self._create_default_base_image()

        # 創建繪圖物件
        draw = ImageDraw.Draw(base_image)

        # 準備個人化資訊 - 三列佈局
        lines = []

        # 第一列：生辰八字
        if order_item.order.user and hasattr(order_item.order.user, 'get_bazi_display'):
            bazi = order_item.order.user.get_bazi_display()
            if bazi:
                lines.append(bazi)

        # 第二列：姓名
        if order_item.order.full_name:
            lines.append(order_item.order.full_name)

        # 第三列：祈福語
        if order_item.product.prayer_text:
            lines.append(order_item.product.prayer_text)

        # 繪製多行文字 - 從底部開始定位，根據列設定不同顏色
        line_spacing = 10  # 行間距
        vertical_offset = 5  # 整體往上移動5像素

        # 定義每列的顏色：第一列黑色，第二列紅色，第三列黑色
        colors = [(0, 0, 0), (255, 0, 0), (0, 0, 0)]

        # 初始化第二列字體大小記錄
        name_font_size = None

        # 先計算所有行的字體和高度
        line_info = []
        for i, line in enumerate(lines):
            if i == 1:  # 第二列：姓名
                font, size = self._get_fitting_font(line, 168)
                name_font_size = size
            elif i == 2:  # 第三列：祈福語
                temp_font, temp_size = self._get_fitting_font(line, 168)
                if name_font_size is not None and temp_size > name_font_size:
                    font, size = self._get_font(name_font_size)
                else:
                    font, size = temp_font, temp_size
            else:  # 其他列
                font, size = self._get_fitting_font(line, 168)

            bbox = draw.textbbox((0, 0), line, font=font)
            text_height = bbox[3] - bbox[1]
            line_info.append({
                'text': line,
                'font': font,
                'height': text_height,
                'color': colors[i] if i < len(colors) else (0, 0, 0)
            })

        # 從底部開始計算位置
        if line_info:
            # 第三列的位置：圖片高度 - 行間距 - 第三列字體高度
            third_index = 2
            if len(line_info) > third_index:
                third_height = line_info[third_index]['height']
                current_y = base_image.height - line_spacing - third_height - vertical_offset
            else:
                # 如果沒有第三列，使用預設位置
                current_y = base_image.height - 100 - vertical_offset

            # 從第三列往上計算其他列的位置
            for i in range(len(line_info) - 1, -1, -1):
                line_data = line_info[i]
                text_width = draw.textbbox((0, 0), line_data['text'], font=line_data['font'])[2] - draw.textbbox((0, 0), line_data['text'], font=line_data['font'])[0]
                x = (base_image.width - text_width) // 2
                y = current_y

                # 繪製文字
                draw.text((x, y), line_data['text'], fill=line_data['color'], font=line_data['font'])

                # 更新下一個文字的Y座標（往上）
                if i > 0:  # 如果不是第一列
                    current_y -= line_info[i-1]['height'] + line_spacing

        return base_image

    def generate_image(self, order_item: OrderItem) -> str:
        """
        為訂單項目生成個人化圖片

        Args:
            order_item: OrderItem實例

        Returns:
            生成的圖片檔案名稱
        """
        try:
            base_image = self._generate_image_content(order_item)

            # 儲存圖片到記憶體
            buffer = BytesIO()
            base_image.save(buffer, format='PNG')
            buffer.seek(0)

            # 生成檔案名稱
            filename = f"lantern_{order_item.id}_{order_item.order.order_key}.png"

            # 儲存到模型
            try:
                order_item.generated_image.save(filename, ContentFile(buffer.getvalue()), save=False)
                order_item.image_generated_at = timezone.now()
                order_item.save()
                logger.info(f"成功生成圖片: {filename} for order_item {order_item.id}")
            except Exception as e:
                logger.error(f"儲存圖片失敗 for order_item {order_item.id}: {e}")
                raise Exception(f"圖片儲存失敗: {str(e)}")

            return filename

        except Exception as e:
            logger.error(f"圖片生成失敗 for order_item {order_item.id}: {str(e)}")
            raise Exception(f"圖片生成失敗: {str(e)}")

    def generate_preview_image(self, order_item: OrderItem) -> str:
        """
        為訂單項目生成預覽圖片（不儲存）

        Args:
            order_item: OrderItem實例

        Returns:
            base64編碼的PNG圖片資料
        """
        try:
            base_image = self._generate_image_content(order_item)

            # 儲存圖片到記憶體並編碼為base64
            buffer = BytesIO()
            base_image.save(buffer, format='PNG')
            buffer.seek(0)

            # 編碼為base64
            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

            logger.info(f"成功生成預覽圖片 for order_item {order_item.id}")
            return image_data

        except Exception as e:
            logger.error(f"預覽圖片生成失敗 for order_item {order_item.id}: {str(e)}")
            raise Exception(f"預覽圖片生成失敗: {str(e)}")