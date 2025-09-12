# Task: 首頁「立即點燈」修正 (shou-ye-li-ji-dian-deng-xiu-zheng) - DONE

## 執行計劃：
修正首頁「立即點燈」按鈕的連結，使其指向實際的燈種選擇頁面。

## 執行項目：
1.  了解首頁「立即點燈」功能的相關程式碼，確認 `templates/pages/home.html` 中的連結指向 `{% url 'coming_soon' %}`。
2.  分析 `products/urls.py`，確定 `products:product_offering_list` 為燈種選擇頁面的正確 URL。
3.  修改 `templates/pages/home.html`，將 `{% url 'coming_soon' %}` 替換為 `{% url 'products:product_offering_list' %}`。
4.  建立 `shou-ye-li-ji-dian-deng-xiu-zheng-Code-Changes-20250909.diff` 檔案，記錄程式碼變更。
5.  更新 `shou-ye-li-ji-dian-deng-xiu-zheng-PROCESS-20250909.md` 檔案，標記已完成的步驟。

## 執行結果：
首頁「立即點燈」按鈕的連結已成功修正，現在指向 `products:product_offering_list`。相關的程式碼變更已記錄在 `_dev_logs/shou-ye-li-ji-dian-deng-xiu-zheng-Code-Changes-20250909.diff` 中。
