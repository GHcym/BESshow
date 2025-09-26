"""
燈牆管理測試
"""
import django
from django.test import TestCase
from accounts.models import CustomUser
from .models import LanternWall, LanternPlayer
from .forms import LanternPlayerForm


class LanternPlayerFormTest(TestCase):
    """測試LanternPlayer表單"""

    def setUp(self):
        """測試設置"""
        # 創建測試用戶
        self.user = CustomUser.objects.create_superuser(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # 創建測試燈牆
        self.wall = LanternWall.objects.create(
            name='測試燈牆',
            description='用於測試的燈牆'
        )

        # 創建測試播放器
        self.player = LanternPlayer.objects.create(
            wall=self.wall,
            position=1,
            serial_number='CM20250924FF',
            is_enabled=True
        )

    def test_valid_player_id_format(self):
        """測試有效的Player ID格式"""
        valid_ids = [
            'CM20250924FF',
            'CM20250101AA',
            'CM20251231ZZ',
            'CM20250201AB'
        ]

        for player_id in valid_ids:
            with self.subTest(player_id=player_id):
                form_data = {
                    'serial_number': player_id,
                    'is_enabled': True
                }
                form = LanternPlayerForm(data=form_data, instance=self.player)
                self.assertTrue(form.is_valid(), f"Player ID {player_id} 應該是有效的")
                self.assertEqual(form.cleaned_data['serial_number'], player_id)

    def test_invalid_player_id_format(self):
        """測試無效的Player ID格式"""
        invalid_ids = [
            'CM20250924F',      # 太短
            'CM20250924FFF',    # 太長
            'CM20250924ff',     # 小寫字母
            'CM20250924F1',     # 包含數字
            'XX20250924FF',     # 錯誤前綴
            'CM202509241F',     # 日期格式錯誤
            'CM20251324FF',     # 無效日期
            'CM20250932FF',     # 無效日期
            'INVALID',          # 完全無效
        ]

        for player_id in invalid_ids:
            with self.subTest(player_id=player_id):
                form_data = {
                    'serial_number': player_id,
                    'is_enabled': True
                }
                form = LanternPlayerForm(data=form_data, instance=self.player)
                self.assertFalse(form.is_valid(), f"Player ID {player_id} 應該是無效的")
                self.assertIn('serial_number', form.errors)

    def test_player_id_validation_error_message(self):
        """測試Player ID驗證錯誤訊息"""
        form_data = {
            'serial_number': 'INVALID',
            'is_enabled': True
        }
        form = LanternPlayerForm(data=form_data, instance=self.player)
        self.assertFalse(form.is_valid())
        self.assertIn('Player ID格式錯誤', str(form.errors['serial_number']))

    def test_empty_player_id_allowed(self):
        """測試允許空的Player ID"""
        form_data = {
            'serial_number': '',
            'is_enabled': True
        }
        form = LanternPlayerForm(data=form_data, instance=self.player)
        self.assertTrue(form.is_valid(), "空的Player ID應該是允許的")
        self.assertEqual(form.cleaned_data['serial_number'], '')