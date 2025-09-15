"""
註冊 EPD API 使用者的管理指令
"""
import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = '註冊新的 EPD API 使用者'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='使用者 email'
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help='使用者密碼 (至少 5 個字元)'
        )
        parser.add_argument(
            '--name',
            type=str,
            required=True,
            help='使用者姓名'
        )
        parser.add_argument(
            '--base-url',
            type=str,
            help='EPD API 基礎 URL',
            default=getattr(settings, 'EPD_API_BASE_URL', 'http://43.213.2.34/api')
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        name = options['name']
        base_url = options['base_url']

        if len(password) < 5:
            self.stdout.write(
                self.style.ERROR('密碼至少需要 5 個字元')
            )
            return

        self.stdout.write(f'正在註冊使用者: {email}')
        
        try:
            response = requests.post(
                f"{base_url}/user/create/",
                json={
                    'email': email,
                    'password': password,
                    'name': name
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 使用者註冊成功！')
                )
                self.stdout.write(f'Email: {email}')
                self.stdout.write(f'Name: {name}')
                self.stdout.write('\n現在可以使用以下指令測試 API:')
                self.stdout.write(
                    f'docker compose -f docker-compose.yml exec bes-app python manage.py test_epd_api --email={email} --password={password}'
                )
            elif response.status_code == 400:
                error_data = response.json() if response.content else {}
                self.stdout.write(
                    self.style.ERROR(f'❌ 註冊失敗: {error_data}')
                )
                if 'email' in error_data:
                    self.stdout.write('提示: 此 email 可能已被使用')
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ 註冊失敗 ({response.status_code}): {response.text}')
                )
                
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'❌ 連線錯誤: {str(e)}')
            )