"""
測試 EPD API 連線的管理指令
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from epd_integration.services.api_client import EPDAPIClient
from epd_integration.exceptions import EPDAPIException


class Command(BaseCommand):
    help = '測試 EPD API 連線和基本功能'

    def add_arguments(self, parser):
        parser.add_argument(
            '--token',
            type=str,
            help='直接使用 EPD API token',
            default=getattr(settings, 'EPD_API_TOKEN', None)
        )
        parser.add_argument(
            '--email',
            type=str,
            help='EPD API 使用者 email',
            default=getattr(settings, 'EPD_API_EMAIL', None)
        )
        parser.add_argument(
            '--password',
            type=str,
            help='EPD API 使用者密碼',
            default=getattr(settings, 'EPD_API_PASSWORD', None)
        )
        parser.add_argument(
            '--base-url',
            type=str,
            help='EPD API 基礎 URL',
            default=getattr(settings, 'EPD_API_BASE_URL', 'http://43.213.2.34/api')
        )

    def handle(self, *args, **options):
        token = options['token']
        email = options['email']
        password = options['password']
        base_url = options['base_url']

        if not token and (not email or not password):
            self.stdout.write(
                self.style.ERROR('請提供 EPD API 的 token 或 email/password')
            )
            return

        self.stdout.write(f'測試 EPD API 連線: {base_url}')
        
        try:
            if token:
                # 使用現有 token
                self.stdout.write(f'使用提供的 Token: {token[:20]}...')
                client = EPDAPIClient(base_url=base_url, token=token)
            else:
                # 使用 email/password 認證
                client = EPDAPIClient(base_url=base_url)
                self.stdout.write('正在測試認證...')
                auth_token = client.authenticate(email, password)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 認證成功，Token: {auth_token.token[:20]}...')
                )
            
            # 測試列出播放器
            self.stdout.write('正在測試列出播放器...')
            players = client.list_players()
            self.stdout.write(
                self.style.SUCCESS(f'✓ 成功取得 {len(players)} 個播放器')
            )
            
            for player in players:
                self.stdout.write(f'  - 播放器 ID: {player.id}, 序號: {player.serialnum}')
            
            # 測試列出 EPD 設備
            self.stdout.write('正在測試列出 EPD 設備...')
            epds = client.list_epds()
            self.stdout.write(
                self.style.SUCCESS(f'✓ 成功取得 {len(epds)} 個 EPD 設備')
            )
            
            for epd in epds:
                self.stdout.write(f'  - EPD ID: {epd.id}, 順序: {epd.order}')
            
            # 測試列出圖片
            self.stdout.write('正在測試列出圖片...')
            images = client.list_images()
            self.stdout.write(
                self.style.SUCCESS(f'✓ 成功取得 {len(images)} 張圖片')
            )
            
            for image in images:
                self.stdout.write(f'  - 圖片 ID: {image.id}')
            
            self.stdout.write(
                self.style.SUCCESS('\n🎉 所有 EPD API 測試通過！')
            )
            
        except EPDAPIException as e:
            self.stdout.write(
                self.style.ERROR(f'❌ EPD API 錯誤: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ 未預期的錯誤: {str(e)}')
            )