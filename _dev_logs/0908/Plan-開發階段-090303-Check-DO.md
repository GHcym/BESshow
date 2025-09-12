# 開發執行紀錄：開發階段-090303-Check

本文件記錄了 `開發階段-090303-Check` 任務的詳細執行步驟、發現與結果。

## 1. 專案整體架構分析

### 1.1. `settings.py` 分析

- **`INSTALLED_APPS`**:
  - **本地應用**: `accounts`, `pages`, `products`, `cart`, `orders`。
  - **第三方應用**: `allauth`, `crispy_forms`, `crispy_bootstrap5`, `debug_toolbar`。
- **資料庫**:
  - 使用 PostgreSQL (`django.db.backends.postgresql`)。
  - 主機為 `bes-db`，與 Docker 設定一致。
- **使用者模型**:
  - `AUTH_USER_MODEL` 設定為 `accounts.CustomUser`，確認使用者模型已客製化。
- **`django-allauth` 設定**:
  - 登入方式為 `email`。
  - 使用客製化的註冊表單 `accounts.allauth_forms.CustomSignupForm`。
  - 使用客製化的帳號適配器 `accounts.adapter.CustomAccountAdapter`。
- **語言**:
  - `LANGUAGE_CODE` 設定為 `zh-Hant` (繁體中文)。

**結論**: `settings.py` 的配置清晰地反映了專案的技術選型與模組劃分，特別是 `accounts` 應用作為使用者資料管理的核心。

### 1.2. `urls.py` 分析

#### `django_project/urls.py` (根路由)

- **`accounts/`**: 包含 `allauth.urls`，處理標準驗證流程 (登入、登出、密碼重設)。
- **`my-account/`**: 包含 `accounts.urls`，處理客製化的使用者資料功能，此為 `開發階段-090302` 的核心。
- **`products/`**: 包含 `products.urls`，對應燈種管理功能。
- **`cart/`**: 包含 `cart.urls`，對應購物車功能。
- **`orders/`**: 包含 `orders.urls`，對應訂單功能。
- **`""` (根路徑)**: 包含 `pages.urls`，用於處理靜態頁面 (如首頁)。

**結論**: 根路由配置清晰，將不同功能的 URL 分發到各自的應用程式中。`my-account/` 的路徑分離是理解使用者資料管理功能的關鍵。

## 2. `開發階段-090302` 程式碼審查 (信眾個人資料維護)

### 2.1. `accounts` 應用程式檔案分析

- **`models.py`**: `CustomUser` 模型已擴充所有必要的信眾資料欄位。`save()` 方法中實作了從國曆到農曆的自動轉換，使用了 `lunar-python` 函式庫。
- **`forms.py`**: `CustomUserUpdateForm` 是使用者編輯資料的主要介面。它從 JSON 檔案載入資料以實現地址的二級連動下拉選單。`clean()` 方法也包含農曆轉換邏輯，與 `models.py` 中的邏輯有部分重疊，但功能正確。
- **`views.py`**: `UserProfileUpdateView` (對應 `my-account/profile/edit/`) 是使用者更新資料的核心視圖。其 `get_success_url` 方法中已包含對 `next=payment` 參數的處理，這對於串接結帳流程至關重要。
- **`urls.py`**: 路由 `my-account/profile/edit/` 指向 `UserProfileUpdateView`，確認了使用者資料的編輯入口。

## 3. 任務總結與後續步驟

**檢查結論**:
- 專案架構清晰，模組劃分合理。
- `開發階段-090302` 的信眾資料維護功能已完整實作，包含農曆轉換、地址連動等關鍵需求。
- `accounts` 應用中的 `UserProfileUpdateView` 已為 `開發階段-090303` 的結帳流程準備了必要的掛鉤 (`next=payment`)。

**後續建議**:
- 可以安全地開始 `開發階段-090303` 的工作。
- 開發流程將從「燈種列表」開始，然後是「加入購物車」，最後是「結帳流程」。
- 在結帳流程中，將利用 `accounts` 應用已有的 `next=payment` 參數，引導未完善資料的使用者前往 `my-account/profile/edit/` 頁面。

---
**檢查任務完成**
