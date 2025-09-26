"""
圖片上傳服務
負責將生成的圖片上傳到EPD Player
"""
import logging
from django.conf import settings
from epd_integration.services.api_client import EPDAPIClient
from epd_integration.exceptions import EPDAPIException
from ..models import OrderItemPlayerAssignment

logger = logging.getLogger(__name__)


class ImageUploadService:
    """圖片上傳服務類"""

    def __init__(self):
        self.client = EPDAPIClient(token=settings.EPD_API_TOKEN)

    def upload_image(self, assignment: OrderItemPlayerAssignment) -> bool:
        """
        上傳圖片到指定的播放器配對

        Args:
            assignment: OrderItemPlayerAssignment實例

        Returns:
            bool: 上傳是否成功
        """
        try:
            # 檢查是否有生成的圖片
            if not assignment.order_item.generated_image:
                error_msg = "沒有找到生成的圖片"
                assignment.upload_status = 'failed'
                assignment.upload_error = error_msg
                assignment.save()
                logger.error(f"上傳失敗 - {assignment}: {error_msg}")
                return False

            # 更新狀態為上傳中
            assignment.upload_status = 'uploading'
            assignment.save()

            # 獲取或創建EPD設備ID
            epd_id = self._get_or_create_epd_id(assignment)
            if not epd_id:
                error_msg = "無法獲取EPD設備ID"
                assignment.upload_status = 'failed'
                assignment.upload_error = error_msg
                assignment.save()
                logger.error(f"上傳失敗 - {assignment}: {error_msg}")
                return False

            # 檢查 EPD 是否已有圖片
            epd_device = self.client.get_epd(epd_id)
            existing_image = epd_device.images[0] if epd_device.images else None
            
            # 開啟圖片文件
            image_file_path = assignment.order_item.generated_image.path
            logger.info(f"準備上傳圖片文件: {image_file_path}")
            with assignment.order_item.generated_image.open('rb') as image_file:
                image_file.seek(0, 2)  # 移動到文件末尾
                file_size = image_file.tell()
                image_file.seek(0)  # 回到文件開頭
                logger.debug(f"圖片文件大小: {file_size} bytes")

                if existing_image:
                    # 更新現有圖片
                    logger.info(f"更新現有圖片 ID {existing_image.id} 於 EPD {epd_id}")
                    epd_image = self.client.update_image(existing_image.id, image_file)
                    logger.info(f"成功更新圖片 ID {existing_image.id}")
                else:
                    # 上傳新圖片
                    logger.info(f"上傳新圖片到 EPD {epd_id}")
                    epd_image = self.client.upload_image(epd_id, image_file)
                    logger.info(f"成功上傳新圖片到 EPD {epd_id}")

            # 更新成功狀態
            assignment.upload_status = 'completed'
            assignment.epd_id = epd_id
            assignment.uploaded_at = getattr(epd_image, 'created_time', None) or getattr(epd_image, 'updated_time', None)
            assignment.upload_error = None
            assignment.save()

            logger.info(f"圖片上傳成功 - {assignment}")
            return True

        except EPDAPIException as e:
            error_msg = f"EPD API 錯誤: {str(e)}"
            assignment.upload_status = 'failed'
            assignment.upload_error = error_msg
            assignment.save()
            logger.error(f"上傳失敗 - {assignment}: {error_msg}")
            return False
        except Exception as e:
            error_msg = f"意外錯誤: {str(e)}"
            assignment.upload_status = 'failed'
            assignment.upload_error = error_msg
            assignment.save()
            logger.error(f"上傳失敗 - {assignment}: {error_msg}")
            return False

    def _get_or_create_epd_id(self, assignment: OrderItemPlayerAssignment) -> int:
        """
        獲取或創建EPD設備ID

        Args:
            assignment: OrderItemPlayerAssignment實例

        Returns:
            int: EPD設備ID，如果失敗返回None
        """
        try:
            logger.info(f"開始獲取 EPD ID for assignment {assignment.id}, player serial: {assignment.player.serial_number}")

            # 如果已經有epd_id，直接返回
            if assignment.epd_id:
                logger.info(f"使用已設置的EPD ID: {assignment.epd_id}")
                return assignment.epd_id

            # 如果沒有epd_id，這是舊記錄，需要向後兼容
            logger.warning(f"Assignment {assignment.id} 沒有epd_id，使用舊邏輯查找")

            # 根據serial_number獲取player
            logger.debug(f"查詢播放器，serial_number: {assignment.player.serial_number}")
            player = self.client.list_players(serialnum=assignment.player.serial_number)
            logger.debug(f"找到 {len(player)} 個播放器匹配 serial_number {assignment.player.serial_number}")
            if not player:
                logger.error(f"找不到播放器: {assignment.player.serial_number}")
                return None

            epd_player = player[0]
            logger.info(f"使用播放器 ID: {epd_player.id}, EPD 數量: {len(epd_player.epds)}")

            # 根據播放器位置選擇對應的EPD設備
            target_order = assignment.player.position
            logger.debug(f"目標位置 (order): {target_order}")

            # 查找對應order的EPD
            target_epd = None
            for epd in epd_player.epds:
                logger.debug(f"檢查 EPD ID {epd.id}, order {epd.order}")
                if epd.order == target_order:
                    target_epd = epd
                    break

            if target_epd:
                epd_id = target_epd.id
                logger.info(f"找到匹配的 EPD 設備 (位置 {target_order}): {epd_id}")
            else:
                logger.info(f"未找到匹配的 EPD 設備 (位置 {target_order})，將創建新的")
                # 創建指定order的EPD設備
                epd_device = self.client.create_epd(epd_player.id, order=target_order)
                epd_id = epd_device.id
                logger.info(f"成功創建新 EPD 設備 (位置 {target_order}): {epd_id}")

            return epd_id

        except Exception as e:
            logger.error(f"獲取 EPD ID 失敗 for assignment {assignment.id}: {str(e)}", exc_info=True)
            return None