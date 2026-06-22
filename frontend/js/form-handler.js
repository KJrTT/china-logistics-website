// form-handler.js — отправка формы на бэкенд

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.feedback-form');
    
    if (!form) return;
    const getApiUrl = () => {
        // Если мы на локальном сервере (localhost или 127.0.0.1)
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://127.0.0.1:8000/api/feedback/';
        }
        // Если мы на Render (или любом другом продакшен-сервере)
        return 'https://china-logistics-website.onrender.com/api/feedback/';
    };
    
    const API_URL = getApiUrl();
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value.trim(),
            contact: document.getElementById('contact').value.trim(),
            message: document.getElementById('message').value.trim()
        };
        
        if (!formData.name || formData.name.length < 2) {
            showNotification('Пожалуйста, введите ваше имя (минимум 2 символа)');
            return;
        }
        
        if (!formData.contact || formData.contact.length < 5) {
            showNotification('Пожалуйста, введите телефон или email');
            return;
        }
        
        if (!formData.message || formData.message.length < 10) {
            showNotification('Сообщение должно содержать минимум 10 символов');
            return;
        }
        
        const submitBtn = form.querySelector('.btn-submit');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Отправка...';
        submitBtn.disabled = true;
        
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showNotification('Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время.');
                form.reset();
                submitBtn.textContent = 'Отправлено!';
                submitBtn.style.background = '#22C55E';
                
                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            } else {
                const errorMsg = result.detail || 'Произошла ошибка. Попробуйте позже.';
                showNotification('Ошибка: ' + errorMsg);
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        } catch (error) {
            console.error('Ошибка отправки:', error);
            showNotification('Ошибка соединения с сервером. Проверьте, запущен ли бэкенд.');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
});

function showNotification(message) {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = 'toast-notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.classList.add('show'), 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 400);
    }, 5000);
}