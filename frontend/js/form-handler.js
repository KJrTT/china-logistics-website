document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.feedback-form');
    
    if (!form) return;

    const getApiUrl = function() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://127.0.0.1:8000/api/feedback/';
        }
        return 'https://china-logistics-website.onrender.com/api/feedback/';
    };
    
    const API_URL = getApiUrl();
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const nameInput = document.getElementById('name');
        const contactInput = document.getElementById('contact');
        const messageInput = document.getElementById('message');
        
        const formData = {
            name: nameInput.value.trim(),
            contact: contactInput.value.trim(),
            message: messageInput.value.trim()
        };
        
        clearErrors();
        
        let hasError = false;
        
        if (!formData.name) {
            showFieldError(nameInput, 'Пожалуйста, введите ваше имя');
            hasError = true;
        }
        
        if (!formData.contact) {
            showFieldError(contactInput, 'Пожалуйста, введите телефон или email');
            hasError = true;
        }
        
        if (!formData.message) {
            showFieldError(messageInput, 'Пожалуйста, напишите сообщение');
            hasError = true;
        }
        
        if (hasError) return;
        
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
                showNotification('Спасибо! Ваша заявка принята.', 'success');
                form.reset();
                submitBtn.textContent = 'Отправлено!';
                submitBtn.style.background = '#22C55E';
                
                setTimeout(function() {
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            } else {
                let errorMessage = 'Произошла ошибка. Попробуйте позже.';
                
                if (result.detail) {
                    if (Array.isArray(result.detail)) {
                        errorMessage = result.detail.map(function(err) {
                            return err.msg || err.message || JSON.stringify(err);
                        }).join(', ');
                    } else if (typeof result.detail === 'string') {
                        errorMessage = result.detail;
                    } else {
                        errorMessage = JSON.stringify(result.detail);
                    }
                }
                
                showNotification('Ошибка: ' + errorMessage, 'error');
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        } catch (error) {
            console.error('Ошибка отправки:', error);
            showNotification('Ошибка соединения с сервером. Проверьте, запущен ли бэкенд.', 'error');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
});

function showFieldError(input, message) {
    input.style.borderColor = '#EF4444';
    input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.15)';
    
    const existingError = input.parentElement.querySelector('.field-error');
    if (existingError) existingError.remove();
    
    const error = document.createElement('div');
    error.className = 'field-error';
    error.textContent = message;
    input.parentElement.appendChild(error);
}

function clearErrors() {
    document.querySelectorAll('.field-error').forEach(function(el) {
        el.remove();
    });
    document.querySelectorAll('.feedback-form input, .feedback-form textarea').forEach(function(el) {
        el.style.borderColor = '';
        el.style.boxShadow = '';
    });
}

function showNotification(message, type) {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = 'toast-notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(function() {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(function() {
        notification.classList.remove('show');
        setTimeout(function() {
            notification.remove();
        }, 400);
    }, 5000);
}