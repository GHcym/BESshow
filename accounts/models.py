import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    擴充預設的 User 模型，以儲存 BESshow 專案所需的額外使用者資料。
    """
    # 根據需求文件，我們嚴格區分內部 ID、公開 ID 與登入憑證
    # 內部 ID: 沿用 Django 預設的 auto-incrementing id
    # 公開 ID: 使用 UUID，用於 API 或外部連結，避免暴露內部 ID
    uuid = models.UUIDField(
        _("公開識別碼"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("用於 API 的唯一識別碼，不可變更。")
    )

    # 登入憑證: email (來自 AbstractUser) 和 phone_number
    # 為了讓管理者能不透過手機號碼建立帳號，此處允許為空
    # 但在使用者註冊表單中會設定為必填
    phone_number = models.CharField(
        _("手機號碼"),
        max_length=20,
        unique=True,
        null=True, # 允許資料庫中為空
        blank=True, # 允許表單中為空（主要針對後台）
        help_text=_("用於登入和接收通知。")
    )

    # 性別選項
    class Gender(models.TextChoices):
        MALE = 'M', _('善男')
        FEMALE = 'F', _('信女')
        OTHER = 'O', _('善信')

    gender = models.CharField(
        _("性別"),
        max_length=1,
        choices=Gender.choices,
        default=Gender.OTHER,
        help_text=_("稱謂，用於疏文或感謝狀。")
    )

    # 生日資訊
    # 國曆生日在註冊表單中為必填
    gregorian_birth_date = models.DateField(
        _("國曆生日"),
        null=True, # 允許資料庫中為空
        blank=True, # 允許表單中為空（主要針對後台）
    )
    # 國曆時辰為選填
    gregorian_birth_time = models.TimeField(
        _("國曆出生時間"),
        null=True,
        blank=True,
    )
    # 農曆生日由國曆生日轉換而來，儲存為文字
    lunar_birth_date = models.CharField(_("農曆生日"), max_length=30, blank=True)
    lunar_birth_time = models.CharField(_("農曆時辰"), max_length=10, blank=True, default=_("吉時"))

    # 地址資訊
    address_zip_code = models.CharField(_("郵遞區號"), max_length=5, blank=True)
    address_county = models.CharField(_("縣市"), max_length=20, blank=True)
    address_district = models.CharField(_("鄉鎮市區"), max_length=20, blank=True)
    address_detail = models.CharField(_("詳細地址"), max_length=255, blank=True)

    def __str__(self):
        # 如果有姓名，顯示姓名，否則顯示 email
        if self.first_name and self.last_name:
            return f"{self.last_name}{self.first_name}"
        return self.email
