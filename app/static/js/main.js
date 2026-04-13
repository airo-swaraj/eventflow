// Flash message auto-dismiss
document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
        el.style.opacity = '0';
        el.style.transition = 'opacity 0.5s';
        setTimeout(() => el.remove(), 500);
    }, 4000);
});