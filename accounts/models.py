import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from lunar_python import Lunar, Solar

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
    lunar_birth_time = models.CharField(_("農曆時辰"), max_length=20, blank=True, default=_("吉時"))

    # 八字相關欄位
    bazi_year = models.CharField(_("八字年柱"), max_length=20, blank=True, help_text=_("天干地支年柱，如甲辰年"))
    bazi_month = models.CharField(_("八字月柱"), max_length=20, blank=True, help_text=_("天干地支月柱，如乙巳月"))
    bazi_day = models.CharField(_("八字日柱"), max_length=20, blank=True, help_text=_("天干地支日柱，如丙午日"))
    zodiac_animal = models.CharField(_("生肖"), max_length=10, blank=True, help_text=_("生肖動物，如龍"))

    # 地址資訊
    address_zip_code = models.CharField(_("郵遞區號"), max_length=5, blank=True)
    address_county = models.CharField(_("縣市"), max_length=20, blank=True)
    address_district = models.CharField(_("鄉鎮市區"), max_length=20, blank=True)
    address_detail = models.CharField(_("詳細地址"), max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.gregorian_birth_date:
            solar = Solar.fromYmd(
                self.gregorian_birth_date.year,
                self.gregorian_birth_date.month,
                self.gregorian_birth_date.day
            )
            lunar = solar.getLunar()
            # Store as YYYY-MM-DD format to match the test
            self.lunar_birth_date = f"{lunar.getYear()}-{lunar.getMonth()}-{lunar.getDay()}"

            if self.gregorian_birth_time:
                solar_with_time = Solar.fromYmdHms(
                    self.gregorian_birth_date.year,
                    self.gregorian_birth_date.month,
                    self.gregorian_birth_date.day,
                    self.gregorian_birth_time.hour,
                    self.gregorian_birth_time.minute,
                    self.gregorian_birth_time.second
                )
                lunar_with_time = solar_with_time.getLunar()
                # The complete time pillar (天干 + 地支)
                self.lunar_birth_time = f"{lunar_with_time.getTimeGan()}{lunar_with_time.getTimeZhi()}時"
            else:
                # If no time is provided, default to "吉時"
                self.lunar_birth_time = "吉時"

            # 計算八字
            bazi_data = self.get_complete_bazi()
            if bazi_data:
                self.bazi_year = bazi_data['year']
                self.bazi_month = bazi_data['month']
                self.bazi_day = bazi_data['day']
                self.zodiac_animal = bazi_data['zodiac']

        super().save(*args, **kwargs)

    def get_complete_bazi(self):
        """
        計算完整的八字（天干地支）
        返回包含年柱、月柱、日柱和生肖的字典
        """
        if not self.gregorian_birth_date:
            return None

        # 建立農曆物件
        solar = Solar.fromYmd(
            self.gregorian_birth_date.year,
            self.gregorian_birth_date.month,
            self.gregorian_birth_date.day
        )
        lunar = solar.getLunar()

        # 年柱：天干 + 地支 + 年
        year_gan = lunar.getYearGan()
        year_zhi = lunar.getYearZhi()
        bazi_year = f"{year_gan}{year_zhi}年"

        # 月柱：天干 + 地支 + 月
        month_gan = lunar.getMonthGan()
        month_zhi = lunar.getMonthZhi()
        bazi_month = f"{month_gan}{month_zhi}月"

        # 日柱：天干 + 地支 + 日
        day_gan = lunar.getDayGan()
        day_zhi = lunar.getDayZhi()
        bazi_day = f"{day_gan}{day_zhi}日"

        # 生肖
        zodiac_animal = lunar.getYearShengXiao()

        return {
            'year': bazi_year,
            'month': bazi_month,
            'day': bazi_day,
            'zodiac': zodiac_animal
        }

    def get_bazi_display(self):
        """
        返回完整的生辰八字字串。
        """
        if not self.bazi_year or not self.bazi_month or not self.bazi_day:
            return ""
        
        time_display = self.lunar_birth_time if self.lunar_birth_time else "吉時"
        return f"{self.bazi_year} {self.bazi_month} {self.bazi_day} {time_display}"

    def get_lunar_birth_display_chinese(self):
        """
        返回中文格式的農曆生日和時辰。
        """
        if not self.gregorian_birth_date or not self.bazi_year:
            return ""

        # 年份使用天干地支
        year_part = self.bazi_year

        solar = Solar.fromYmd(
            self.gregorian_birth_date.year,
            self.gregorian_birth_date.month,
            self.gregorian_birth_date.day
        )
        lunar = solar.getLunar()
        month_in_chinese = lunar.getMonthInChinese()
        day_in_chinese = lunar.getDayInChinese()

        date_part = f"{year_part}{month_in_chinese}月{day_in_chinese}日"

        time_part = ""
        if self.lunar_birth_time and self.lunar_birth_time != "吉時":
            # 從 "癸巳時" 提取 "巳時"
            time_part = self.lunar_birth_time[1:3]
        else:
            time_part = "吉時"

        return f"{date_part}{time_part}"

    def __str__(self):
        # 如果有姓名，顯示姓名，否則顯示 email
        if self.first_name and self.last_name:
            return f"{self.last_name}{self.first_name}"
        return self.email