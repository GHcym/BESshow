// EPD Management JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // API 狀態檢查
    const checkApiButton = document.getElementById('check-api-status');
    if (checkApiButton) {
        checkApiButton.addEventListener('click', checkApiStatus);
    }

    // 圖片上傳拖拽功能
    initImageUpload();
    
    // 自動隱藏訊息
    autoHideMessages();
});

function checkApiStatus() {
    const button = document.getElementById('check-api-status');
    const originalText = button.innerHTML;
    
    // 顯示載入狀態
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 檢查中...';
    button.disabled = true;
    
    fetch('/epd/api/status/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showAlert('success', `API 連線正常 - 找到 ${data.player_count} 個播放器`);
            } else {
                showAlert('danger', `API 連線失敗: ${data.message}`);
            }
        })
        .catch(error => {
            showAlert('danger', `檢查失敗: ${error.message}`);
        })
        .finally(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        });
}

function initImageUpload() {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.querySelector('input[type="file"]');
    
    if (!uploadArea || !fileInput) return;
    
    // 拖拽事件
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            // 可以在這裡添加預覽功能
        }
    });
}

function showAlert(type, message) {
    const alertContainer = document.querySelector('.container-fluid');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // 插入到容器頂部
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // 自動隱藏
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function autoHideMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.classList.remove('show');
                setTimeout(() => alert.remove(), 150);
            }
        }, 5000);
    });
}

// 確認刪除對話框
function confirmDelete(message) {
    return confirm(message || '確定要執行此操作嗎？');
}

// 圖片預覽功能
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('image-preview');
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// 燈牆編輯頁面批量操作功能
function enableAllPlayers() {
    console.log('enableAllPlayers called');
    const checkboxes = document.querySelectorAll('input[name$="-is_enabled"]');
    console.log('Found checkboxes:', checkboxes.length, checkboxes);
    checkboxes.forEach(function(checkbox) {
        console.log('Setting checkbox checked:', checkbox.name);
        checkbox.checked = true;
        checkbox.dispatchEvent(new Event('change'));
    });
    showToast('成功', '已啟用所有播放器位置', 'success');
}

function disableAllPlayers() {
    console.log('disableAllPlayers called');
    const checkboxes = document.querySelectorAll('input[name$="-is_enabled"]');
    console.log('Found checkboxes:', checkboxes.length, checkboxes);
    checkboxes.forEach(function(checkbox) {
        console.log('Setting checkbox unchecked:', checkbox.name);
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change'));
    });
    showToast('成功', '已停用所有播放器位置', 'warning');
}

function clearAllPlayerIds() {
    console.log('clearAllPlayerIds called');
    if (confirm('確定要清除所有 Player ID 嗎？此操作無法復原。')) {
        const inputs = document.querySelectorAll('input[name$="-serial_number"]');
        console.log('Found serial inputs:', inputs.length, inputs);
        inputs.forEach(function(input) {
            console.log('Clearing input:', input.name);
            input.value = '';
        });
        showToast('成功', '已清除所有 Player ID', 'info');
    }
}

// 顯示 Toast 訊息
function showToast(title, message, type) {
    // 簡單的 Toast 實作，可以後續改用 Bootstrap Toast
    const alertClass = type === 'success' ? 'alert-success' :
                      type === 'warning' ? 'alert-warning' : 'alert-info';

    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show position-fixed"
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            <strong>${title}:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', alertHtml);

    // 3秒後自動消失
    setTimeout(function() {
        const alert = document.querySelector('.alert:last-of-type');
        if (alert) {
            alert.remove();
        }
    }, 3000);
}