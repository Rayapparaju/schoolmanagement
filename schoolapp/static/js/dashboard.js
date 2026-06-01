// Dashboard JS

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // Counter animation
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.innerText) || 0;
        let current = 0;
        const increment = Math.ceil(target / 50);
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.innerText = current;
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target;
            }
        };
        updateCounter();
    });

    // Sidebar toggle
    window.toggleSidebar = function() {
        const sidebar = document.getElementById('sidebar');
        sidebar.classList.toggle('show');
        let overlay = document.querySelector('.sidebar-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            overlay.onclick = () => sidebar.classList.remove('show');
            document.body.appendChild(overlay);
        }
        overlay.classList.toggle('show');
    };
});
