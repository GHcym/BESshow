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