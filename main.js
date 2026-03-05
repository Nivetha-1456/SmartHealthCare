// ========== GLOBAL FUNCTIONS ==========

// Theme toggle
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        const currentTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', currentTheme);
        themeToggle.innerHTML = currentTheme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';

        themeToggle.addEventListener('click', () => {
            let theme = document.documentElement.getAttribute('data-theme');
            theme = theme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            themeToggle.innerHTML = theme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            showToast(`Switched to ${theme} mode`, 'info');
        });
    }

    // Mobile menu
    const menuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.querySelector('.nav-menu');
    if (menuBtn) {
        menuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Notifications (demo)
    const bell = document.getElementById('notificationBell');
    if (bell) {
        bell.addEventListener('click', () => {
            alert('Notifications panel - coming soon!');
        });
    }

    // Auto-hide alerts
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Toast notification
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) {
        const newContainer = document.createElement('div');
        newContainer.id = 'toastContainer';
        newContainer.className = 'toast-container';
        document.body.appendChild(newContainer);
    }
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i> ${message}`;
    document.getElementById('toastContainer').appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Watch sync (simulated)
function syncWatch() {
    const steps = Math.floor(Math.random() * 5000) + 2000;
    const hr = Math.floor(Math.random() * 40) + 60;
    const spo2 = Math.floor(Math.random() * 5) + 95;
    fetch('/api/watch/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ steps, heart_rate: hr, spo2 })
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                const stepsCounter = document.getElementById('stepsCounter');
                if (stepsCounter) stepsCounter.innerText = steps;
                showToast('Watch synced!', 'success');
            }
        })
        .catch(() => showToast('Sync failed', 'error'));
}

// AI Chat (for ai_doctor.html)
function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const chatWindow = document.getElementById('chatWindow');
    if (!input || !chatWindow) return;
    if (input.value.trim() === '') return;

    // User message
    const userMsg = document.createElement('div');
    userMsg.className = 'message message-user';
    userMsg.innerHTML = `${input.value}<div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>`;
    chatWindow.appendChild(userMsg);
    input.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Simulate AI response
    setTimeout(() => {
        const responses = [
            "Based on your symptoms, rest well.",
            "I recommend checking your blood pressure.",
            "Drink plenty of water.",
            "Your sleep data suggests you need more rest.",
            "Consider a short walk."
        ];
        const r = responses[Math.floor(Math.random() * responses.length)];
        const aiMsg = document.createElement('div');
        aiMsg.className = 'message message-ai';
        aiMsg.innerHTML = `${r}<div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>`;
        chatWindow.appendChild(aiMsg);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 1000);
}

// Optional: voice input simulation (for ai_doctor)
function initVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    if (!voiceBtn) return;
    voiceBtn.addEventListener('click', () => {
        const input = document.getElementById('chatInput');
        if (input) {
            input.value = 'I have a headache'; // Simulated voice input
            showToast('Voice input simulated', 'info');
        }
    });
}

// Video call functions (used in video_call.html)
let timerInterval = null;
let seconds = 0;

function startTimer() {
    if (timerInterval) clearInterval(timerInterval);
    seconds = 0;
    timerInterval = setInterval(() => {
        seconds++;
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        const timerEl = document.getElementById('callTimer');
        if (timerEl) {
            timerEl.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
    }, 1000);
}

function stopTimer() {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = null;
}

function toggleMute() {
    const btn = document.getElementById('muteBtn');
    if (!btn) return;
    const isMuted = btn.innerHTML.includes('microphone-slash');
    btn.innerHTML = isMuted ? '<i class="fas fa-microphone"></i>' : '<i class="fas fa-microphone-slash"></i>';
    showToast(isMuted ? 'Microphone unmuted' : 'Microphone muted', 'info');
}

function toggleCamera() {
    const btn = document.getElementById('cameraBtn');
    const localPlaceholder = document.getElementById('localPlaceholder');
    const localVideo = document.getElementById('localVideo');
    if (!btn || !localPlaceholder || !localVideo) return;
    const isCamOn = btn.innerHTML.includes('video-slash');
    if (isCamOn) {
        btn.innerHTML = '<i class="fas fa-video"></i>';
        localPlaceholder.style.display = 'none';
        localVideo.style.display = 'block';
    } else {
        btn.innerHTML = '<i class="fas fa-video-slash"></i>';
        localPlaceholder.style.display = 'flex';
        localVideo.style.display = 'none';
    }
    showToast(isCamOn ? 'Camera turned on' : 'Camera turned off', 'info');
}

function endCall() {
    stopTimer();
    showToast('Call ended', 'error');
    setTimeout(() => {
        window.location.href = '/patient/dashboard'; // fallback
    }, 1500);
}

function toggleFullScreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

// Auto‑initialize voice input if on AI doctor page
if (document.getElementById('voiceBtn')) {
    initVoiceInput();
}