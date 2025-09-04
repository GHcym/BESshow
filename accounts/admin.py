from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
    ]

    # 將我們的自訂欄位分組，並附加到預設的 fieldsets 後面
    fieldsets = UserAdmin.fieldsets + (
        (_("廟宇專屬資訊"), {
            "fields": (
                "uuid",
                "phone_number",
                "gender",
                "gregorian_birth_date",
                "gregorian_birth_time",
                "lunar_birth_date",
                "lunar_birth_time",
                "address_zip_code",
                "address_county",
                "address_district",
                "address_detail",
            )
        }),
    )

    # 設定唯讀欄位，防止管理員手動修改
    readonly_fields = (
        "uuid",
        "lunar_birth_date",
        "lunar_birth_time",
        "last_login",
        "date_joined",
    )


admin.site.register(CustomUser, CustomUserAdmin)
