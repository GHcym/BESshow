"""
燈牆管理表單
"""
from django import forms
from django.forms import modelformset_factory
from .models import LanternWall, LanternPlayer


class LanternWallForm(forms.ModelForm):
    """燈牆基本資訊表單"""
    class Meta:
        model = LanternWall
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '輸入燈牆名稱'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '輸入燈牆描述（可選）'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class LanternPlayerForm(forms.ModelForm):
    """燈牆播放器表單"""
    position = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = LanternPlayer
        fields = ['position', 'serial_number', 'is_enabled']
        widgets = {
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '輸入Player ID (如: CM20250924FF)'
            }),
            'is_enabled': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['serial_number'].widget.attrs['placeholder'] = f'位置 {self.instance.position} 的Player ID'

    def clean_serial_number(self):
        """簡化驗證：允許任意字串輸入"""
        serial_number = self.cleaned_data.get('serial_number')
        if serial_number:
            # 移除格式驗證，允許任意字串
            pass
        return serial_number


# 建立播放器位置的表單集
LanternPlayerFormSet = modelformset_factory(
    LanternPlayer,
    form=LanternPlayerForm,
    extra=0,  # 不新增額外表單
    can_delete=False,  # 不允許刪除
    min_num=0,
    max_num=12,
    validate_min=False,
    validate_max=True
)


class LanternWallWithPlayersForm:
    """燈牆及其播放器整合表單"""

    def __init__(self, instance=None, data=None, files=None):
        self.instance = instance
        self.wall_form = LanternWallForm(instance=self.instance, data=data, files=files)

        # 如果是編輯現有燈牆，取得現有的播放器
        if self.instance:
            players = self.instance.players.all().order_by('position')
            # 確保有12個位置
            existing_positions = set(players.values_list('position', flat=True))
            if len(existing_positions) < 12:
                for pos in range(1, 13):
                    if pos not in existing_positions:
                        LanternPlayer.objects.create(
                            wall=self.instance,
                            position=pos
                        )
            # 重新取得
            players_qs = self.instance.players.all().order_by('position')
            self.players_formset = LanternPlayerFormSet(
                queryset=players_qs,
                data=data,
                files=files,
                prefix='players'
            )
        else:
            # 新建燈牆：使用空的 queryset
            initial_data = [{'position': i} for i in range(1, 13)]
            self.players_formset = LanternPlayerFormSet(
                queryset=LanternPlayer.objects.none(),
                initial=initial_data,
                data=data,
                files=files,
                prefix='players'
            )

    def is_valid(self):
        """檢查主表單和表單集是否都有效"""
        return self.wall_form.is_valid() and self.players_formset.is_valid()

    def save(self, commit=True):
        """儲存燈牆和關聯的播放器"""
        import logging
        logger = logging.getLogger(__name__)

        logger.info(f'開始儲存燈牆表單: commit={commit}')
        if not self.is_valid():
            logger.error('表單驗證失敗，無法儲存')
            raise ValueError("表單資料無效，無法儲存")

        # 儲存燈牆實例
        logger.info('儲存燈牆實例...')
        wall = self.wall_form.save(commit=commit)
        logger.info(f'燈牆實例儲存成功: {wall.name} (ID: {wall.id})')

        # 處理播放器表單集 - 確保所有位置都被處理
        logger.info('處理播放器表單集...')

        # 首先儲存表單集中的播放器（這些是用戶實際編輯過的）
        players = self.players_formset.save(commit=False)
        logger.info(f'表單集返回 {len(players)} 個播放器實例')

        saved_count = 0
        updated_positions = set()

        for player in players:
            player.wall = wall
            logger.info(f'準備儲存播放器: position={player.position}, serial_number={player.serial_number}, is_enabled={player.is_enabled}')
            if commit:
                try:
                    player.save()
                    saved_count += 1
                    updated_positions.add(player.position)
                    logger.info(f'播放器儲存成功: position={player.position}')
                except Exception as e:
                    logger.error(f'播放器儲存失敗 position={player.position}: {str(e)}', exc_info=True)
                    raise

        # 確保所有12個位置都存在並正確設定
        # 對於那些沒有在POST資料中出現的位置，我們需要從現有資料庫記錄中獲取它們
        if self.instance:  # 編輯模式
            logger.info('檢查是否所有位置都已正確處理...')
            existing_players = wall.players.all()
            for player in existing_players:
                if player.position not in updated_positions:
                    logger.info(f'位置 {player.position} 沒有在表單集中更新，保持現有資料')
                    # 這些播放器已經存在於資料庫中，不需要重新儲存

        logger.info(f'成功處理 {saved_count} 個播放器')

        # 如果表單集有 m2m 關係，需要單獨保存
        if commit and hasattr(self.players_formset, 'save_m2m'):
            logger.info('儲存 m2m 關係...')
            self.players_formset.save_m2m()

        logger.info(f'燈牆表單儲存完成: {wall.name}')
        return wall

    @property
    def errors(self):
        """收集並返回所有錯誤"""
        errors = {}
        if self.wall_form.errors:
            errors.update(self.wall_form.errors)
        
        formset_errors = self.players_formset.errors
        if any(formset_errors):
            errors['players'] = formset_errors
            
        return errors

    @property
    def non_form_errors(self):
        """返回非字段錯誤"""
        return self.wall_form.non_field_errors() + self.players_formset.non_form_errors()

    def __getitem__(self, key):
        """允許模板通過字典方式訪問表單和表單集"""
        if key in self.wall_form.fields:
            return self.wall_form[key]
        if key == 'players_formset':
            return self.players_formset
        raise KeyError(key)